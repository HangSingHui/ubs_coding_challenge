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
        candidates = []
        for candidate in self._get_all_words(self.root, "", []):
            if self._is_one_mistyped(word, candidate):
                candidates.append(candidate)
        return candidates

    def _get_all_words(self, node, prefix, results):
        if node.end:
            results.append(prefix)
        for i in range(26):
            if node.children[i] is not None:
                self._get_all_words(node.children[i], prefix + chr(i + ord("a")), results)
        return results

    def _is_one_mistyped(self, mistyped_word, correct_word):
        if len(mistyped_word) != len(correct_word):
            return False
        # Count the number of differences
        differences = sum(1 for a, b in zip(mistyped_word, correct_word) if a != b)
        return differences == 1


@clumsy_programmer_bp.route('/the-clumsy-programmer', methods=['POST'])
def clumsy():
    corrections = []
    data = request.get_json()

    for case in data:
        dictionary, mistypes = case["dictionary"], case["mistypes"]

        prefixTree = PrefixTree()
        # Create a prefix trie
        for word in dictionary:
            prefixTree.insert(word)
        
        case_corrections = []
        # Check for mistypes
        for word in mistypes:
            corrected_words = prefixTree.find_one_mistype(word)
            if corrected_words:
                case_corrections.append(corrected_words[0])  # First correct candidate
            else:
                case_corrections.append(None)  # If no correction is found
        
        corrections.append({"corrections": case_corrections})
    
    # Return the corrections in the specified format
    return jsonify(corrections)
