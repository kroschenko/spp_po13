import pygame
import sys
from datetime import datetime

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Движение окружности")


class Circle:
    def __init__(self, x, y, r, sx, sy):
        self.x = x
        self.y = y
        self.r = r
        self.sx = sx
        self.sy = sy

    def move(self):
        self.x += self.sx
        self.y += self.sy

        if self.x - self.r <= 0 or self.x + self.r >= WIDTH:
            self.sx = -self.sx
        if self.y - self.r <= 0 or self.y + self.r >= HEIGHT:
            self.sy = -self.sy

    def draw(self):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), self.r)


circle = Circle(WIDTH // 2, HEIGHT // 2, 30, 5, 3)
running = True
paused = False
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            if event.key == pygame.K_s:
                name = f"screenshot_{datetime.now().strftime('%H%M%S')}.png"
                pygame.image.save(screen, name)
                print(f"Сохранен: {name}")

    screen.fill((0, 0, 0))

    if not paused:
        circle.move()

    circle.draw()

    font = pygame.font.Font(None, 24)
    status = "ПАУЗА" if paused else "ДВИЖЕНИЕ"
    color = (255, 255, 0) if paused else (0, 255, 0)
    text = font.render(f"{status} | Space - пауза | S - скриншот", True, color)
    screen.blit(text, (10, HEIGHT - 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
