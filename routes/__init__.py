from flask import Flask

app = Flask(__name__)
import routes.wordle_game
import routes.dodge_bullet
