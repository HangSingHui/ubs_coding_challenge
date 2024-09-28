from flask import Blueprint, request, jsonify

clumsy_programmer_bp = Blueprint('clumsy_programmer', __name__)

class PrefixTreeNode:
    def __init__(self):
        self.children = {}  # Use a dictionary for dynamic children
        self.end = False

class PrefixTree:
    def __init__(self):
        self.root = PrefixTreeNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for c in word:
            if c not in curr.children:
                curr.children[c] = PrefixTreeNode()
            curr = curr.children[c]
        curr.end = True

    def find_one_mistype(self, mistyped_word: str):
        return self._search_for_candidate(self.root, "", mistyped_word)

    def _search_for_candidate(self, node: PrefixTreeNode, prefix: str, mistyped_word: str):
        # If we reach a word end and it's a valid correction, return it
        if node.end and self._is_one_mistyped(mistyped_word, prefix):
            return prefix
        
        # Explore all child nodes (characters) recursively
        for char, child in node.children.items():
            result = self._search_for_candidate(child, prefix + char, mistyped_word)
            if result:  # Return early if a match is found
                return result
        
        return None

    def _is_one_mistyped(self, mistyped_word: str, correct_word: str) -> bool:
        # Ensure both words have the same length
        if len(mistyped_word) != len(correct_word):
            return False
        # Count the number of character differences
        differences = sum(1 for a, b in zip(mistyped_word, correct_word) if a != b)
        return differences == 1

@clumsy_programmer_bp.route('/the-clumsy-programmer', methods=['POST'])
def clumsy():
    corrections = []
    data = request.get_json()

    # Limit the processing to only the first 4 cases
    data = data[0:4]

    # Create one PrefixTree for all cases
    prefixTree = PrefixTree()
    
    # Insert all words from all cases into the PrefixTree
    for case in data:
        dictionary = case["dictionary"]
        for word in dictionary:
            prefixTree.insert(word)

    # Process each case's mistypes
    for case in data:
        mistypes = case["mistypes"]
        case_corrections = []
        
        for word in mistypes:
            corrected_word = prefixTree.find_one_mistype(word)
            case_corrections.append(corrected_word if corrected_word else None)
        
        corrections.append({"corrections": case_corrections})
    
    # Return the corrections for the first 4 cases
    return jsonify(corrections)
