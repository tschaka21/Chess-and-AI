import os

class Piece:
    """
    Represents a chess piece.

    Attributes:
        name (str): The name of the piece.
        color (str): The color of the piece ('white' or 'black').
        value (float): The value of the piece in terms of chess strength.
        moves (list): A list of possible moves for the piece.
        moved (bool): Indicates whether the piece has moved from its initial position.
        texture (str): The file path to the texture image of the piece.
        texture_rect (pygame.Rect): The rectangle specifying the position and size of the piece's texture.

    Methods:
        set_texture(size=80): Sets the texture image file path for the piece.
        add_move(move): Adds a move to the list of possible moves for the piece.
        clear_moves(): Clears the list of possible moves for the piece.
    """
    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color

        if color == 'white':
            value_sign = 1
        else:
            value_sign = -1

        self.value = value * value_sign
        self.moves = []
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self, size = 80):
        self.texture = os.path.join(f'assets/images/imgs-{size}px/{self.color}_{self.name}.png')

    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []

class Pawn(Piece):

    def __init__(self, color):
        if color == 'white':
            self.dir = -1
        else: 
            self.dir = 1
        self.en_passant = False
        super().__init__('pawn', color, 1.0)
 
class Knight(Piece):
    def __init__(self, color):
        super().__init__('knight', color, 3.0)

class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', color, 3.001)

class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color, 5.0)

class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color, 9.0)

class King(Piece):
    def __init__(self, color):
        self.left_rook = None
        self.right_rook = None
        super().__init__('king', color, 10000.0)
