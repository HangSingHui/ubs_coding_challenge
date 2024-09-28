from flask import Blueprint, request, jsonify

digital_colony_bp = Blueprint('digital_colony', __name__)

hashMap = {}

def calculateSignature(num1, num2):
    if num1 == num2:
        return 0  # Signature for the same digits
    return (num1 - num2) if num1 > num2 else (10 - num2 + num1)

@digital_colony_bp.route('/digital-colony', methods=['POST'])
def colony():
    data = request.get_json()
    
    # Validate the input
    if not data or len(data) != 2:
        return jsonify({"error": "Invalid input format"}), 400

    gen10_c, gen50_c = data[0]["colony"], data[1]["colony"]

    def evolve_colony(colony, generations):
        colony_list = list(map(int, colony))  # Convert to a list of integers
        weight = sum(colony_list)
        length = len(colony_list)

        # Precompute signatures for all pairs in the initial colony
        signatures = [hashMap.setdefault((colony_list[j], colony_list[j + 1]), calculateSignature(colony_list[j], colony_list[j + 1])) for j in range(length - 1)]

        for _ in range(10):
            new_colony = []
            for j in range(length - 1):
                new_digit = (signatures[j] + weight) % 10  # Get last digit directly
                new_colony.append(colony_list[j])
                new_colony.append(new_digit)

            new_colony.append(colony_list[-1])  # Append last digit
            colony_list = new_colony
            weight = sum(colony_list)  # Update weight for next generation
            length = len(colony_list)

            # Update signatures for the new colony
            signatures = [hashMap.setdefault((colony_list[j], colony_list[j + 1]), calculateSignature(colony_list[j], colony_list[j + 1])) for j in range(length - 1)]

        return sum(colony_list)

    # Process the required generations and calculate weights
    weight10 = evolve_colony(gen10_c, 10)
    weight50 = evolve_colony(gen50_c, 50)

    # Return the weights as a JSON response
    return jsonify([str(weight10), str(weight50)])