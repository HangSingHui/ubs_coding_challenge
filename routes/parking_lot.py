from flask import Blueprint, request, jsonify

parking_lot_bp = Blueprint('parking_lot', __name__)

# Helper function to check parking and exiting logic
def process_vehicle_action(parking_lot, vehicle, action):
    plate_number = vehicle["plateNumber"]
    length = vehicle["length"]
    width = vehicle["width"]
    direction = None
    x = y = None
    
    # Logic to determine whether the action should be executed (park/exit)
    execute = True
    # Example: You can add validation logic for parking/exiting positions here

    # If it's a "park" action, assign position and direction
    if action == "park":
        # Example: Assign a parking spot (placeholder, needs logic for parking spot determination)
        x, y, direction = 1, 1, "SOUTH"  # This is just a placeholder
    elif action == "exit":
        # Example: Assign an exit point (placeholder, needs logic for exiting)
        x, y, direction = 4, 4, "EAST"  # This is just a placeholder
    
    # If not valid, set execute to False and position to None
    if not execute:
        return {"plateNumber": plate_number, "action": action, "execute": False, "position": None}
    
    # Otherwise, return the valid action with position
    return {
        "plateNumber": plate_number,
        "action": action,
        "execute": True,
        "position": {
            "x": x,
            "y": y,
            "direction": direction
        }
    }

@parking_lot_bp.route('/parkinglot', methods=['POST'])
def parking_lot():
    data = request.get_json()
    result = []
    
    for case in data:
        minimum_total_fare = case['minimumTotalFare']
        vehicles = case['vehicles']
        actions = case['actions']
        parking_lot_map = case['parkingLot']

        vehicle_actions = []
        total_fare = 0

        # Process each action
        for action in actions:
            vehicle = next(v for v in vehicles if v["plateNumber"] == action["plateNumber"])
            action_type = action["action"]
            vehicle_action_result = process_vehicle_action(parking_lot_map, vehicle, action_type)
            
            if vehicle_action_result["execute"] and action_type == "exit":
                total_fare += vehicle["parkingFare"]
            
            vehicle_actions.append(vehicle_action_result)
        
        # Check if the total fare meets the minimum requirement
        if total_fare < minimum_total_fare:
            for vehicle_action in vehicle_actions:
                vehicle_action["execute"] = False
                vehicle_action["position"] = None
        
        result.append({
            "actions": vehicle_actions
        })
    
    return jsonify(result)
