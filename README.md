# Task Manager - Streamlit Web Application

## 🎯 Overview
A web-based task management system that organizes tasks by assignee and hotel. Converted from CustomTkinter desktop app to Streamlit web application.

## ✨ Features
- 🔐 **Password Authentication** - Secure login for Yasmin and Aidil
- 📤 **File Upload** - Support for CSV and Excel files
- 👥 **All Tasks View** - See all tasks grouped by assignee
- 👤 **Individual Tasks** - View tasks by assignee and hotel
- 📋 **Copy to Clipboard** - Easy copy functionality for WhatsApp sharing
- 🎨 **Clean UI** - Modern, responsive design

## 👤 User Credentials

| Username | Password |
|----------|----------|
| yasmin   | ######   |
| aidil    | ######## |

## 🚀 Quick Start

## 📖 How to Use

### Step 1: Login
- Enter username: `yasmin` or `aidil`
- Enter corresponding password
- Click "Login"

### Step 2: Upload File
1. Click "Upload File" in sidebar
2. Drag and drop or browse for your CSV/Excel file
3. Wait for processing
4. Preview the data

### Step 3: View Tasks

#### Option A: All Tasks by Assignee
1. Click "All Tasks" in sidebar
2. Use tabs to switch between assignees
3. View task metrics (Red/Yellow/Green/Completed)
4. Click "Copy" to get formatted text for WhatsApp

#### Option B: Individual Tasks by Hotel
1. Click "Individual Tasks" in sidebar
2. Select an assignee from dropdown
3. View tasks organized by hotel
4. Copy individual hotel tasks or all tasks

### Step 4: Copy for WhatsApp
- Click any "Copy" button
- The formatted text will appear in a code box
- Select all text (Ctrl+A or Cmd+A)
- Copy (Ctrl+C or Cmd+C)
- Paste into WhatsApp

## 📁 File Format

Your CSV/Excel file should have these columns:

| Column | Description |
|--------|-------------|
| Assignee | Person assigned to task |
| Hotel | Hotel name (can be multiple, separated by comma/slash) |
| Task Name | Name of the task |
| Subtask | Subtask details |
| Description | Task description |
| Status | Task status (On Going, To Do, Hold, Completed, etc.) |
| Priority | Priority level |
| Progress (G) | Green progress |
| Due Date (G) | Green due date |
| Progress (Y) | Yellow progress |
| Due Date (Y) | Yellow due date |
| Progress (R) | Red progress |
| Due Date (R) | Red due date |
| Review | Review notes |
| Dependencies | (Optional) Task dependencies |

## 🎨 Task Color Coding

- 🔴 **Red Tasks** - High priority / Urgent (has red progress or due date)
- 🟡 **Yellow Tasks** - Medium priority (has yellow progress or due date)
- 🟢 **Green Tasks** - Normal priority (has only green progress or due date)
- 👀 **On Hold** - Tasks marked as "Hold" status
- ⭐ **Completed** - Finished tasks
- 🚫 **Cancelled** - Cancelled tasks
- ➡️ **Transferred** - Transferred tasks

## 🔧 Troubleshooting

### Issue: File won't upload
- **Solution**: Make sure file is CSV or Excel (.xlsx, .xls)
- Check file isn't corrupted
- Try re-downloading the original file

### Issue: Login not working
- **Solution**: Check username and password (case-sensitive)
- Make sure no extra spaces
- Try typing instead of copy-paste

### Issue: Tasks not showing correctly
- **Solution**: Verify file has all required columns
- Check for empty or missing data
- Review file format requirements above

### Issue: Can't copy text
- **Solution**: Click "Copy" button first
- Text will appear in code box
- Manually select and copy (Ctrl+A, Ctrl+C)

## 📱 Mobile Support

The app works on mobile devices! Access the same URL from your phone or tablet.

## 🔒 Security Notes

- Passwords are NOT stored in the app
- Each session is independent
- Click "Logout" when done
- Don't share your login credentials

## 💡 Tips

1. **Upload once, view many ways** - No need to re-upload for different views
2. **Use tabs efficiently** - In "All Tasks", tabs let you quickly switch assignees
3. **Hotel grouping** - "Individual Tasks" shows tasks by hotel for better organization
4. **Regular updates** - Upload new CSV files as tasks change
5. **Bookmark the app** - Save the URL for quick access

## 🆘 Support

If you need help:
1. Check the Troubleshooting section above
2. Contact your system administrator
3. Refer to this README file

## 📝 Version History

### Version 1.0 (Current)
- Initial Streamlit conversion
- Password authentication
- Three main pages: Upload, All Tasks, Individual Tasks
- Copy to clipboard functionality
- Mobile responsive design

## 🙏 Credits

Converted from CustomTkinter desktop application to Streamlit web application.

---

Made with ❤️ for efficient task management
