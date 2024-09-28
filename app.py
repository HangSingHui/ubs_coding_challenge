import logging
import socket

from routes import app

logger = logging.getLogger(__name__)

# Import your routes here
from routes.wordle_game import w_game

# Register the routes
app.add_url_rule('/wordle-game', 'w_game', w_game, methods=['POST'])


@app.route('/', methods=['GET'])
def default_route():
    return 'Python Template'


logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    logging.info("Starting application ...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 5050))
    port = sock.getsockname()[1]
    sock.close()
    app.run(port=port)
