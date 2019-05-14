from marshmallow import Schema, fields, post_load


class Move:
    def __init__(self, id, player, x, y, piece):
        self.id = id
        self.player = player
        self.x = x
        self.y = y
        self.piece = piece
        self.read = False

    def __repr__(self):
        return '<Move(id={self.id!r})>'.format(self=self)


class MoveSchema(Schema):
    id = fields.Int()
    player = fields.Str()
    x = fields.Int()
    y = fields.Int()
    piece = fields.Int()
    read = fields.Bool()

    @post_load
    def make_move(self, data):
        return Move(**data)
