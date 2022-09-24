import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, screen, ai_settings, ship):
        super().__init__()

        self.ship = ship
        self.screen = screen
        self.settings = ai_settings
        self.color = ai_settings.bullet_color

        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = self.ship.rect.midtop

        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
