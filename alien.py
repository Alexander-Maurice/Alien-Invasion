import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    # Класс, представляющий одного пришельца
    def __init__(self, screen, settings):
        super().__init__()

        self.screen = screen
        self.settings = settings

        # Загрузка изображения и создание прямоугольника из изображения
        self.image = pygame.image.load('alien3.png')
        self.rect = self.image.get_rect()

        # Каждый новый пришелец появляется в верхнем левом углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение точной горизонтальной позиции пришельца
        self.x = float(self.rect.x)

    def check_edges(self):
        # Возвращает True, если пришелец находится у края экрана
        self.screen_rect = self.screen.get_rect()
        if self.rect.right >= self.screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        # Перемещает пришельца вправо
        self.x += (self.settings.alien_speed_factor *
                   self.settings.fleet_direction)
        self.rect.x = self.x
