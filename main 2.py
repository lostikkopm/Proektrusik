import pygame
import math
import random
import os

pygame.init()
WIDTH, HEIGHT = 600, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snow Fort Defense ❄️")

BACKGROUND = pygame.image.load("images/fon/fon1.png")
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))

TOWER_IMG = pygame.image.load("images/hq720-removebg-preview.png")
TOWER_IMG = pygame.transform.scale(TOWER_IMG, (50, 50))

ENEMY_IMG = pygame.image.load("images/Tower-Defense-Monster-2D-Sprites-removebg-preview.png")
ENEMY_IMG = pygame.transform.scale(ENEMY_IMG, (40, 40))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 150, 255)
BLACK = (0, 0, 0)


class Enemy:
    def __init__(self, path):
        self.path = path
        self.x, self.y = path[0]
        self.health = 100
        self.speed = 1.0
        self.path_index = 0
        self.alive = True
        self.img = ENEMY_IMG

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
        win.blit(self.img, (self.x - 20, self.y - 20))

        # health bar
        pygame.draw.rect(win, RED, (self.x - 20, self.y - 30, 40, 5))
        pygame.draw.rect(win, GREEN, (self.x - 20, self.y - 30, 40 * (self.health / 100), 5))


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
        self.x, self.y = x, y
        self.range = 120
        self.cooldown = 0
        self.reload_time = 60
        self.bullets = []
        self.img = TOWER_IMG

    def shoot(self, enemies):
        if self.cooldown > 0:
            self.cooldown -= 1
            return

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
        win.blit(self.img, (self.x - 25, self.y - 25))
        pygame.draw.circle(win, (150,150,150), (int(self.x), int(self.y)), self.range, 1)
        for b in self.bullets:
            b.draw(win)


PATH = [(50, 750), (50, 400), (200, 400), (200, 750), (550, 750), (550, 500), (300, 500), (300, 150), (550, 150), (550, 50)]
# PATH = [(50, 750), (50, 400), (300, 400), (300, 150), (550, 150), (550, 50)]
reached_end = 0 # ⬅️⬅️⬅️
font = pygame.font.SysFont(None, 36) # ⬅️⬅️⬅️

def main():
    global reached_end # ⬅️⬅️⬅️
    clock = pygame.time.Clock()
    run = True
    towers = []
    enemies = []
    wave_timer = 0
    spawn_delay = 60

    while run:
        clock.tick(60)
        WIN.blit(BACKGROUND, (0, 0))

        wave_timer += 1
        if wave_timer >= spawn_delay:
            enemies.append(Enemy(PATH))
            wave_timer = 0

        for e in enemies:
            e.move()
            if not e.alive and e.path_index + 1 >= len(e.path): # ⬅️⬅️⬅️
                reached_end += 1 # ⬅️⬅️⬅️
        text = font.render(f"Enemies reached end: {reached_end}", True, WHITE) # ⬅️⬅️⬅️
        WIN.blit(text, (10, 10)) # ⬅️⬅️⬅️
        enemies = [e for e in enemies if e.alive]

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

        for e in enemies:
            e.draw(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if len(towers) < 10:
                    x, y = pygame.mouse.get_pos()
                    towers.append(Tower(x, y))

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()