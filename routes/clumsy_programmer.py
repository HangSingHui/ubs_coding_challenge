from flask import Flask, Blueprint, request, jsonify
from flask_caching import Cache

# Initialize Flask app
app = Flask(__name__)

# Initialize Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Initialize Blueprint
clumsy_programmer_bp = Blueprint('clumsy_programmer', __name__)

class PrefixTreeNode:
    def __init__(self):
        self.children = {}
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
        if node.end and self._is_one_mistyped(mistyped_word, prefix):
            return prefix
        
        for char, child in node.children.items():
            result = self._search_for_candidate(child, prefix + char, mistyped_word)
            if result:
                return result
        
        return None

    def _is_one_mistyped(self, mistyped_word: str, correct_word: str) -> bool:
        if len(mistyped_word) != len(correct_word):
            return False
        differences = sum(1 for a, b in zip(mistyped_word, correct_word) if a != b)
        return differences == 1

@clumsy_programmer_bp.route('/the-clumsy-programmer', methods=['POST'])
@cache.cached(timeout=60)  # Cache the response for 60 seconds
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

# Register the blueprint
app.register_blueprint(clumsy_programmer_bp)

if __name__ == '__main__':
    app.run(debug=True)