import streamlit as st
import pandas as pd
from utils.auth import check_password
from utils.data_processing import determine_color, format_task_line, format_progress_line

st.set_page_config(
    page_title="All Tasks",
    page_icon="👥",
    layout="wide"
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
    
    # File info
    if 'df' in st.session_state:
        st.success("✅ File loaded")
        st.caption(f"Total rows: {len(st.session_state['df'])}")
    else:
        st.warning("⚠️ No file uploaded")
        st.info("👈 Go to Home to upload")
    
    st.markdown("---")
    
    if st.button("🚪 Logout", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Main content
st.title("👥 All Tasks by Assignee")

if 'df' not in st.session_state:
    st.warning("⚠️ Please upload a file first!")
    st.info("👈 Go to 'Home' page in the sidebar to upload your file")
    st.stop()

df = st.session_state['df']

# Group by Assignee
grouped = df.groupby('Assignee')

st.markdown(f"### Found {len(grouped)} assignees")
st.markdown("---")

# Create tabs for each assignee
assignees = sorted(grouped.groups.keys())
tabs = st.tabs(assignees)

for tab, assignee in zip(tabs, assignees):
    with tab:
        group = grouped.get_group(assignee)
        
        # Generate formatted output
        output_lines = []
        output_lines.append(f"Attention to {assignee}:\n")
        
        # Task on Hold
        hold_tasks = group[group['Status'].str.lower().str.contains('hold', na=False)]
        if not hold_tasks.empty:
            output_lines.append("*Task on Hold*")
            for _, row in hold_tasks.iterrows():
                task_line = format_task_line('👀', row)
                output_lines.append(task_line)
            output_lines.append("")
        
        # Active Tasks
        active_statuses = ['on going', 'to do', 'awaiting', 'new']
        active_tasks = group[group['Status'].str.lower().str.contains('|'.join(active_statuses), na=False)]
        
        red_tasks = []
        yellow_tasks = []
        green_tasks = []
        
        if not active_tasks.empty:
            output_lines.append("*Task*")
            
            for _, row in active_tasks.iterrows():
                color = determine_color(row)
                if color == 'red':
                    red_tasks.append(row)
                elif color == 'yellow':
                    yellow_tasks.append(row)
                else:
                    green_tasks.append(row)
            
            for row in red_tasks:
                task_line = format_task_line('🔴', row)
                output_lines.append(task_line)
                progress_line = format_progress_line(row, 'red')
                output_lines.append(progress_line)
            
            for row in yellow_tasks:
                task_line = format_task_line('🟡', row)
                output_lines.append(task_line)
                progress_line = format_progress_line(row, 'yellow')
                output_lines.append(progress_line)
            
            for row in green_tasks:
                task_line = format_task_line('🟢', row)
                output_lines.append(task_line)
                progress_line = format_progress_line(row, 'green')
                output_lines.append(progress_line)
            
            output_lines.append("")
        
        # Cancelled
        cancelled_tasks = group[group['Status'].str.lower().str.contains('cancel', na=False)]
        if not cancelled_tasks.empty:
            output_lines.append("*Cancelled*")
            for _, row in cancelled_tasks.iterrows():
                hotel = row['Hotel']
                task_name = row['Task Name']
                output_lines.append(f"🚫 {hotel} | {task_name}")
            output_lines.append("")
        
        # Transferred
        transferred_tasks = group[group['Status'].str.lower().str.contains('transf', na=False)]
        if not transferred_tasks.empty:
            output_lines.append("*Transferred*")
            for _, row in transferred_tasks.iterrows():
                hotel = row['Hotel']
                task_name = row['Task Name']
                output_lines.append(f"➡️ {hotel} | {task_name}")
            output_lines.append("")
        
        # Completed
        completed_tasks = group[group['Status'].str.lower().str.contains('complete', na=False)]
        if not completed_tasks.empty:
            output_lines.append("*Completed*")
            for _, row in completed_tasks.iterrows():
                hotel = row['Hotel']
                task_name = row['Task Name']
                output_lines.append(f"⭐ {hotel} | {task_name}")
            output_lines.append("")
        
        # Display
        formatted_output = "\n".join(output_lines)
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🔴 Red Tasks", len(red_tasks))
        with col2:
            st.metric("🟡 Yellow Tasks", len(yellow_tasks))
        with col3:
            st.metric("🟢 Green Tasks", len(green_tasks))
        with col4:
            st.metric("⭐ Completed", len(completed_tasks))
        
        st.markdown("---")
        
        # Copy button
        if st.button(f"📋 Copy {assignee}'s Tasks", key=f"copy_{assignee}"):
            st.code(formatted_output, language=None)
            st.success("✅ Text ready to copy! Select and copy from the box above.")
        
        # Show in expander
        with st.expander(f"👁️ View {assignee}'s Tasks", expanded=False):
            st.code(formatted_output, language=None)
