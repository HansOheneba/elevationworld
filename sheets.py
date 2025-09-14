import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime


def get_sheets_service():
    """Build credentials from environment variables for Vercel"""
    try:
        # Create credentials dict from environment variables
        creds_dict = {
            "type": os.environ.get("GOOGLE_TYPE"),
            "project_id": os.environ.get("GOOGLE_PROJECT_ID"),
            "private_key_id": os.environ.get("GOOGLE_PRIVATE_KEY_ID"),
            "private_key": os.environ.get("GOOGLE_PRIVATE_KEY", "").replace(
                "\\n", "\n"
            ),
            "client_email": os.environ.get("GOOGLE_CLIENT_EMAIL"),
            "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
            "auth_uri": os.environ.get("GOOGLE_AUTH_URI"),
            "token_uri": os.environ.get("GOOGLE_TOKEN_URI"),
        }

        creds = service_account.Credentials.from_service_account_info(
            creds_dict, scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )

        service = build("sheets", "v4", credentials=creds)
        return service

    except Exception as e:
        print(f"Error authenticating: {e}")
        return None


def append_to_sheet(range_name, values):
    """Append data to a Google Sheet"""
    try:
        service = get_sheets_service()
        if not service:
            return False

        spreadsheet_id = os.environ.get("GOOGLE_SHEET_ID")
        if not spreadsheet_id:
            print("Spreadsheet ID not found in environment variables")
            return False

        body = {"values": values}
        result = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )

        print(f"Appended {result.get('updates').get('updatedCells')} cells")
        return True

    except HttpError as error:
        print(f"An error occurred: {error}")
        return False


# ADD THIS NEW FUNCTION FOR REGISTRATION SPECIFICALLY
def append_registration(data):
    """Helper function specifically for registration form"""
    # Prepare the data in the right order for Google Sheets
    values = [
        [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Timestamp
            data.get("email", ""),
            data.get("firstname", ""),
            data.get("lastname", ""),
            data.get("phonenumber", ""),
            data.get("gender", ""),
            data.get("age_bracket", ""),
            data.get("occupation", ""),
        ]
    ]

    # Append to sheet (8 columns: A to H)
    return append_to_sheet("Sheet1!A:H", values)
