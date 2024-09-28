from flask import Blueprint, request, jsonify

digital_colony_bp = Blueprint('digital_colony', __name__)

hashMap = {}

def calculateSignature(pair):
    num1, num2 = int(pair[0]), int(pair[1])
    if num1 >= num2:
        sig = num1 - num2
    else:
        sig = 10 - num2 + num1
    
    # Store the signature in the hashmap for future reference
    hashMap[(pair[0], pair[1])] = sig
    return sig

@digital_colony_bp.route('/digital-colony', methods=['POST'])
def colony():
    data = request.get_json()
    
    # Validate the input
    if not data or len(data) != 2:
        return jsonify({"error": "Invalid input format"}), 400

    gen10_c, gen50_c = data[0]["colony"], data[1]["colony"]
    gen10_i, gen50_i = data[0]["generations"], data[1]["generations"]

    # Function to evolve the colony and calculate weight
    def evolve_colony(colony, generations):
        weight = sum(int(n) for n in colony)
        for _ in range(generations):
            new_list = []
            new_weight = 0
            
            for j in range(len(colony)):
                if j == len(colony) - 1:  # Last number, just add it
                    new_list.append(colony[j])
                    break
                
                # Check if the pairs are already in the hashmap
                if (colony[j], colony[j + 1]) not in hashMap:
                    sig = calculateSignature((colony[j], colony[j + 1]))
                else:
                    sig = hashMap[(colony[j], colony[j + 1])]
                
                # Calculate new value and append to new_list
                new_value = str(sig + weight)[-1]
                new_list.append(colony[j])
                new_list.append(new_value)
            
            # Update the colony and the weight for the next iteration
            colony = ''.join(new_list)  # Convert list back to string
            new_weight = sum(int(n) for n in colony)
            weight = new_weight  # Update weight for the next generation

        return weight, colony

    # Process the 10 generations and calculate weight
    weight10, _ = evolve_colony(gen10_c, gen10_i)

    # Process the 50 generations and calculate weight
    weight50, _ = evolve_colony(gen50_c, gen50_i)

    # Return the weights as a JSON response
    return jsonify([str(weight10), str(weight50)])
