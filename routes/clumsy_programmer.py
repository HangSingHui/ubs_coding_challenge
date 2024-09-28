from flask import Blueprint, request, jsonify

clumsy_programmer_bp = Blueprint('clumsy_programmer', __name__)

class PrefixTreeNode:
    def __init__(self):
        self.children = [None] * 26
        self.end = False

class PrefixTree:
    def __init__(self):
        self.root = PrefixTreeNode()

    def insert(self, word) -> None:
        curr = self.root
        for c in word:
            i = ord(c) - ord("a")
            if curr.children[i] is None:
                curr.children[i] = PrefixTreeNode()
            curr = curr.children[i]
        curr.end = True

    def search(self, word):
        curr = self.root
        for c in word:
            i = ord(c) - ord("a")
            if curr.children[i] is None:
                return False
            curr = curr.children[i]
        return curr.end

    def find_one_mistype(self, word):
        # Use a helper method to find candidates of the same length
        return self._find_candidates_of_length(word, self.root, word)

    def _find_candidates_of_length(self, mistyped_word, node, original_word):
        candidates = []
        self._search_candidates(node, "", candidates, mistyped_word)

        for candidate in candidates:
            if self._is_one_mistyped(mistyped_word, candidate):
                return candidate  # Return immediately upon finding the first match
        return []

    def _search_candidates(self, node, prefix, candidates, mistyped_word):
        if node.end:
            candidates.append(prefix)
        for i in range(26):
            if node.children[i] is not None:
                self._search_candidates(node.children[i], prefix + chr(i + ord("a")), candidates, mistyped_word)

    def _is_one_mistyped(self, mistyped_word, correct_word):
        if len(mistyped_word) != len(correct_word):
            return False
        # Count the number of differences
        differences = sum(1 for a, b in zip(mistyped_word, correct_word) if a != b)
        return differences == 1


@clumsy_programmer_bp.route('/the-clumsy-programmer', methods=['POST'])
def clumsy():
    corrections = []
    data = request.get_json()[:-2]

    for case in data:
        dictionary, mistypes = case["dictionary"], case["mistypes"]

        prefixTree = PrefixTree()
        # Create a prefix trie
        for word in dictionary:
            prefixTree.insert(word)
        
        case_corrections = []
        # Check for mistypes
        for word in mistypes:
            corrected_word = prefixTree.find_one_mistype(word)
            if corrected_word:
                case_corrections.append(corrected_word)  # First correct candidate
            else:
                case_corrections.append(None)  # If no correction is found
        
        corrections.append({"corrections": case_corrections})
    
    # Return the corrections in the specified format
    return jsonify(corrections)
