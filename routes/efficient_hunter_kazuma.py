from flask import Blueprint, request, jsonify
from typing import List

efficient_hunter_bp = Blueprint('efficient_hunter_kazuma', __name__)
class Solution:
    def calculate_efficiency(self, monsters: List[int]) -> int:
        n = len(monsters)
        if n == 0:
            return 0
        
        # Initialize dp array
        # dp[i] represents the maximum efficiency achievable up to index i
        dp = [0] * (n + 2)  # +2 to handle the cooldown period
        
        # Initialize variables to keep track of the best efficiency after attacking and not attacking
        best_after_attack = 0
        best_without_attack = 0
        
        for i in range(n):
            # Current best efficiency without attacking
            current_without_attack = max(best_after_attack, best_without_attack)
            
            # Calculate efficiency if we attack at this position
            attack_gain = sum(monsters[i:min(i+3, n)]) - 1  # Sum of next 3 positions (or less) minus preparation cost
            current_with_attack = attack_gain + (dp[i-1] if i > 0 else 0)
            
            # Update dp
            dp[i] = max(current_without_attack, current_with_attack)
            
            # Update best efficiencies
            best_without_attack = current_without_attack
            best_after_attack = current_with_attack
        
        return max(dp)


@efficient_hunter_bp.route('/efficient-hunter-kazuma', methods=['POST'])
def efficient_hunter_kazuma():
    data = request.get_json()
    solution = Solution()
    result = []
    
    for case in data:
        monsters =list(case['monsters'])
        efficiency = solution.calculate_efficiency(monsters)
        result.append({"efficiency": efficiency})
    
    return jsonify(result)
