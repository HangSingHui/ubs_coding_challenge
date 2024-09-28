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

    # Extract generations and colonies from input data
    gen10_c, gen10_i = list(data[0]["colony"]), data[0]["generations"]
    gen50_c, gen50_i = list(data[1]["colony"]), data[1]["generations"]

    # Process the 10 generations
    for i in range(gen10_i):
        new_list = []
        weight = sum(int(n) for n in gen10_c)
        
        for j in range(len(gen10_c)):
            if j == len(gen10_c) - 1:  # Last number, just add it
                new_list.append(gen10_c[j])
                break
            
            # Check if the pairs are already in the hashmap
            if (gen10_c[j], gen10_c[j + 1]) not in hashMap:
                sig = calculateSignature((gen10_c[j], gen10_c[j + 1]))
            else:
                sig = hashMap[(gen10_c[j], gen10_c[j + 1])]
            
            # Calculate new value and append to new_list
            new_value = str(sig + weight)[-1]
            new_list.append(gen10_c[j])
            new_list.append(new_value)
        
        gen10_c = new_list

    # Calculate weight for the first 10 generations
    weight10 = sum(int(n) for n in gen10_c)

    # Process the 50 generations
    for i in range(gen50_i):
        new_list = []
        weight = sum(int(n) for n in gen50_c)

        for j in range(len(gen50_c)):
            if j == len(gen50_c) - 1:  # Last number, just add it
                new_list.append(gen50_c[j])
                break
            
            if (gen50_c[j], gen50_c[j + 1]) not in hashMap:
                sig = calculateSignature((gen50_c[j], gen50_c[j + 1]))
            else:
                sig = hashMap[(gen50_c[j], gen50_c[j + 1])]
            
            new_value = str(sig + weight)[-1]
            new_list.append(gen50_c[j])
            new_list.append(new_value)

        gen50_c = new_list

    # Calculate weight for the 50 generations
    weight50 = sum(int(n) for n in gen50_c)

    # Return the weights as a JSON response
    return jsonify([str(weight10), str(weight50)])
