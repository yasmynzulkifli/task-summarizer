import streamlit as st
import pandas as pd
from datetime import datetime
from utils.auth import check_password
from utils.data_processing import normalize_text, read_file_with_encoding

# Must be the first Streamlit command
st.set_page_config(
    page_title="Task Manager",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check authentication
if not check_password():
    st.stop()

# Get username
username = st.session_state.get("user", "User")

# Sidebar
with st.sidebar:
    st.title("📋 Task Manager")
    st.markdown(f"### Hi, {username}! 👋")
    st.markdown("---")
    
    # File info if uploaded
    if 'df' in st.session_state:
        st.success("✅ File loaded")
        st.caption(f"Total rows: {len(st.session_state['df'])}")
        st.caption(f"Uploaded: {st.session_state.get('upload_time', 'N/A')}")
    else:
        st.info("👆 Upload a file to get started")
    
    st.markdown("---")
    
    if st.button("🚪 Logout", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Main content - Upload page
st.title("📤 Upload Task File")
st.markdown("Upload your CSV or Excel file to get started")
st.markdown("---")

uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=['csv', 'xlsx', 'xls'],
    help="Upload your task management file"
)

if uploaded_file is not None:
    try:
        with st.spinner("Processing file..."):
            # Read file
            df = read_file_with_encoding(uploaded_file)
            
            # Normalize all text cells
            df = df.applymap(normalize_text)
            
            # Rename columns
            if len(df.columns) == 14:
                df.columns = ['Assignee', 'Hotel', 'Task Name', 'Subtask', 'Description', 
                              'Status', 'Priority', 'Progress_G', 'DueDate_G', 
                              'Progress_Y', 'DueDate_Y', 'Progress_R', 'DueDate_R', 'Review']
            else:
                df.columns = ['Assignee', 'Hotel', 'Task Name', 'Subtask', 'Description', 
                              'Status', 'Priority', 'Progress_G', 'DueDate_G', 
                              'Progress_Y', 'DueDate_Y', 'Progress_R', 'DueDate_R', 
                              'Review', 'Dependencies']
            
            # Replace blank Hotel with "General"
            df['Hotel'] = df['Hotel'].fillna('General').replace('', 'General')
            
            # Store in session state
            st.session_state['df'] = df
            st.session_state['upload_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            st.success(f"✅ File uploaded successfully! Found {len(df)} tasks")
            
            # Show preview
            st.markdown("### 📊 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Show assignees
            assignees = df['Assignee'].dropna().unique()
            st.markdown(f"### 👥 Assignees Found: {len(assignees)}")
            cols = st.columns(4)
            for idx, assignee in enumerate(sorted(assignees)):
                with cols[idx % 4]:
                    count = len(df[df['Assignee'] == assignee])
                    st.metric(assignee, f"{count} tasks")
            
            st.info("👈 Now go to 'All Tasks' or 'Individual Tasks' pages from the sidebar!")
    
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        st.exception(e)
else:
    # Show instructions
    st.info("👆 Please upload a file to continue")
    
    with st.expander("📝 File Format Requirements"):
        st.markdown("""
        Your file should contain the following columns:
        - Assignee
        - Hotel
        - Task Name
        - Subtask
        - Description
        - Status
        - Priority
        - Progress (G/Y/R)
        - Due Date (G/Y/R)
        - Review
        - Dependencies (optional)
        """)
