import pygame
from const import *

class Dragger:
    """
    A class to manage dragging chess pieces on the board.

    Attributes:
        piece: The chess piece being dragged.
        dragging (bool): Indicates whether a piece is currently being dragged.
        mouseX: The x-coordinate of the mouse cursor.
        mouseY: The y-coordinate of the mouse cursor.
        initial_row: The initial row index of the piece being dragged.
        initial_col: The initial column index of the piece being dragged.

    Methods:
        update_blit(surface): Updates the display surface with the dragged piece.
        update_mouse(pos): Updates the mouse coordinates.
        save_initial(pos): Saves the initial position of the piece being dragged.
        drag_piece(piece): Sets the piece to be dragged.
        undrag_piece(): Clears the dragged piece and ends the dragging operation.
    """
    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0


    #blit methods

    def update_blit(self, surface):

        #texture
        self.piece.set_texture(size=128)
        texture = self.piece.texture
        #img
        img = pygame.image.load(texture)
        #rect
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center=img_center)
        #blit
        surface.blit(img, self.piece.texture_rect)


 
    #other methods
    
    
    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos

    def save_initial(self, pos):
        self.initial_row = pos[1] // SQSIZE
        self.initial_col = pos[0] // SQSIZE

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False

