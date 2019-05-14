import datetime as dt

from marshmallow import Schema, fields, post_load

from model.move import MoveSchema


class Game:
    def __init__(self, name, players, moves=[]):
        self.name = name
        self.players = players
        self.created_at = dt.datetime.now()
        self.moves = moves
        self.finished = False

    def __repr__(self):
        return '<Game(name={self.name!r})>'.format(self=self)

    def add_move(self, move):
        self.moves.append(move)

    def get_last_move(self, player_name):
        player_moves = list(filter(lambda m: m.player == player_name, self.moves))
        return player_moves[-1]


class GameSchema(Schema):
    name = fields.Str()
    players = fields.List(fields.Str())
    created_at = fields.Date()
    moves = fields.List(fields.Nested(MoveSchema))
    finished = fields.Bool()

    @post_load
    def make_game(self, data):
        return Game(**data)
