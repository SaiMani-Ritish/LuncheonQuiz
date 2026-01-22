"""
Google Sheets-based score storage for Streamlit Cloud deployment.
Simple, visual, and works great for 30-40 users.
"""

import streamlit as st
from datetime import datetime, timezone

try:
    import gspread
    from google.oauth2.service_account import Credentials
    GSPREAD_AVAILABLE = True
except ImportError:
    GSPREAD_AVAILABLE = False


# Google Sheets API scopes
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


def init_firebase():
    """
    Initialize Google Sheets connection.
    Returns the worksheet object.
    """
    if not GSPREAD_AVAILABLE:
        st.error("gspread not installed. Run: pip install gspread google-auth")
        st.stop()
    
    try:
        # Load credentials from Streamlit secrets
        creds_dict = dict(st.secrets["GOOGLE_SHEETS"])
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        client = gspread.authorize(creds)
        
        # Open the spreadsheet by name or URL
        spreadsheet_key = st.secrets["SPREADSHEET_ID"]
        sheet = client.open_by_key(spreadsheet_key)
        
        # Get or create the scores worksheet
        try:
            worksheet = sheet.worksheet("scores")
        except gspread.WorksheetNotFound:
            worksheet = sheet.add_worksheet(title="scores", rows=1000, cols=3)
            worksheet.update("A1:C1", [["username", "score", "timestamp"]])
        
        return worksheet
        
    except Exception as e:
        st.error(f"Google Sheets connection failed: {e}")
        st.stop()


def save_score(worksheet, username: str, score: int) -> bool:
    """
    Save a user's score to Google Sheets.
    
    Args:
        worksheet: gspread worksheet object
        username: Player's username
        score: Quiz score
    
    Returns:
        bool: True if save successful
    """
    try:
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        worksheet.append_row([username, score, timestamp])
        return True
    except Exception as e:
        st.error(f"Failed to save score: {e}")
        return False


def get_leaderboard(worksheet, limit: int = 50) -> list:
    """
    Retrieve leaderboard data from Google Sheets.
    
    Args:
        worksheet: gspread worksheet object
        limit: Maximum number of entries to retrieve
    
    Returns:
        list: List of dicts with username, score, timestamp (sorted by score desc)
    """
    try:
        # Get all records (skip header row)
        records = worksheet.get_all_records()
        
        # Sort by score descending
        sorted_records = sorted(records, key=lambda x: -int(x.get("score", 0)))
        
        # Format and limit
        leaderboard = []
        for entry in sorted_records[:limit]:
            leaderboard.append({
                "username": entry.get("username", "Anonymous"),
                "score": int(entry.get("score", 0)),
                "timestamp": entry.get("timestamp", "")
            })
        
        return leaderboard
        
    except Exception as e:
        st.error(f"Failed to load leaderboard: {e}")
        return []


def clear_scores(worksheet) -> bool:
    """
    Clear all scores (reset for new event).
    Keeps the header row.
    
    Returns:
        bool: True if successful
    """
    try:
        # Clear all rows except header
        worksheet.delete_rows(2, worksheet.row_count)
        return True
    except Exception as e:
        st.error(f"Failed to clear scores: {e}")
        return False
