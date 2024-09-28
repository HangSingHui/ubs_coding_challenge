from flask import Blueprint, request, jsonify

clumsy_programmer_bp = Blueprint('clumsy_programmer', __name__)

class PrefixTreeNode:
    def __init__(self):
        self.children = [None] * 26
        self.end = False

class PrefixTree:
    def __init__(self):
        self.root = PrefixTreeNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for c in word:
            i = ord(c) - ord("a")
            if curr.children[i] is None:
                curr.children[i] = PrefixTreeNode()
            curr = curr.children[i]
        curr.end = True

    def find_one_mistype(self, mistyped_word: str):
        return self._search_for_candidate(self.root, "", mistyped_word)

    def _search_for_candidate(self, node: PrefixTreeNode, prefix: str, mistyped_word: str):
        if node.end and self._is_one_mistyped(mistyped_word, prefix):
            return prefix  # Return the first matching candidate
        
        for i in range(26):
            if node.children[i] is not None:
                result = self._search_for_candidate(node.children[i], prefix + chr(i + ord("a")), mistyped_word)
                if result:  # If a candidate was found
                    return result
        
        return None  # Return None if no candidates found

    def _is_one_mistyped(self, mistyped_word: str, correct_word: str) -> bool:
        if len(mistyped_word) != len(correct_word):
            return False
        differences = sum(1 for a, b in zip(mistyped_word, correct_word) if a != b)
        return differences == 1


@clumsy_programmer_bp.route('/the-clumsy-programmer', methods=['POST'])
def clumsy():
    corrections = []
    data = request.get_json()[:-2]

    for case in data:
        dictionary, mistypes = case["dictionary"], case["mistypes"]

        prefixTree = PrefixTree()
        for word in dictionary:
            prefixTree.insert(word)
        
        case_corrections = []
        for word in mistypes:
            corrected_word = prefixTree.find_one_mistype(word)
            case_corrections.append(corrected_word if corrected_word else None)
        
        corrections.append({"corrections": case_corrections})
    
    return jsonify(corrections)
