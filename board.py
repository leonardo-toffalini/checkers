from typing import List
from piece import Piece, Color
from tile import Tile
from pawn import Pawn


class Board:
    def __init__(
        self,
        turn: Color = Color.RED,
        board_size: int = 600,
        num_tiles: int = 3,
        board: list | None = None,
    ):
        self.turn: Color = turn
        self.board_size: int = board_size
        self.num_tiles: int = num_tiles
        self.tile_size: int = self.board_size // self.num_tiles
        self.selected_piece: Piece | None = None
        self.last_piece_to_take: Piece | None = None

        if board is None:
            self.board: List[List[int | Color]] = []

            # alternating black piece for the first 3 rows
            for i in range(3):
                self.board.append([])
                if i % 2:
                    for _ in range(self.num_tiles // 2):
                        self.board[-1].append(0)
                        self.board[-1].append(Color.BLACK)
                else:
                    for _ in range(self.num_tiles // 2):
                        self.board[-1].append(Color.BLACK)
                        self.board[-1].append(0)

            for _ in range(self.num_tiles - 6):
                self.board.append([0 for _ in range(self.num_tiles)])

            # alternating red piece for the last 3 rows
            for i in range(3):
                self.board.append([])
                if i % 2:
                    for _ in range(self.num_tiles // 2):
                        self.board[-1].append(Color.RED)
                        self.board[-1].append(0)
                else:
                    for _ in range(self.num_tiles // 2):
                        self.board[-1].append(0)
                        self.board[-1].append(Color.RED)
        else:
            self.board = board

        self.tiles_list = self._generate_tiles()

    def _generate_tiles(self) -> list[Tile]:
        """Creates a list of tiles for the board with the piece on the tiles according to self.board initialization"""
        tiles_list = []
        for i in range(self.num_tiles):
            for j in range(self.num_tiles):
                new_tile = Tile(i, j, self.tile_size)
                if self.board[i][j] == Color.BLACK:
                    new_tile.piece = Pawn((i, j), Color.BLACK, self, self.tile_size)
                elif self.board[i][j] == Color.RED:
                    new_tile.piece = Pawn((i, j), Color.RED, self, self.tile_size)
                tiles_list.append(new_tile)
        return tiles_list

    def draw(self, display) -> None:
        """Draws the board with the tiles and the piece one the tiles"""
        for tile in self.tiles_list:
            tile.draw(display)

    def get_tile_from_pos(self, x: int, y: int) -> Tile | None:
        """Expects parameters: x/col, y/row. Returns the tile at position (row, col)"""
        for tile in self.tiles_list:
            if (tile.x_index, tile.y_index) == (x, y):
                return tile
        return None

    def handle_click(self, x: int, y: int, takes_available: bool) -> None:
        """Highlights clicked tile, selects the piece on clicked tile if applicable, moves piece if applicable"""
        x = x // self.tile_size
        y = y // self.tile_size
        clicked_tile = self.get_tile_from_pos(x, y)

        if clicked_tile is None:
            raise Exception("clicked_tile is None in board.py :92")

        # selecet a piece if there is no piece selected yet
        if (
            self.selected_piece is None
            and clicked_tile.piece is not None
            and clicked_tile.piece == self.turn
        ):
            self.selected_piece = clicked_tile.piece

        # move a piece if applicable
        elif self.selected_piece is not None and self.selected_piece.move(
            clicked_tile, takes_available
        ):
            if (
                self.last_piece_to_take is None
                or len(self.last_piece_to_take.valid_takes()) == 0
            ):
                self.turn = Color.BLACK if self.turn == Color.RED else Color.RED
                self.last_piece_to_take = None

        # select another piece if there is a selected piece already
        elif clicked_tile.piece is not None and clicked_tile.piece.color == self.turn:
            self.selected_piece = clicked_tile.piece

        for tile in self.tiles_list:
            tile.highlight = False
        clicked_tile.highlight = True
