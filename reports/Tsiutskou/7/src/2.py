import pygame
import sys
import math
from datetime import datetime

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Дерево Пифагора")
clock = pygame.time.Clock()


def draw_tree(x, y, length, angle, depth, wind):
    if depth == 0 or length < 2:
        return

    wind_effect = wind * depth

    x2 = x + length * math.cos(math.radians(angle + wind_effect))
    y2 = y - length * math.sin(math.radians(angle + wind_effect))

    # Цвет (R, G, B) - от коричневого до зеленого
    r = min(139, 80 + depth * 10)
    g = min(69, 40 + depth * 5)
    b = min(19, 10 + depth)
    color = (r, g, b)

    if depth < 4:
        color = (34, 139, 34)  # Зеленый

    pygame.draw.line(screen, color, (int(x), int(y)), (int(x2), int(y2)), max(1, depth // 2))

    new_len = length * 0.7
    draw_tree(x2, y2, new_len, angle - 35 - wind, depth - 1, wind)
    draw_tree(x2, y2, new_len, angle + 35 - wind, depth - 1, wind)


depth = 10
wind = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                depth = min(depth + 1, 12)
            if event.key == pygame.K_DOWN:
                depth = max(depth - 1, 1)
            if event.key == pygame.K_LEFT:
                wind -= 3
            if event.key == pygame.K_RIGHT:
                wind += 3
            if event.key == pygame.K_SPACE:
                wind = 0
            if event.key == pygame.K_s:
                name = f"tree_{datetime.now().strftime('%H%M%S')}.png"
                pygame.image.save(screen, name)
                print(f"Сохранен: {name}")

    screen.fill((0, 0, 0))
    draw_tree(WIDTH // 2, HEIGHT - 100, 100, -90, depth, wind)

    font = pygame.font.Font(None, 24)
    text1 = font.render(f"Глубина: {depth} (↑↓)", True, (255, 255, 255))
    text2 = font.render(f"Ветер: {wind} (←→) | Space - сброс | S - скриншот", True, (255, 255, 255))
    screen.blit(text1, (10, 10))
    screen.blit(text2, (10, 35))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
