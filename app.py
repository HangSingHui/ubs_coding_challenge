import logging
import socket

from routes import app

logger = logging.getLogger(__name__)

# Import your routes here
# from routes.wordle_game import w_game
# from routes.dodge_bullet import dodge
from routes.digital_colony import digital_colony_bp
from routes.clumsy_programmer import clumsy_programmer_bp
from routes.efficient_hunter_kazuma import efficient_hunter_bp
from routes.parking_lot import parking_lot_bp
from routes.mail_time import mailtime_bp

# Register the routes
app.register_blueprint(digital_colony_bp)
app.register_blueprint(clumsy_programmer_bp)
app.register_blueprint(efficient_hunter_bp)
app.register_blueprint(parking_lot_bp)
app.register_blueprint(mailtime_bp)

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
