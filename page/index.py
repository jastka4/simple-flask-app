from flask import Flask, jsonify, request

from model.game import Game, GameSchema
from model.move import Move, MoveSchema

app = Flask(__name__)

games = [
    Game('test', ['Ola', 'Justyna'], [Move(0, 'Ola', 4, 3, 2)]),
    Game('finals_k_k', ['Garri Kasparow', 'Anatolij Karpow']),
    Game('finals_k_c', ['Siergiej Kariakin', 'Magnus Carlsen']),
    Game('match_s_g', ['Dariusz Świercz', 'Anisz Giri'])
]


@app.route('/games')
def get_games():
    schema = GameSchema(many=True)
    result = schema.dump(filter(lambda t: t.finished is not True, games))
    return jsonify(result.data)


@app.route('/createGame', methods=['POST'])
def create_game():
    game = GameSchema().load(request.get_json())
    games.append(game.data)
    return '', 201


@app.route('/endGame', methods=['GET'])
def end_game():
    game_name = request.args.get('game')
    game = find_game(game_name)
    game.finished = True
    return '', 204


@app.route('/move', methods=['GET'])
def get_move():
    game_name = request.args.get('game')
    player_name = request.args.get('player')
    game = find_game(game_name)
    last_move = game.get_last_move(player_name)
    if last_move.read is not True:
        schema = MoveSchema()
        result = schema.dump(last_move)
        last_move.read = True
        return jsonify(result.data)
    else:
        return 'Value already read!', 403


@app.route('/move', methods=['POST'])
def add_move():
    json_data = request.get_json()
    game_name = json_data['game']
    game = find_game(game_name)
    schema = MoveSchema()
    result = schema.load(json_data['move'])
    game.add_move(result.data)
    return '', 201


def find_game(name):
    return [game for game in games if game.name in name][0]


if __name__ == '__main__':
    app.run()
