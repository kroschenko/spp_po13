import math
from datetime import datetime
import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Дерево Пифагора")
CLOCK = pygame.time.Clock()


def draw_tree(x, y, length, angle, tree_depth, wind_power):
    if tree_depth == 0 or length < 2:
        return

    wind_effect = wind_power * tree_depth

    x2 = x + length * math.cos(math.radians(angle + wind_effect))
    y2 = y - length * math.sin(math.radians(angle + wind_effect))

    red = min(139, 80 + tree_depth * 10)
    green = min(69, 40 + tree_depth * 5)
    blue = min(19, 10 + tree_depth)
    color = (red, green, blue)

    if tree_depth < 4:
        color = (34, 139, 34)

    pygame.draw.line(SCREEN, color, (int(x), int(y)), (int(x2), int(y2)), max(1, tree_depth // 2))

    new_len = length * 0.7
    draw_tree(x2, y2, new_len, angle - 35 - wind_power, tree_depth - 1, wind_power)
    draw_tree(x2, y2, new_len, angle + 35 - wind_power, tree_depth - 1, wind_power)


DEPTH = 10
WIND = 0
RUNNING = True

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                DEPTH = min(DEPTH + 1, 12)
            if event.key == pygame.K_DOWN:
                DEPTH = max(DEPTH - 1, 1)
            if event.key == pygame.K_LEFT:
                WIND -= 3
            if event.key == pygame.K_RIGHT:
                WIND += 3
            if event.key == pygame.K_SPACE:
                WIND = 0
            if event.key == pygame.K_s:
                SCREENSHOT_NAME = f"tree_{datetime.now().strftime('%H%M%S')}.png"
                pygame.image.save(SCREEN, SCREENSHOT_NAME)
                print(f"Сохранен: {SCREENSHOT_NAME}")

    SCREEN.fill((0, 0, 0))
    draw_tree(WIDTH // 2, HEIGHT - 100, 100, -90, DEPTH, WIND)

    FONT = pygame.font.Font(None, 24)
    TEXT1 = FONT.render(f"Глубина: {DEPTH} (↑↓)", True, (255, 255, 255))
    TEXT2 = FONT.render(f"Ветер: {WIND} (←→) | Space - сброс | S - скриншот", True, (255, 255, 255))
    SCREEN.blit(TEXT1, (10, 10))
    SCREEN.blit(TEXT2, (10, 35))

    pygame.display.flip()
    CLOCK.tick(60)

pygame.quit()
