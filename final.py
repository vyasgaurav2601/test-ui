import streamlit as st

# Set full page width
st.set_page_config(layout="wide")

# ---------------------------
# SESSION STATE INITIALIZATION
# ---------------------------
if 'page' not in st.session_state:
    st.session_state.page = 1  # 1 = initial, 2 = details fetched, 3 = analysis results
if 'jira_details' not in st.session_state:
    st.session_state.jira_details = {}
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = {}
if 'jira_key' not in st.session_state:
    st.session_state.jira_key = ""

# For preserving file uploads
if 'new_logs_files' not in st.session_state:
    st.session_state.new_logs_files = None
if 'new_attachments_files' not in st.session_state:
    st.session_state.new_attachments_files = None
# Upload counter used to force resetting uploader keys when a new Jira key is fetched
if 'upload_counter' not in st.session_state:
    st.session_state.upload_counter = 0

# ---------------------------
# CUSTOM CSS
# ---------------------------
st.markdown("""
    <style>
    /* Banner styling: 36px, bold */
    .banner {
        background-color: #90EE90;
        padding: 25px;
        text-align: center;
        font-size: 36px;
        font-weight: bolder;
        color: black;
        margin-bottom: 20px;
    }
    /* Section heading styling */
    .section-heading {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    /* Analysis result box styling */
    .analysis-box {
        background-color: #fff;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 20px;
    }
    /* Base button styling */
    .stButton > button {
        background-color: #90EE90 !important;
        color: black !important;
        border: none !important;
    }
    /* Analyze button override: 36px font, 36px line-height, normal weight, forced min-height */
    #analyze-container .stButton > button {
        font-size: 36px !important;
        line-height: 36px !important;
        font-weight: normal !important;
        padding: 20px 40px !important;
        width: 100% !important;
        border-radius: 10px !important;
        min-height: 90px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# BANNER (Always visible)
# ---------------------------
st.markdown('<div class="banner">Virtual On-Call Engineer</div>', unsafe_allow_html=True)

# ---------------------------
# LAYOUT: Left column (0.29) and Right column (0.70)
# ---------------------------
left_col, right_col = st.columns([0.29, 0.70])

# ---------------------------
# Helper: Unique key for file uploader keys based on counter
def get_upload_key():
    return st.session_state.upload_counter

# ---------------------------
# LEFT COLUMN: Jira Input, Fetch Button, and Jira Details (always visible)
# ---------------------------
with left_col:
    st.markdown("<div class='section-heading'>Jira Issue Details</div>", unsafe_allow_html=True)
    # Always show Jira input and fetch button
    jira_key_input = st.text_input("Enter Jira issue key", key="universal_jira_input", value=st.session_state.jira_key)
    if st.button("Fetch Jira details", key="universal_fetch_jira"):
        if jira_key_input:
            # If the Jira key is different from the stored value, reset file uploads.
            if jira_key_input != st.session_state.jira_key:
                st.session_state.upload_counter += 1
                st.session_state.new_logs_files = None
                st.session_state.new_attachments_files = None
            # Simulate fetching Jira details (dummy data)
            st.session_state.jira_details = {
                "description": f"Dummy description for issue {jira_key_input}",
                "logs": [{"name": "dummy_log.txt", "data": "Dummy log content."}],
                "attachments": [{"name": "dummy_attachment.png", "data": b"DummyImageBytes"}]
            }
            st.session_state.jira_key = jira_key_input
            # For the first fetch, move to page 2 (if not already on a page with analysis)
            if st.session_state.page == 1:
                st.session_state.page = 2
            st.rerun()
        else:
            st.error("Please enter a Jira issue key.")
    
    # Always show fetched Jira details (if any) and file uploaders
    if st.session_state.jira_details:
        st.write("**Description:**", st.session_state.jira_details.get("description", "N/A"))
        st.write("**Log Files:**")
        for log in st.session_state.jira_details.get("logs", []):
            st.markdown(f"- {log['name']}")
            st.download_button("Download Log", data=log["data"],
                               file_name=log["name"], mime="text/plain")
        st.write("**Attachments:**")
        for attach in st.session_state.jira_details.get("attachments", []):
            st.markdown(f"- {attach['name']}")
            st.download_button("Download Attachment", data=attach["data"],
                               file_name=attach["name"], mime="application/octet-stream")
        # File uploaders using keys that include the current upload counter
        upload_key = get_upload_key()
        new_logs = st.file_uploader("Upload New Logs (max 15 files)",
                                    accept_multiple_files=True,
                                    key=f"logs_upload_{upload_key}",
                                    type=['txt', 'log'])
        new_attachments = st.file_uploader("Upload New Attachments (max 10 files)",
                                           accept_multiple_files=True,
                                           key=f"attachments_upload_{upload_key}",
                                           type=['png', 'jpg', 'jpeg', 'pdf'])
        # Save uploaded files in session state, preserving already uploaded ones if no new file is selected
        if new_logs is not None and len(new_logs) > 0:
            st.session_state.new_logs_files = new_logs
        else:
            new_logs = st.session_state.get("new_logs_files", None)
        if new_attachments is not None and len(new_attachments) > 0:
            st.session_state.new_attachments_files = new_attachments
        else:
            new_attachments = st.session_state.get("new_attachments_files", None)
        st.session_state.new_logs = new_logs
        st.session_state.new_attachments = new_attachments

# ---------------------------
# RIGHT COLUMN: AI Analysis Section
# ---------------------------
with right_col:
    st.markdown("<div class='section-heading'>AI Analysis</div>", unsafe_allow_html=True)
    
    # Analyze button with validation logic
    st.markdown('<div id="analyze-container">', unsafe_allow_html=True)
    if st.button("Analyze", key="analyze_btn"):
        # Validate: If no Jira key is fetched, display an error.
        if not st.session_state.jira_key:
            st.error("Fetch Jira details with Jira key first.")
        elif not st.session_state.jira_details:
            st.error("Unable to fetch the Jira details.")
        else:
            st.session_state.analysis_result = {
                "summary": "Dummy analysis summary.",
                "root_cause": "Dummy root cause identified.",
                "solution": "Dummy proposed solution."
            }
            # The analysis button may be clicked multiple times;
            # each click will update the analysis_result.
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display analysis result if available; otherwise, display placeholders
    if st.session_state.analysis_result:
        st.markdown("<div class='section-heading'>Summary</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='analysis-box'>{st.session_state.analysis_result.get('summary', '')}</div>",
                    unsafe_allow_html=True)
        st.markdown("<div class='section-heading'>Root Cause</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='analysis-box'>{st.session_state.analysis_result.get('root_cause', '')}</div>",
                    unsafe_allow_html=True)
        st.markdown("<div class='section-heading'>Solution</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='analysis-box'>{st.session_state.analysis_result.get('solution', '')}</div>",
                    unsafe_allow_html=True)
    else:
        st.markdown("<div class='section-heading'>Summary</div>", unsafe_allow_html=True)
        st.markdown("<div class='analysis-box'>*Enter Jira details to get summary*</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-heading'>Root Cause</div>", unsafe_allow_html=True)
        st.markdown("<div class='analysis-box'>*Enter Jira details to get root cause*</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-heading'>Solution</div>", unsafe_allow_html=True)
        st.markdown("<div class='analysis-box'>*Enter Jira details to get solution*</div>", unsafe_allow_html=True)

