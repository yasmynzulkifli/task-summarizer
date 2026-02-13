import pandas as pd
from datetime import datetime

def normalize_text(val):
    """
    Normalize Excel / smart punctuation and whitespace.
    Converts em dash, en dash, minus sign to regular hyphen.
    """
    if not isinstance(val, str):
        return val

    replacements = {
        '\u2014': '-',  # em dash
        '\u2013': '-',  # en dash
        '\u2212': '-',  # minus sign
        '\u00A0': ' ',  # non-breaking space
        '\u2018': "'",  # left single quote
        '\u2019': "'",  # right single quote
        '\u201C': '"',  # left double quote
        '\u201D': '"',  # right double quote
    }

    for k, v in replacements.items():
        val = val.replace(k, v)

    return val.strip()

def read_file_with_encoding(uploaded_file):
    """Read uploaded file with proper encoding handling"""
    if uploaded_file.name.endswith('.csv'):
        try:
            return pd.read_csv(uploaded_file, encoding='utf-8-sig')
        except UnicodeDecodeError:
            return pd.read_csv(uploaded_file, encoding='cp1252')
    else:
        return pd.read_excel(uploaded_file, header=0)

def determine_color(row):
    """Determine task color based on progress columns"""
    if pd.notna(row['Progress_R']) or pd.notna(row['DueDate_R']):
        return 'red'
    elif pd.notna(row['Progress_Y']) or pd.notna(row['DueDate_Y']):
        return 'yellow'
    else:
        return 'green'

def format_task_line(emoji, row):
    """Format a task line"""
    hotel = row['Hotel']
    task_name = row['Task Name']
    
    detail = ""
    if pd.notna(row['Subtask']) and str(row['Subtask']).strip():
        detail = str(row['Subtask']).replace('\n', ', ')
    elif pd.notna(row['Description']) and str(row['Description']).strip():
        detail = str(row['Description']).replace('\n', ', ')
    
    if detail:
        return f"{emoji} {hotel} | {task_name} — {detail}"
    else:
        return f"{emoji} {hotel} | {task_name}"

def format_progress_line(row, color):
    """Format the progress line"""
    if color == 'red':
        progress = row['Progress_R']
        due_date = row['DueDate_R']
    elif color == 'yellow':
        progress = row['Progress_Y']
        due_date = row['DueDate_Y']
    else:
        progress = row['Progress_G']
        due_date = row['DueDate_G']
    
    if pd.notna(progress):
        if isinstance(progress, float) and progress <= 1:
            progress_str = f"{progress*100:.0f}%"
        else:
            progress_str = str(progress)
    else:
        progress_str = "N/A"
    
    if pd.notna(due_date):
        if isinstance(due_date, datetime):
            due_str = due_date.strftime('%Y-%m-%d')
        else:
            due_str = str(due_date)[:10]
    else:
        due_str = "-"
    
    review = str(row['Review']).replace('\n', ', ') if pd.notna(row['Review']) else ""
    
    return f"   {progress_str} | {due_str}" + (f" | {review}" if review else "")
