from flask import Blueprint, render_template, session, url_for, request, json

from src.minesweeper.game import Game, GameTracker

page_bp = Blueprint('/', __name__)


@page_bp.route('/')
def index():
    return render_template('index.html')


@page_bp.route('/minesweeper')
def minesweeper():
    gid = session['gid']
    game = GameTracker().get_grid(gid)
    return render_template('game.html', game=game,  tools=game.data['assist'], width=game.width, height=game.height)
