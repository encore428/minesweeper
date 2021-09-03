from flask import Blueprint, request, json, redirect, Response, session, url_for


from src.minesweeper.game import get_game_type, Game, GameTracker

api_bp = Blueprint('api', __name__)


@api_bp.route('/game', methods=['POST'])
def game():
    level = request.json.get('level')
    assist = request.json.get('assist')
    game = get_game_type(level, assist)
    game.gen_new_game()

    gameTracker = GameTracker()
    gid = gameTracker.set_grid(game)

    session['gid'] = gid

    return Response(status=200)


@api_bp.route('/reload_game_type', methods=['GET'])
def reload_game():
    gid = session['gid']
    game = GameTracker().get_grid(gid)
    return game.reload_game(gid)


def set_session(key, value):
    session[key] = value


@api_bp.route('/update', methods=['POST'])
def update_game():

    result = request.json
    action_type = result.get('type')
    cell = result.get('cell')
    gid = session['gid']

    game = GameTracker().get_grid(gid)
    print(f"action_type={action_type} cell={cell}, gid={gid} game={game}")

    if action_type == 'flag':
        return game.toggle_flag(gid, cell)

    return game.open(gid, cell)
