import pygame
import numpy as np
import math
import random
from pygame.locals import *

# 初始化Pygame
pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF)
pygame.display.set_caption("2026跨年夜·烟花盛宴")
clock = pygame.time.Clock()
FPS = 60

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (255, 50, 50), (50, 255, 50), (50, 50, 255),
    (255, 255, 50), (255, 50, 255), (50, 255, 255)
]

# 烟花粒子类
class FireworkParticle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 8)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.gravity = 0.05
        self.life = 60 + random.randint(0, 30)
        self.alpha = 255

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.alpha = max(0, self.alpha - 4)

    def draw(self):
        if self.alpha > 0:
            temp_surface = pygame.Surface((4, 4), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface, (*self.color, self.alpha), (2, 2), 2)
            screen.blit(temp_surface, (int(self.x)-2, int(self.y)-2))

# 2026文字粒子类
class TextParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vy = random.uniform(-3, -1)
        self.vx = random.uniform(-0.5, 0.5)
        self.color = random.choice(COLORS)
        self.size = random.uniform(2, 4)
        self.life = 120 + random.randint(0, 40)
        self.alpha = 255

    def update(self):
        self.y += self.vy
        self.x += self.vx
        self.life -= 1
        self.alpha = max(0, self.alpha - 2)

    def draw(self):
        if self.alpha > 0:
            temp_surface = pygame.Surface((int(self.size*2), int(self.size*2)), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface, (*self.color, self.alpha), (int(self.size), int(self.size)), int(self.size))
            screen.blit(temp_surface, (int(self.x)-int(self.size), int(self.y)-int(self.size)))

# 粒子列表
firework_particles = []
text_particles = []

# 字体
font = pygame.font.SysFont("Arial", 180, bold=True)

# 主循环
running = True
while running:
    screen.fill(BLACK)
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            color = random.choice(COLORS)
            for _ in range(150):
                firework_particles.append(FireworkParticle(x, y, color))

    # 2026粒子效果
    if random.random() < 0.2:
        text_surf = font.render("2026", True, WHITE)
        text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
        x = random.randint(text_rect.left, text_rect.right)
        y = random.randint(text_rect.top, text_rect.bottom)
        if text_surf.get_at((x - text_rect.left, y - text_rect.top))[3] > 0:
            text_particles.append(TextParticle(x, y))

    # 更新烟花
    for p in firework_particles[:]:
        p.update()
        p.draw()
        if p.life <= 0:
            firework_particles.remove(p)

    # 更新文字粒子
    for p in text_particles[:]:
        p.update()
        p.draw()
        if p.life <= 0:
            text_particles.remove(p)

    # 半透明2026
    text_surf = font.render("2026", True, WHITE)
    text_surf.set_alpha(80)
    text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text_surf, text_rect)

    pygame.display.flip()

pygame.quit()