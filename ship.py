import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    # Класс для управления кораблем

    def __init__(self, screen, ai_settings):
        # Инициализирует корабль и его начальную позицию

        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.image = pygame.image.load('ship2.png')
        self.rect = self.image.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Передвижение
        self.moving_left = False
        self.moving_right = False
        # self.moving_down = False
        # self.moving_up = False

        # Сохранение вещественной координаты корабля
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.ai_settings.ship_speed_factor
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.ai_settings.ship_speed_factor
        # if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
        #     self.y += self.ai_settings.ship_speed_factor
        # if self.moving_up and self.rect.top > self.screen_rect.top:
        #     self.y -= self.ai_settings.ship_speed_factor

        self.rect.x = self.x
        # self.rect.y = self.y

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        # Размещает корабль в центре нижней стороны
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
