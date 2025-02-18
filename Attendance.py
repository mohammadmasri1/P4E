import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import pandas as pd

# Google Sheets authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(credentials)

# Open the Google Sheet
sheet = client.open("Attendance Form Responses").sheet1

def get_responses():
    # Fetch all responses
    responses = sheet.get_all_records()
    return responses

def check_duplicate(student_id, on_board_code, timestamp):
    responses = get_responses()
    current_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    for response in responses:
        response_time = datetime.strptime(response['Timestamp'], '%Y-%m-%d %H:%M:%S')
        if response['Student ID'] == student_id and abs((current_time - response_time).total_seconds()) < 1800:
            return True
    return False

def record_attendance(first_name, last_name, student_id, on_board_code):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if not check_duplicate(student_id, on_board_code, timestamp):
        # Add the new response to the sheet
        sheet.append_row([timestamp, first_name, last_name, student_id, on_board_code])
        print("Attendance recorded")
    else:
        print("Duplicate submission detected")

# Example usage
first_name = "John"
last_name = "Doe"
student_id = "123456"
on_board_code = "ABC123"
record_attendance(first_name, last_name, student_id, on_board_code)
