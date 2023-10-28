import pygame
from piece import Piece, Color, DEBUG


class King(Piece):
    def __init__(self, pos: tuple[int, int], color: Color, board, tile_size:int = 200):
        super().__init__(pos, color, board)
        img_path = 'images/black-king.png' if color == Color.BLACK else 'images/red-king.png'
        self.x = pos[1]
        self.y = pos[0]
        self.board = board
        self.tile_size = tile_size
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (self.tile_size, self.tile_size))

    def _possible_moves(self) -> list[tuple[int]]:
        """ Returns a list of possible moves for the pawn, does not check if move is legal for the current positions """
        return [(1, 1), (1, -1), (-1, 1), (-1, -1)] # returns a list of possible moves with indexing (x, y)
    

    def _possible_takes(self) -> list[tuple[int]]:
        """ Returns a list of possible takes for the pawn, does not check if take is legal for the current positions """
        return [(2, -2), (2, 2), (-2, -2), (-2, 2)] # returns a list of possible takes with indexing (x, y)


    def valid_moves(self) -> list[tuple[int]]:
        """ Returns a list of legal moves for the pawn for the current position """
        moves = []
        poss_moves = self._possible_moves()
        for move in poss_moves:
            tile_pos = (self.pos[0] + move[0], self.pos[1] + move[1]) # (row, col)
            if tile_pos[0] > self.board.num_tiles or tile_pos[0] < 0 or tile_pos[1] > self.board.num_tiles or tile_pos[1] < 0:
                continue
            
            tile = self.board.get_tile_from_pos(tile_pos[1], tile_pos[0]) # function takes (x, y) parameters so (col, row)
            # NOTE: we have to check if the tile is None because in checkers you could 'move off the board'
            if tile is not None and tile.piece is None:
                moves.append(move)
        return moves

    
    def valid_takes(self) -> list[tuple[int]]:
        """ Returns a list of legal takes for the pawn for the current position """
        takes = []
        poss_takes = self._possible_takes()
        for take in poss_takes:
            jump_tile_pos = (self.pos[0] + take[0], self.pos[1] + take[1]) # (row, col)
            if jump_tile_pos[0] > self.board.num_tiles or jump_tile_pos[0] < 0 or jump_tile_pos[1] > self.board.num_tiles or jump_tile_pos[1] < 0:
                continue
            
            jump_tile = self.board.get_tile_from_pos(jump_tile_pos[1], jump_tile_pos[0]) # function takes (x, y) parameters so (col, row)
            if jump_tile is not None and jump_tile.piece is None:
                target_tile_pos = (self.pos[0] + take[0] // 2, self.pos[1] + take[1] // 2) # (row, col)
                target_tile = self.board.get_tile_from_pos(target_tile_pos[1], target_tile_pos[0])
                other_color = Color.BLACK if self.color == Color.RED else Color.RED
                if target_tile.piece is not None and target_tile.piece.color == other_color:
                    takes.append(take)
        return takes
