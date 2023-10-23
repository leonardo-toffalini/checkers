import pygame

class Tile:
    def __init__(self, row:int, col:int, tile_size:int):
        self.tile_size = tile_size
        self.x_abs = col * self.tile_size # absolute x position
        self.y_abs = row * self.tile_size # absolute y position

        self.x_index = col # column index
        self.y_index = row # row index

        self.color = 'dark' if (row + col) % 2 else 'light'
        self.draw_color = (220, 189, 194) if self.color == 'light' else (92, 75, 75)
        self.highlight_color = (100, 249, 83) if self.color == 'light' else (0, 200, 10)
        self.highlight = False

        self.piece = None

        self.rect = pygame.Rect(
            self.x_abs,
            self.y_abs,
            self.tile_size,
            self.tile_size
        )

    def __repr__(self):
        return f'Tile at position {self.x_abs, self.y_abs}'

    def draw(self, display):
        """ Draws a rectangle for each tile and renders the image of a piece on top of the tile if applicable """
        if self.highlight:
            pygame.draw.rect(display, self.highlight_color, self.rect)
        else:
            pygame.draw.rect(display, self.draw_color, self.rect)

        if self.piece is not None:
            cRect = self.piece.img.get_rect()
            cRect.center = self.rect.center
            display.blit(self.piece.img, cRect.topleft)