import os

class Config(): 
    """Base config"""
    APP_DIR = os.path.abspath(os.path.dirname(__file__)) 
    

class ProdConfig(Config): 
    ENV = 'prod'
    DEBUG = False

class DevConfig(Config): 
    ENV = 'dev' 
    DEBUG = True

