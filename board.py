from const import *
from square import Square
from piece import *
import os
from move import *
import copy
from sound import Sound

class Board:

    """
    Represents a chess board.

    Attributes:
        squares (list): A 2D list representing the squares on the chess board.
        last_move (Move or None): The last move made on the board.

    Methods:
        move(piece, move, testing=False): Moves a piece on the board.
        valid_move(piece, move): Checks if a move is valid for a given piece.
        check_promotion(piece, final): Checks for pawn promotion and promotes if necessary.
        castling(initial, final): Checks if castling is possible.
        set_true_en_passant(piece): Sets en passant flag for the given pawn piece to true.
        in_check(piece, move): Checks if a move puts the player's king in check.
        calc_moves(piece, row, col, bool=True): Calculates all possible moves for a given piece.
        _create(): Creates the initial layout of the chess board.
        _add_pieces(color): Adds pieces of the specified color to the board.
    """

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move, testing = False):
        initial = move.initial
        final = move.final

        en_passant_empty = self.squares[final.row][final.col].isempty()

        #console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        

        

        
        if isinstance(piece, Pawn):
            #enpassant capoture
        
            diff = final.col - initial.col
            if diff != 0 and en_passant_empty:
                self.squares[initial.row][initial.col + diff].piece = None
                self.squares[final.row][final.col].piece = piece
                if not testing:
                    sound = Sound(os.path.join('assets/sounds/siuuu.mp3'))
                    sound.play()
   

            #pawn promotion
            else:
                self.check_promotion(piece, final)

        #king casteling
        if isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                diff = final.col - initial.col
                
                if diff < 0:
                    rook = piece.left_rook
                else:
                    rook = piece.right_rook     
                self.move(rook, rook.moves[-1])


        #move
        piece.moved = True

        #clear valid moves
        piece.clear_moves()

        #set last move
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2
    
    
    
    def set_true_en_passant(self, piece):
        if not isinstance(piece, Pawn):
            return
        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False

        piece.en_passant = True


    

  
    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, testing = True)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    p= temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool = False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
                        

    def calc_moves(self, piece, row, col, bool = True):
        '''
            Calculate all the possible (valid) moves of an spcifiv piece on a specific position.
            
        '''
        def pawn_moves():
            if piece.moved:
                steps = 1
            else:
                steps = 2

            #vertical move
            start = row + piece.dir
            end = row + (piece.dir * (1+steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        #create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        #create new move
                        move = Move(initial, final)
                        #check checks
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                    else:
                        break #we are blocked
                else:
                    break

                #diagonal move
                possible_move_row = row + piece.dir
                possible_move_cols = [col-1, col+1]
                for possible_move_col in possible_move_cols:
                    if Square.in_range(possible_move_row, possible_move_col):
                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            #create initial and final move squares
                            initial = Square(row, col)
                            final_piece = self.squares[possible_move_row][possible_move_col].piece
                            final = Square(possible_move_row, possible_move_col, final_piece)
                            #create new move
                            move = Move(initial, final)
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            
                #en passant moves
                if piece.color == 'white':
                    r = 3
                else:
                    r = 4
                if piece.color == 'white':
                    fr = 2
                else:
                    fr = 5
                #left en passant
                if Square.in_range(col-1) and row == r:
                    if self.squares[row][col-1].has_enemy_piece(piece.color):
                        p = self.squares[row][col-1].piece
                        if isinstance(p, Pawn):
                            if p.en_passant:
                                #create initial and final move squares
                                initial = Square(row, col)
                                final = Square(fr,col-1, p)
                                #create new move
                                move = Move(initial, final)
                                if bool:
                                    if not self.in_check(piece, move):
                                        piece.add_move(move)
                                else:
                                    piece.add_move(move)

               
                #right en passant
                if Square.in_range(col+1) and row == r:
                    if self.squares[row][col+1].has_enemy_piece(piece.color):
                        p = self.squares[row][col+1].piece
                        if isinstance(p, Pawn):
                            if p.en_passant:
                                #create initial and final move squares
                                initial = Square(row, col)
                                final = Square(fr, col+1, p)
                                #create new move
                                move = Move(initial, final)
                                if bool:
                                    if not self.in_check(piece, move):
                                        piece.add_move(move)
                                else:
                                    piece.add_move(move)





        def knight_moves():
        
            #8 possible moves
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        #create squares of new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece) 
                        #create new move
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                            else:
                                break
                        else:
                            piece.add_move(move)

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

        


                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        # create squares of the possible new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create a possible new move
                        move = Move(initial, final)

                        # empty = continue looping
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                          
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            break
                            

                        # has team piece = break
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    
                    # not in range
                    else: break

                    possible_move_row = possible_move_row + row_incr 
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjs = [
                (row-1, col+0),
                (row-1, col+1),
                (row+0, col+1),
                (row+1, col+1),
                (row+1, col+0),
                (row+1, col-1),
                (row+0, col-1),
                (row-1,col-1)
            ]
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        #create squares of new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col) #piece = piece
                        #create new move
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                            else:
                                break
                        else:
                            piece.add_move(move)

            #castling moves
            if not piece.moved:
                #queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            if self.squares[row][c].has_piece():
                                break

                            if c ==3:
                                #adds keft rook to king
                                piece.left_rook = left_rook

                                #rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)
                                

                                #king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)
                                
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        left_rook.add_move(moveR)
                                        piece.add_move(moveK)
                                else:
                                    left_rook.add_move(moveR)
                                    piece.add_move(moveK)

                #king castling
                right_rook = self.squares[row][7].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(5, 7):
                            if self.squares[row][c].has_piece():
                                break

                            if c == 6:
                                #adds right rook to king
                                piece.right_rook = right_rook

                                #rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)
                                

                                #king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                        right_rook.add_move(moveR)
                                        piece.add_move(moveK)
                                else:
                                    right_rook.add_move(moveR)
                                    piece.add_move(moveK) 


        if isinstance(piece, Pawn):
            pawn_moves()

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            straightline_moves([
                (-1,1),
                (-1,-1),
                (1,1),
                (1,-1)
            ])

        elif isinstance(piece, Rook):
            straightline_moves([
                (-1,0),
                (0,1),
                (1,0),
                (0,-1)
            ])

        elif isinstance(piece, Queen):
            straightline_moves([
                (-1,1),
                (-1,-1),
                (1,1),
                (1,-1),
                (-1,0),
                (0,1),
                (1,0),
                (0,-1)
            ])

        elif isinstance(piece, King):
            king_moves()
        
    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)
    
    def _add_pieces(self, color):
        if color == 'white':
            row_pawn, row_other = (6, 7)
        else:
            row_pawn, row_other = (1, 0)


        #Create all pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        #create knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        #create bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        #create rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        #create queens
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        #create kings
        self.squares[row_other][4] = Square(row_other, 4, King(color))





