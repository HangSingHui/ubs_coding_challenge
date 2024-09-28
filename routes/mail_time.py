from flask import Blueprint, request, jsonify
from datetime import datetime
from dateutil import parser
import pytz
from collections import defaultdict

mailtime_bp = Blueprint('mailtime', __name__)

# Time converter
def convert_to_singapore_time(email_data):
    singapore_tz = pytz.timezone("Asia/Singapore")
    user_timezones = {user["name"]: user["officeHours"]["timeZone"] for user in email_data["users"]}

    for email in email_data["emails"]:
        sender = email["sender"]
        sender_timezone = user_timezones[sender]
        original_time = parser.parse(email["timeSent"]).astimezone(pytz.timezone(sender_timezone))
        singapore_time = original_time.astimezone(singapore_tz)
        email["timeSentInSingapore"] = singapore_time.isoformat()

    return email_data

def group_emails(email_data):
    response_times = defaultdict(list)
    user_timezones = {user["name"]: user["officeHours"]["timeZone"] for user in email_data["users"]}

    for email in email_data["emails"]:
        subject = email["subject"]
        sender = email["sender"]
        receiver = email["receiver"]

        if subject.startswith("RE:"):
            original_subject = subject[4:].strip()  # Remove the "RE: " prefix and strip spaces

            # Check for matching original emails
            for orig_email in email_data["emails"]:
                # Ensure we match against the original subject and the correct sender and receiver
                if orig_email["subject"] == original_subject and orig_email["receiver"] == sender and orig_email["sender"] == receiver:
                    # Convert times to Singapore time
                    orig_time_sender = parser.parse(orig_email["timeSent"])
                    reply_time_sender = parser.parse(email["timeSent"])

                    # Time in the timezone of the original sender
                    orig_time_sender_local = orig_time_sender.astimezone(pytz.timezone(user_timezones[receiver]))
                    # Time in the timezone of the current sender
                    reply_time_receiver_local = reply_time_sender.astimezone(pytz.timezone(user_timezones[sender]))

                    # Calculate response time in seconds
                    response_time = (reply_time_receiver_local - orig_time_sender_local).total_seconds()
                    response_times[sender].append(response_time)

                    break  # Exit the loop after finding the match

    # Calculate average response times
    average_response_times = {}
    for user, times in response_times.items():
        if times:  # Avoid division by zero
            average_response_times[user] = sum(times) // len(times)  # Calculate average
        else:
            average_response_times[user] = 0  # No responses

    return {"averageResponseTimes": average_response_times}

@mailtime_bp.route('/mailtime', methods=['POST'])
def mailtime():
    data = request.get_json()
    
    # Convert email timestamps to Singapore time
    convert_to_singapore_time(data)
    
    # Group emails into threads and calculate averages
    averages = group_emails(data)

    # Prepare the final response format
    response = {
        "response": averages["averageResponseTimes"]
    }
    
    return jsonify(response)
