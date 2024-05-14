
import pygame
import sys
from const import *
from game import Game
from dragger import Dragger
from square import Square
from move import Move
from theme import Theme
from color import Color



class Main:
    """
This is the main class for a simple chess game implemented in Python using Pygame.

Dependencies:
    - pygame
    - sys
    - const module
    - game module
    - dragger module
    - square module
    - move module
    - theme module
    - color module

Attributes:
    screen (pygame.Surface): The Pygame window surface.
    game (Game): The instance of the Game class representing the chess game.

Methods:
    mainloop(self): The main loop of the game that handles user input and updates the game state accordingly.
"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):

        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger


        while True:
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
    	    
                #click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    #if clicked square has a piece 
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        #valid piece(color)
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool = True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            #show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                 
                #motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE
                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)
                
                #click release
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        #possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        if board.valid_move(dragger.piece, move):
                            #normal capture
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)

                            board.set_true_en_passant(dragger.piece)
                            #sound
                            game.play_sound(captured)
                            #show methods
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            #next turn
                            game.next_turn()


                    dragger.undrag_piece()
                
                #key press
                    
                elif event.type == pygame.KEYDOWN:
                    #change theme
                    if event.key == pygame.K_t:
                        game.change_theme()

                    if event.key == pygame.K_r:
                        game.reset()
                        screen = self.screen
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger


                #quit
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


               
            pygame.display.update()

main = Main()
main.mainloop()

