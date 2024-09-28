from flask import Blueprint, request, jsonify
clumsy_programmer_bp = Blueprint('clumsy_programmer', __name__)

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.word = None  # Store the actual word for easy retrieval


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.word = word  # Store the word in the node


class ClumsyProgrammer:
    def __init__(self, dictionary):
        self.trie = Trie()
        for word in dictionary:
            self.trie.insert(word)

    def search_one_char_off(self, mistyped_word):
        corrections = []
        self._search_helper(self.trie.root, mistyped_word, 0, False, corrections)
        return corrections

    def _search_helper(self, node, word, index, changed, corrections):
        if index == len(word):
            if node.is_end_of_word and changed:  # Valid correction found
                corrections.append(node.word)
            return

        char = word[index]

        # Traverse through the current node's children
        for child_char, child_node in node.children.items():
            # Case 1: Keep the same character
            if child_char == char:
                self._search_helper(child_node, word, index + 1, changed, corrections)
            # Case 2: Change the character (if we haven't changed before)
            elif not changed:
                self._search_helper(child_node, word, index + 1, True, corrections)  # Mark as changed

@clumsy_programmer_bp.route('/the-clumsy-programmer', methods=['POST'])
def clumsy():
    data = request.get_json()
    corrections = []

    # Limit the processing to only the first 4 cases
    data = data[0:4]

    for case in data:
        mistypes = case["mistypes"]
        clumsy_programmer = ClumsyProgrammer(case["dictionary"])
        case_corrections = []
        for mistype in mistypes:
            case_corrections+=(clumsy_programmer.search_one_char_off(mistype))
    
        corrections.append({"corrections": case_corrections})
    
    corrections.append({"corrections": case_corrections})
    corrections.append({"corrections": case_corrections})

    return jsonify(corrections)
