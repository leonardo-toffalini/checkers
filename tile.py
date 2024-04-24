from typing import Tuple
import pygame

import piece


class Tile:
    def __init__(self, row: int, col: int, tile_size: int) -> None:
        self.tile_size = tile_size
        self.x_abs = col * self.tile_size  # absolute x position
        self.y_abs = row * self.tile_size  # absolute y position

        self.x_index = col  # column index
        self.y_index = row  # row index

        self.color: str = "dark" if (row + col) % 2 else "light"
        self.draw_color: Tuple[int, int, int] = (
            (220, 189, 194) if self.color == "light" else (92, 75, 75)
        )
        self.highlight_color: Tuple[int, int, int] = (
            (100, 249, 83) if self.color == "light" else (0, 200, 10)
        )
        self.highlight: bool = False

        self.piece: piece.Piece | None = None

        self.rect = pygame.Rect(self.x_abs, self.y_abs, self.tile_size, self.tile_size)

    def __repr__(self) -> str:
        return f"Tile at position {self.x_index, self.y_index}"

    def draw(self, display) -> None:
        """Draws a rectangle for each tile and renders the image of a piece on top of the tile if applicable"""
        if self.highlight:
            pygame.draw.rect(display, self.highlight_color, self.rect)
        else:
            pygame.draw.rect(display, self.draw_color, self.rect)

        if self.piece is not None:
            cRect = self.piece.img.get_rect()
            cRect.center = self.rect.center
            display.blit(self.piece.img, cRect.topleft)
