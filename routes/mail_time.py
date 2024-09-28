from flask import Blueprint, request, jsonify
from datetime import datetime
from dateutil import parser

mailtime_bp = Blueprint('mailtime', __name__)

def parse_email_time(time_string):
    # Parse ISO 8601 time string into datetime object
    return parser.parse(time_string)

@mailtime_bp.route('/mailtime', methods=['POST'])
def mailtime():
    data = request.get_json()
    emails = data['emails']
    users = data['users']
    
    # Create a dictionary to hold total response times and number of responses
    response_times = {user['name']: {'total_time': 0, 'responses': 0} for user in users}
    
    # Sort emails based on their timestamps
    emails.sort(key=lambda email: parse_email_time(email['timeSent']))
    
    # Traverse through the emails and calculate response times
    for i in range(1, len(emails)):
        prev_email = emails[i - 1]
        curr_email = emails[i]
        
        # Ensure that the current email is a reply in the same thread
        if curr_email['subject'].startswith('RE:') and curr_email['subject'][4:] == prev_email['subject']:
            # Calculate the time difference in seconds between emails
            prev_time = parse_email_time(prev_email['timeSent'])
            curr_time = parse_email_time(curr_email['timeSent'])
            time_diff = (curr_time - prev_time).total_seconds()
            
            # Update response times for the sender of the current email
            sender = curr_email['sender']
            response_times[sender]['total_time'] += time_diff
            response_times[sender]['responses'] += 1
    
    # Calculate the average response time for each user
    averages = {}
    for user, times in response_times.items():
        if times['responses'] > 0:
            averages[user] = round(times['total_time'] / times['responses'])
        else:
            averages[user] = 0  # No responses
    
    return jsonify({"response": averages})
