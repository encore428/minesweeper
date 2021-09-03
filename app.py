"""Create an application instance."""
from flask.helpers import get_debug_flag

from src.main import create_app
from src.settings import DevConfig, ProdConfig

CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app(CONFIG)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
