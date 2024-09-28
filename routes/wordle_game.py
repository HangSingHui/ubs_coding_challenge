import logging
import random
from flask import request, jsonify

logger = logging.getLogger(__name__)

# Load the words from the file only once at startup
with open("data/wordle-list.txt", "r") as file: 
    allText = file.read() 
    words = list(map(str, allText.split())) 

# Global game state variables
history = []
evaluation = []
success = False
word = ""

def get_new_word():
    """Select a new word from the word list."""
    global word
    word = random.choice(words)

def get_evaluation(count, guess):
    if guess == word:
        return "O" * len(guess)
    
    res = ""
    for i in range(len(guess)):
        if i + 1 == count:
            res += "?"
        elif guess[i] == word[i]:
            res += "O"
        elif guess[i] not in word:
            res += "-"
        elif guess[i] in word:
            res += "X"
    return res

def w_game():
    global word, history, success, evaluation
    print(word)
    # Initialize or reset the game state if needed
    if not word or success or len(history) == 6:
        get_new_word()
        history = []
        success = False
        evaluation = []

    # Get the guess from the request
    guess_data = request.get_json()
    guess = guess_data['guess']
    history.append(guess)
    evaluation.append(get_evaluation(len(history), guess))

    if guess == word:
        success = True
        return jsonify({"guessHistory": history, "evaluationHistory": evaluation}), 200

    return jsonify({"guessHistory": history, "evaluationHistory": evaluation}), 200
