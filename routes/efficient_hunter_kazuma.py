from flask import Blueprint, request, jsonify
from typing import List

efficient_hunter_bp = Blueprint('efficient_hunter_kazuma', __name__)
def calculate_efficiency(monster_list):
    
    n = len(monster_list)
    
    # Memoization table to store the maximum efficiency from time `i` onwards
    memo = [-1] * n

    # Helper function to calculate max efficiency from time `i`
    def dp(i):
        # Base case: if we're beyond the last time frame, return 0
        if i >= n:
            return 0
        
        # Return memoized result if it exists
        if memo[i] != -1:
            return memo[i]

        # Case 1: Skip this time frame and move to rear (just carry forward the previous efficiency)
        max_efficiency = dp(i + 1)

        # Case 2: Try preparing a circle at time `i` and attack at some `j > i`
        cost = monster_list[i]  # The cost of preparing a circle at `i`
        for j in range(i + 1, n):
            gain = monster_list[j]  # The gold gained by attacking at `j`
            # Efficiency is gain - cost, plus the best future efficiency from `j + 2` (because Kazuma must retreat)
            efficiency = (gain - cost) + dp(j + 2)
            # Update the maximum efficiency
            max_efficiency = max(max_efficiency, efficiency)

        # Memoize the result for time `i`
        memo[i] = max_efficiency
        return max_efficiency

    # Start the recursion from time `0`
    return dp(0)

@efficient_hunter_bp.route('/efficient-hunter-kazuma', methods=['POST'])
def calculate_efficiency_api():
    monster_list = request.get_json()
    result = []

    for m in list(monster_list):
        efficiency = calculate_efficiency(m["monsters"])
        result.append({"efficiency": efficiency})
    
    return jsonify(result)




