import pygame
from piece import Piece, Color
from tile import Tile

DEBUG = 0


class Pawn(Piece):
    def __init__(self, pos: tuple[int, int], color: Color, board, tile_size:int = 200):
        super().__init__(pos, color, board)
        # TODO: add correct image for king, currently it shares the image of the pawns
        img_path = 'images/black-pawn.png' if color == Color.BLACK else 'images/red-pawn.png'
        self.x = pos[1]
        self.y = pos[0]
        self.board = board
        self.tile_size = tile_size
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (self.tile_size, self.tile_size))

    def _possible_moves(self) -> list[tuple[int]]:
        """ Returns a list of possible moves for the pawn, does not check if move is legal for the current positions """
        # TODO: return the correct possible moves
        return [(1, 0)] if self.color == Color.BLACK else [(-1, 0)] # returns a list of possible moves with indexing (x, y)
    

    def _possible_takes(self) -> list[tuple[int]]:
        """ Returns a list of possible takes for the pawn, does not check if take is legal for the current positions """
        # TODO: return the correct possible takes
        return [(1, -1), (1, 1)] if self.color == Color.BLACK else [(-1, -1), (-1, 1)] # returns a list of possible takes with indexing (x, y)


    def valid_moves(self) -> list[tuple[int]]:
        """ Returns a list of legal moves for the pawn for the current position """
        # TODO: return the correct legal moves
        moves = []
        poss_moves = self._possible_moves()
        for move in poss_moves:
            tile_pos = (self.pos[0] + move[0], self.pos[1] + move[1]) # (row, col)
            if tile_pos[0] > self.board.num_tiles or tile_pos[0] < 0 or tile_pos[1] > self.board.num_tiles or tile_pos[1] < 0:
                continue
            
            tile = self.board.get_tile_from_pos(tile_pos[1], tile_pos[0]) # function takes (x, y) parameters so (col, row)
            if tile.piece is None:
                moves.append(move)
        return moves

    
    def valid_takes(self) -> list[tuple[int]]:
        """ Returns a list of legal takes for the pawn for the current position """
        # TODO: return the correct legal takes
        takes = []
        poss_takes = self._possible_takes()
        for take in poss_takes:
            tile_pos = (self.pos[0] + take[0], self.pos[1] + take[1]) # (row, col)
            if tile_pos[0] > 2 or tile_pos[0] < 0 or tile_pos[1] > 2 or tile_pos[1] < 0:
                continue
            
            tile = self.board.get_tile_from_pos(tile_pos[1], tile_pos[0]) # function takes (x, y) parameters so (col, row)
            if tile.piece is not None:
                other_color = Color.BLACK if self.color == Color.RED else Color.RED
                if tile.piece.color == other_color:
                    takes.append(take)
        return takes


    def move(self, tile: Tile) -> bool:
        """ Moves the pawn to the specified tile if applicable, returns True if move was applicable, returns False otherwise """
        # TODO: move this to piece.py
        valid_moves = self.valid_moves()
        valid_takes = self.valid_takes()
        move = (tile.y_index - self.pos[0], tile.x_index - self.pos[1]) # (row, col)
        print(f'pos: {self.pos[0], self.pos[1]}')
        print(f'move: {move[0], move[1]}')

        #if DEBUG >= 1: 
        print(f'valid moves: {valid_moves}')
        # if DEBUG >= 1: 
        print(f'valid takes: {valid_takes}')
        if move in self.valid_moves():
            prev = self.board.get_tile_from_pos(self.pos[1], self.pos[0])
            self.pos = (tile.y_index, tile.x_index)
            prev.piece = None
            tile.piece = self
            self.board.selected_piece = None
            return True

        if move in valid_takes:
            prev = self.board.get_tile_from_pos(self.pos[1], self.pos[0])
            self.pos = (tile.y_index, tile.x_index)
            prev.piece = None
            tile.piece = self
            self.board.selected_piece = None
            return True

        else:
            self.board.selected_piece = None
            return False
