import pygame
import os
from utils.constantes import Couleur, TypePiece
from game.gamestate import GameState
class BoardView:
    def __init__(self, screen):
        self.width, self.height = screen.get_size()
        self.tile_size = min(self.width, self.height) // 8
        self.offset_x = (self.width - (self.tile_size * 8)) // 2
        self.offset_y = (self.height - (self.tile_size * 8)) // 2
        self.screen = screen
        self.images = {}
        self.load_images()
        
    def load_images(self):
        for couleur in Couleur: 
            for type_piece in TypePiece:
                # 1. Générer la clé d'accès (ex: 'wp' pour white-pawn)
                asset_key = f"{couleur.value}{type_piece.value}" 
                
                # 2. Construire le chemin du fichier (ex: "images/wp.png")
                chemin = os.path.join("images", f"{asset_key}.png")
                
                # 3. Charger et redimensionner l'image
                try:
                    image_originale = pygame.image.load(chemin)
                    
                    image_scale = pygame.transform.scale(
                        image_originale, 
                        (self.tile_size, self.tile_size)
                    )
                    # 4. Stocker l'image sous la clé générée (ex: self.images['wp'])
                    self.images[asset_key] = image_scale
                    
                except pygame.error as e:
                    # Cela permet de savoir si un fichier est manquant
                    print(f"Erreur: Fichier image manquant ou illisible : {chemin} | {e}")

    def draw_grid(self):

        light = (240, 217, 181)  # light squares
        dark  = (181, 136, 99)   # dark squares

        for row in range(8):
            for col in range(8):
                color = light if (row + col) % 2 == 0 else dark
                rect_x = self.offset_x + col * self.tile_size
                rect_y = self.offset_y + row * self.tile_size
                
                rect = pygame.Rect(rect_x, rect_y, self.tile_size, self.tile_size)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, color, rect)

    def draw_board(self, gamestate: GameState):
        board = gamestate.board
        self.draw_grid()
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece is None:
                    continue
                key = piece.get_asset_key()
                image = self.images.get(key)
                if image:
                    pos_x = self.offset_x + col * self.tile_size
                    pos_y = self.offset_y + row * self.tile_size
                    self.screen.blit(image, (pos_x, pos_y))
