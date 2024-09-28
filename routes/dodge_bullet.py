from flask import Blueprint, request, jsonify

dodge_bullet_bp = Blueprint('dodge_bullet', __name__)


# Main logic for the dodge bullet game
@dodge_bullet_bp.route('/dodge', methods=['POST'])
def dodge():
    # Read the raw text input
    map_text = request.data.decode('utf-8').strip()
    map_data = map_text.splitlines()  # Split the text into lines

    for i, data in enumerate(map_data):
        print(i, data)
    
    #Cannot be in the same column and up and down
    #cannot be in the same row as left or right
    
