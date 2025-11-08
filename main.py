import pygame
import math
import random
import os

# Ініціалізація
pygame.init()
WIDTH, HEIGHT = 600, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snow Fort Defense ❄️")

# Завантаження фону
BACKGROUND = pygame.image.load("images/fon/fon1.png")
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))

# Кольори
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 150, 255)
BLACK = (0, 0, 0)

# Класи
class Enemy:
    def __init__(self, path):
        self.path = path
        self.x, self.y = path[0]
        self.health = 100
        self.speed = 1.0
        self.path_index = 0
        self.alive = True

    def move(self):
        if self.path_index + 1 >= len(self.path):
            self.alive = False
            return
        x1, y1 = self.path[self.path_index]
        x2, y2 = self.path[self.path_index + 1]
        dir_vector = (x2 - x1, y2 - y1)
        distance = math.hypot(*dir_vector)
        dir_vector = (dir_vector[0] / distance, dir_vector[1] / distance)
        self.x += dir_vector[0] * self.speed
        self.y += dir_vector[1] * self.speed

        if math.hypot(x2 - self.x, y2 - self.y) < 2:
            self.path_index += 1

    def draw(self, win):
        pygame.draw.circle(win, RED, (int(self.x), int(self.y)), 10)
        pygame.draw.rect(win, RED, (self.x - 15, self.y - 20, 30, 5))
        pygame.draw.rect(win, GREEN, (self.x - 15, self.y - 20, 30 * (self.health / 100), 5))

class Bullet:
    def __init__(self, x, y, target):
        self.x, self.y = x, y
        self.target = target
        self.speed = 5

    def move(self):
        if not self.target.alive:
            return
        dx, dy = self.target.x - self.x, self.target.y - self.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.x += dx / dist * self.speed
            self.y += dy / dist * self.speed

    def draw(self, win):
        pygame.draw.circle(win, BLUE, (int(self.x), int(self.y)), 5)

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 120
        self.cooldown = 0
        self.reload_time = 60  # кадрів між пострілами
        self.bullets = []

    def shoot(self, enemies):
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        # Знаходимо найближчого ворога в межах радіуса
        nearest = None
        nearest_dist = self.range
        for e in enemies:
            dist = math.hypot(self.x - e.x, self.y - e.y)
            if dist < nearest_dist and e.alive:
                nearest = e
                nearest_dist = dist

        if nearest:
            self.bullets.append(Bullet(self.x, self.y, nearest))
            self.cooldown = self.reload_time

    def draw(self, win):
        pygame.draw.circle(win, BLACK, (int(self.x), int(self.y)), 15)
        pygame.draw.circle(win, (150,150,150), (int(self.x), int(self.y)), self.range, 1)
        for b in self.bullets:
            b.draw(win)

# Створюємо доріжку (path)
PATH = [(50, 750), (50, 400), (300, 400), (300, 150), (550, 150), (550, 50)]

def main():
    clock = pygame.time.Clock()
    run = True
    towers = []
    enemies = []
    wave_timer = 0
    spawn_delay = 60

    while run:
        clock.tick(60)
        WIN.blit(BACKGROUND, (0, 0))

        # Створення ворогів
        wave_timer += 1
        if wave_timer >= spawn_delay:
            enemies.append(Enemy(PATH))
            wave_timer = 0

        # Рух ворогів
        for e in enemies:
            e.move()

        # Видалення мертвих ворогів
        enemies = [e for e in enemies if e.alive]

        # Башти
        for t in towers:
            t.shoot(enemies)
            for b in t.bullets:
                b.move()
                for e in enemies:
                    if math.hypot(b.x - e.x, b.y - e.y) < 10:
                        e.health -= 20
                        if e.health <= 0:
                            e.alive = False
                        if b in t.bullets:
                            t.bullets.remove(b)
                            break
            t.draw(WIN)

        # Малюємо ворогів
        for e in enemies:
            e.draw(WIN)

        # Події
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                towers.append(Tower(x, y))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
