from flask import Flask, request, abort, render_template
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import gspread
import os

app = Flask(__name__)

# Google Sheets authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(credentials)

# Open the Google Sheet
sheet = client.open("Attendance Form Responses").sheet1

# List of allowed IP addresses (replace with your lab's IP range)
allowed_ips = ['192.168.1.0', '192.168.1.255']

@app.before_request
def limit_remote_addr():
    if request.remote_addr not in allowed_ips:
        abort(403)  # Forbidden

@app.route('/')
def index():
    return render_template('index.html')

def get_responses():
    responses = sheet.get_all_records()
    return responses

def check_duplicate(student_id, timestamp):
    responses = get_responses()
    current_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    for response in responses:
        response_time = datetime.strptime(response['Timestamp'], '%Y-%m-%d %H:%M:%S')
        if response['Student ID'] == student_id and abs((current_time - response_time).total_seconds()) < 1800:
            return True
    return False

def record_attendance(first_name, last_name, student_id, on_board_code):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if not check_duplicate(student_id, timestamp):
        sheet.append_row([timestamp, first_name, last_name, student_id, on_board_code])
        print("Attendance recorded")
    else:
        print("Duplicate submission detected")

@app.route('/submit', methods=['POST'])
def submit():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    student_id = request.form['student_id']
    on_board_code = request.form['on_board_code']
    record_attendance(first_name, last_name, student_id, on_board_code)
    return "Attendance recorded" if not check_duplicate(student_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')) else "Duplicate submission detected"

if __name__ == '__main__':
    app.run(debug=True)
