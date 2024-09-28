from flask import Blueprint, request, jsonify

dodge_bullet_bp = Blueprint('dodge_bullet', __name__)

# Directions for player movement
MOVES = {
    'u': (-1, 0),  # up
    'd': (1, 0),   # down
    'l': (0, -1),  # left
    'r': (0, 1)    # right
}

# Bullet movement directions
BULLET_MOVES = {
    'u': (-1, 0),  # up
    'd': (1, 0),   # down
    'l': (0, -1),  # left
    'r': (0, 1)    # right
}

# Helper function to check if a move is valid (not towards a bullet)
def is_safe(map_data, player_pos, new_pos):
    rows, cols = len(map_data), len(map_data[0])
    x, y = new_pos
    
    if 0 <= x < rows and 0 <= y < cols:
        # Check if the new position has no bullet
        return map_data[x][y] == '.'
    return False

# Simulate the movement of bullets on the map
def move_bullets(map_data):
    rows, cols = len(map_data), len(map_data[0])
    new_map = [['.' for _ in range(cols)] for _ in range(rows)]
    
    for i in range(rows):
        for j in range(cols):
            if map_data[i][j] in BULLET_MOVES:
                dx, dy = BULLET_MOVES[map_data[i][j]]
                new_x, new_y = i + dx, j + dy
                if 0 <= new_x < rows and 0 <= new_y < cols:
                    new_map[new_x][new_y] = map_data[i][j]
    
    return new_map

# Main logic for the dodge bullet game
@dodge_bullet_bp.route('/dodge', methods=['POST'])
def dodge():
    # Read the raw text input
    map_text = request.data.decode('utf-8').strip()
    map_data = map_text.splitlines()  # Split the text into lines
    
    # Find player position
    player_pos = None
    for i, row in enumerate(map_data):
        for j, cell in enumerate(row):
            if cell == '*':
                player_pos = (i, j)
                break
        if player_pos:
            break
    
    if not player_pos:
        return jsonify({"instructions": None}), 400  # Invalid input, player not found
    
    # Check all possible moves and see if they are safe
    safe_moves = []
    for move, (dx, dy) in MOVES.items():
        new_pos = (player_pos[0] + dx, player_pos[1] + dy)
        
        # Move the bullets
        new_map = move_bullets(map_data)
        
        # Check if the player can safely move to the new position
        if is_safe(new_map, player_pos, new_pos):
            safe_moves.append(move)
    
    # Return the first safe move or null if no safe moves
    if safe_moves:
        return jsonify({"instructions": safe_moves})
    else:
        return jsonify({"instructions": None})
