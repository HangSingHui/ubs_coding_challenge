from flask import Blueprint, request, jsonify

efficient_hunter_bp = Blueprint('efficient_hunter_kazuma', __name__)

@efficient_hunter_bp.route('/efficient-hunter-kazuma', methods=['POST'])
def efficient_hunter_kazuma():
    data = request.get_json()

    result = []
    
    for case in data:
        monsters = case['monsters']
        efficiency = calculate_efficiency(monsters)
        result.append({"efficiency": efficiency})

    return jsonify(result)

def calculate_efficiency(monsters):
    n = len(monsters)
    efficiency = 0
    i = 0

    while i < n:
        # Check if current time frame has enough monsters to make attacking worthwhile
        if monsters[i] > 0:
            # Calculate total monsters that will be defeated in this attack
            monsters_defeated = monsters[i]
            # Add to efficiency: monsters defeated minus 1 (for hiring adventurers)
            efficiency += monsters_defeated - 1
            # Skip the next time frame for recovery
            i += 2
        else:
            # Move to the next time frame without attacking
            i += 1

    return efficiency
