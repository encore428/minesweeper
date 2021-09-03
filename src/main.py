from flask import Flask
from flask_bootstrap import Bootstrap

from src.settings import ProdConfig
from src.api import api_bp
from src.pages import page_bp
from src.middleware import PrefixMiddleware


def create_app(config_object=ProdConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.secret_key = 'abc'
    bootstrap = Bootstrap(app)
    app.wsgi_app = PrefixMiddleware(app.wsgi_app, voc=False)
    register_blueprint(app)
    return app


def register_blueprint(app):
    app.register_blueprint(page_bp, url_prefix='/')
    app.register_blueprint(api_bp, url_prefix='/api')
