import pygame
import sys
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    def __init__(self):
        pygame.init()

        self.ai_settings = Settings()
        self.screen = pygame.display.set_mode(
            (0, 0), pygame.FULLSCREEN)
        self.ai_settings.screen_width = self.screen.get_rect().width
        self.ai_settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')
        self.bg_color = (self.ai_settings.bg_color)

        # Создание экземпляра для хранения игровой статистики
        self.stats = GameStats(self.ai_settings)
        self.sb = Scoreboard(self.screen, self.ai_settings, self.stats)

        self.ship = Ship(self.screen, self.ai_settings)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.create_fleet()

        # Создание кнопки Play
        self.play_button = Button(self.screen, 'Play')

    def run_game(self):
        while True:
            self.check_events()
            if self.stats.game_active:
                self.ship.update()
                self.update_bullets()
                self.update_aliens()
            self.update_screen()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)

    def check_play_button(self):
        # Запускает новую игру при нажатии кнопки Play
        # button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if not self.stats.game_active:
            # Сброс игровых настроек
            self.ai_settings.initialize_dynamic_settings()

            # Сброс игровой статистики
            self.stats.reset_stats()
            self.stats.game_active = True

            # Очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещения корабля в центре
            self.create_fleet()
            self.ship.center_ship()

            # Указатель мыши скрывается
            pygame.mouse.set_visible(False)

            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

    def check_keydown_events(self, event):
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        # elif event.key == pygame.K_DOWN:
        #     self.ship.moving_down = True
        # elif event.key == pygame.K_UP:
        #     self.ship.moving_up = True
        elif event.key == pygame.K_SPACE:
            self.fire_bullet(self.screen, self.ai_settings, self.ship)
        elif event.key == pygame.K_p:
            # mouse_pos = pygame.mouse.get_pos()
            self.check_play_button()
        elif event.key == pygame.K_q:
            sys.exit()

    def check_keyup_events(self, event):
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        # elif event.key == pygame.K_DOWN:
        #     self.ship.moving_down = False
        # elif event.key == pygame.K_UP:
        #     self.ship.moving_up = False

    def fire_bullet(self, screen, ai_settings, ship):
        if len(self.bullets) < self.ai_settings.bullet_allowed:
            new_bullet = Bullet(screen, ai_settings, ship)
            self.bullets.add(new_bullet)

    def update_bullets(self):
        # Обновление позиции снарядов
        self.bullets.update()

        # Удаление снарядов, дошедших до края экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self.check_bullet_alien_collisions()

    def check_bullet_alien_collisions(self):
        # Проверка попаданий в пришельцев
        # При обнаружении попадания удалить снаряд и пришельца
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            self.stats.score += self.ai_settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Уничтожить существующие снаряды и создать новый флот
            self.bullets.empty()
            self.create_fleet()
            self.ai_settings.increase_speed()

            # Увеличение уровня
            self.stats.level += 1
            self.sb.prep_level()

    def create_fleet(self):
        # Создает флот прищельцев
        # Создание пришельца и вычисление количества пришельцев в ряду
        # Интервал между соседними пришельцами равен ширине пришельца

        alien = Alien(self.screen, self.ai_settings)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.ai_settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Определяем количество рядов, помешающихся на экране
        ship_height = self.ship.rect.height
        available_space_y = (self.ai_settings.screen_height -
                             (6 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Создание флота вторжения
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self.create_alien(alien_number, alien_width,
                                  alien_height, row_number)

    def create_alien(self, alien_number, alien_width, alien_height, row_number):
        # Создание пришельца и размещение его в ряду
        alien = Alien(self.screen, self.ai_settings)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def update_aliens(self):
        # Обновляет позиции всех пришельцев во флоте
        self.check_fleet_edges()
        self.aliens.update()

        # Проверка коллизий пришелец - корабль
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship_hit()

        # Проверить, добрались ли пришельцы до нижнего края
        self.check_aliens_bottom()

    def check_fleet_edges(self):
        # Реагирует на достижение пришельцем края
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        # Опускает весь флот и меняет направление флота
        for alien in self.aliens.sprites():
            alien.rect.y += self.ai_settings.fleet_drop_speed
        self.ai_settings.fleet_direction *= - 1

    def ship_hit(self):
        # Обрабатывает столкновение корабля с пришельцем
        if self.stats.ships_left > 0:
            # Уменьшение ship_left
            self.stats.ships_left -= 1
            self.sb.prep_ships()

        # Очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

        # Создание нового флота и размещение корабля в центре
            self.create_fleet()
            self.ship.center_ship()

        # Пауза
            sleep(0.5)
        else:
            self.stats.game_active = False

    def check_aliens_bottom(self):
        # Проверяет добрались ли пришельцы до нижнего края
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self.ship_hit
                break

    def update_screen(self):
        self.screen.fill(self.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Вывод информации о счете
        self.sb.show_score()

        # Кнопка Play отображается в том случае, если игра неактивна
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    ai_game = AlienInvasion()
    ai_game.run_game()
