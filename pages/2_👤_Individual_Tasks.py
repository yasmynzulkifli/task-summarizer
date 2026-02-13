import streamlit as st
import pandas as pd
from utils.auth import check_password
from utils.data_processing import determine_color, format_task_line, format_progress_line, normalize_text, read_file_with_encoding

st.set_page_config(
    page_title="Individual Tasks",
    page_icon="👤",
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
st.title("👤 Individual Tasks by Hotel")

if 'df' not in st.session_state:
    st.warning("⚠️ Please upload a file first!")
    st.info("👈 Go to 'Home' page in the sidebar to upload your file")
    st.stop()

df = st.session_state['df']

# Select assignee
assignees = sorted(df['Assignee'].dropna().unique())
selected_assignee = st.selectbox("Select Assignee", assignees, key="assignee_selector")

if selected_assignee:
    st.markdown("---")
    
    # Filter for selected assignee
    assignee_df = df[df['Assignee'] == selected_assignee]
    
    # Filter for active tasks only
    active_statuses = ['hold', 'on going', 'to do', 'awaiting', 'new']
    active_df = assignee_df[assignee_df['Status'].str.lower().str.contains('|'.join(active_statuses), na=False)]
    
    # Expand rows with multiple hotels
    expanded_rows = []
    for _, row in active_df.iterrows():
        hotel_str = str(row['Hotel'])
        hotels = [h.strip() for h in hotel_str.replace('/', ',').replace('|', ',').split(',')]
        
        for hotel in hotels:
            if hotel:
                row_copy = row.copy()
                row_copy['Hotel'] = hotel
                expanded_rows.append(row_copy)
    
    if not expanded_rows:
        st.info(f"No active tasks found for {selected_assignee}")
        st.stop()
    
    expanded_df = pd.DataFrame(expanded_rows)
    
    # Group by hotel
    hotel_groups = expanded_df.groupby('Hotel')
    
    st.markdown(f"### {selected_assignee}'s Tasks by Hotel ({len(hotel_groups)} hotels)")
    st.markdown("---")
    
    # Collect all hotel tasks for "Copy All" button
    all_hotel_outputs = []
    
    # Display in grid
    hotels = sorted(hotel_groups.groups.keys())
    cols_per_row = 2
    
    for i in range(0, len(hotels), cols_per_row):
        cols = st.columns(cols_per_row)
        
        for j, hotel in enumerate(hotels[i:i+cols_per_row]):
            with cols[j]:
                group = hotel_groups.get_group(hotel)
                
                # Create hotel card
                st.markdown(f"#### 🏨 {hotel}")
                
                # Generate formatted output
                output_lines = []
                
                # Separate hold and active
                hold_tasks = group[group['Status'].str.lower().str.contains('hold', na=False)]
                non_hold_tasks = group[~group['Status'].str.lower().str.contains('hold', na=False)]
                
                # Task on Hold
                if not hold_tasks.empty:
                    output_lines.append("*Task on Hold*")
                    for _, row in hold_tasks.iterrows():
                        output_lines.append(format_task_line('👀', row))
                    output_lines.append("")
                
                # Active tasks by color
                if not non_hold_tasks.empty:
                    red_tasks = []
                    yellow_tasks = []
                    green_tasks = []
                    
                    for _, row in non_hold_tasks.iterrows():
                        color = determine_color(row)
                        if color == 'red':
                            red_tasks.append(row)
                        elif color == 'yellow':
                            yellow_tasks.append(row)
                        else:
                            green_tasks.append(row)
                    
                    for row in red_tasks:
                        output_lines.append(format_task_line('🔴', row))
                        output_lines.append(format_progress_line(row, 'red'))
                    
                    for row in yellow_tasks:
                        output_lines.append(format_task_line('🟡', row))
                        output_lines.append(format_progress_line(row, 'yellow'))
                    
                    for row in green_tasks:
                        output_lines.append(format_task_line('🟢', row))
                        output_lines.append(format_progress_line(row, 'green'))
                
                formatted_output = "\n".join(output_lines)
                
                # Store for "Copy All"
                all_hotel_outputs.append(f"*{hotel}*\n{formatted_output}")
                
                # Task count
                task_count = len(group)
                st.caption(f"{task_count} task{'s' if task_count > 1 else ''}")
                
                # Show tasks
                with st.expander("👁️ View Tasks", expanded=True):
                    st.code(formatted_output, language=None)
                
                # Copy button
                if st.button(f"📋 Copy", key=f"copy_hotel_{hotel}", use_container_width=True):
                    st.code(formatted_output, language=None)
                    st.success("✅ Ready to copy!")
                
                st.markdown("---")
    
    # Copy All button at the top
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("📋 Copy All Hotels", use_container_width=True):
            all_output = "\n\n".join(all_hotel_outputs)
            st.code(all_output, language=None)
            st.success("✅ All hotel tasks ready to copy!")
