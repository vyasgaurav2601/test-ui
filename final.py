import streamlit as st

# Set full page width
st.set_page_config(layout="wide")

# ---------------------------
# SESSION STATE
# ---------------------------
if 'page' not in st.session_state:
    st.session_state.page = 1  # 1 = initial, 2 = details fetched, 3 = analysis results
if 'jira_details' not in st.session_state:
    st.session_state.jira_details = {}
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = {}
if 'jira_key' not in st.session_state:
    st.session_state.jira_key = ""

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
    /* Analyze button override: 36px font size, 36px line-height, normal weight, forced min-height */
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
# BANNER
# ---------------------------
st.markdown('<div class="banner">Virtual On-Call Engineer</div>', unsafe_allow_html=True)

# ---------------------------
# LAYOUT: Left column (0.29) and Right column (0.70)
# ---------------------------
col_left, col_right = st.columns([0.29, 0.70])

# ---------------------------
# PAGE 1: INITIAL UI
# ---------------------------
if st.session_state.page == 1:
    with col_left:
        st.markdown("<div class='section-heading'>Jira Issue Details</div>", unsafe_allow_html=True)
        jira_key = st.text_input("Enter Jira issue key", key="jira_key_input_standalone")
        if st.button("Fetch Jira details", key="fetch_jira_standalone"):
            if jira_key:
                # Simulate fetching Jira data with dummy info
                st.session_state.jira_details = {
                    "description": f"Dummy description for issue {jira_key}",
                    "logs": [{"name": "dummy_log.txt", "data": "Dummy log content."}],
                    "attachments": [{"name": "dummy_attachment.png", "data": b"DummyImageBytes"}]
                }
                st.session_state.jira_key = jira_key
                st.session_state.page = 2
                st.rerun()
            else:
                st.error("Please enter a Jira issue key.")
    with col_right:
        st.markdown("<div class='section-heading'>AI Analysis</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-heading'>Summary</div>", unsafe_allow_html=True)
        st.markdown("<div class='analysis-box'>*Enter Jira details to get summary*</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-heading'>Root Cause</div>", unsafe_allow_html=True)
        st.markdown("<div class='analysis-box'>*Enter Jira details to get root cause*</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-heading'>Solution</div>", unsafe_allow_html=True)
        st.markdown("<div class='analysis-box'>*Enter Jira details to get solution*</div>", unsafe_allow_html=True)

# ---------------------------
# PAGE 2: AFTER FETCHING DETAILS
# ---------------------------
elif st.session_state.page == 2:
    with col_left:
        st.markdown("<div class='section-heading'>Jira Issue Details</div>", unsafe_allow_html=True)
        if st.session_state.jira_details:
            st.write("**Description:**", st.session_state.jira_details.get("description"))
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
        new_logs = st.file_uploader("Upload New Logs (max 15 files)",
                                    accept_multiple_files=True,
                                    key="logs_standalone_page2",
                                    type=['txt', 'log'])
        new_attachments = st.file_uploader("Upload New Attachments (max 10 files)",
                                           accept_multiple_files=True,
                                           key="attachments_standalone_page2",
                                           type=['png', 'jpg', 'jpeg', 'pdf'])
        st.session_state.new_logs = new_logs
        st.session_state.new_attachments = new_attachments

    with col_right:
        st.markdown("<div class='section-heading'>AI Analysis</div>", unsafe_allow_html=True)
        st.markdown('<div id="analyze-container">', unsafe_allow_html=True)
        if st.button("Analyze", key="analyze_btn_page2_standalone"):
            st.session_state.analysis_result = {
                "summary": "Dummy analysis summary.",
                "root_cause": "Dummy root cause identified.",
                "solution": "Dummy proposed solution."
            }
            st.session_state.page = 3
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        if not st.session_state.analysis_result:
            st.markdown("<div class='section-heading'>Summary</div>", unsafe_allow_html=True)
            st.markdown("<div class='analysis-box'>*Enter Jira details to get summary*</div>", unsafe_allow_html=True)
            st.markdown("<div class='section-heading'>Root Cause</div>", unsafe_allow_html=True)
            st.markdown("<div class='analysis-box'>*Enter Jira details to get root cause*</div>", unsafe_allow_html=True)
            st.markdown("<div class='section-heading'>Solution</div>", unsafe_allow_html=True)
            st.markdown("<div class='analysis-box'>*Enter Jira details to get solution*</div>", unsafe_allow_html=True)

# ---------------------------
# PAGE 3: ANALYSIS RESULTS
# ---------------------------
elif st.session_state.page == 3:
    with col_left:
        st.markdown("<div class='section-heading'>Jira Issue Details</div>", unsafe_allow_html=True)
        new_jira_key = st.text_input("Enter new Jira issue key (or leave blank to keep current)",
                                     key="jira_key_page3_standalone",
                                     value=st.session_state.jira_key)
        if st.button("Fetch Jira details", key="fetch_jira_page3_standalone"):
            if new_jira_key:
                st.session_state.jira_details = {
                    "description": f"Dummy description for issue {new_jira_key}",
                    "logs": [{"name": "dummy_log.txt", "data": "Dummy log content."}],
                    "attachments": [{"name": "dummy_attachment.png", "data": b"DummyImageBytes"}]
                }
                st.session_state.jira_key = new_jira_key
            else:
                st.error("Please enter a Jira issue key.")
        if st.session_state.jira_details:
            st.write("**Description:**", st.session_state.jira_details.get("description"))
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
        new_logs = st.file_uploader("Upload New Logs (max 15 files)",
                                    accept_multiple_files=True,
                                    key="logs_standalone_page3",
                                    type=['txt', 'log'])
        new_attachments = st.file_uploader("Upload New Attachments (max 10 files)",
                                           accept_multiple_files=True,
                                           key="attachments_standalone_page3",
                                           type=['png', 'jpg', 'jpeg', 'pdf'])
        st.session_state.new_logs = new_logs
        st.session_state.new_attachments = new_attachments

    with col_right:
        st.markdown("<div class='section-heading'>AI Analysis</div>", unsafe_allow_html=True)
        st.markdown('<div id="analyze-container">', unsafe_allow_html=True)
        if st.button("Analyze", key="analyze_btn_page3_standalone"):
            st.session_state.analysis_result = {
                "summary": "Dummy analysis summary (re-run).",
                "root_cause": "Dummy root cause identified (re-run).",
                "solution": "Dummy proposed solution (re-run)."
            }
            st.session_state.page = 3
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
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

