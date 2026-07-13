import pygame
from datetime import datetime

pygame.init()

WIDTH = 800
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Движение окружности")


class Circle:
    def __init__(self, x_pos, y_pos, radius, speed_x, speed_y):
        self.x = x_pos
        self.y = y_pos
        self.r = radius
        self.sx = speed_x
        self.sy = speed_y

    def move(self):
        self.x += self.sx
        self.y += self.sy

        if self.x - self.r <= 0 or self.x + self.r >= WIDTH:
            self.sx = -self.sx
        if self.y - self.r <= 0 or self.y + self.r >= HEIGHT:
            self.sy = -self.sy

    def draw(self):
        pygame.draw.circle(SCREEN, (255, 0, 0), (int(self.x), int(self.y)), self.r)


CIRCLE = Circle(WIDTH // 2, HEIGHT // 2, 30, 5, 3)
RUNNING = True
PAUSED = False
CLOCK = pygame.time.Clock()

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                PAUSED = not PAUSED
            if event.key == pygame.K_s:
                SCREENSHOT_NAME = f"screenshot_{datetime.now().strftime('%H%M%S')}.png"
                pygame.image.save(SCREEN, SCREENSHOT_NAME)
                print(f"Сохранен: {SCREENSHOT_NAME}")

    SCREEN.fill((0, 0, 0))

    if not PAUSED:
        CIRCLE.move()

    CIRCLE.draw()

    FONT = pygame.font.Font(None, 24)
    STATUS_TEXT = "ПАУЗА" if PAUSED else "ДВИЖЕНИЕ"
    TEXT_COLOR = (255, 255, 0) if PAUSED else (0, 255, 0)
    TEXT_SURFACE = FONT.render(f"{STATUS_TEXT} | Space - пауза | S - скриншот", True, TEXT_COLOR)
    SCREEN.blit(TEXT_SURFACE, (10, HEIGHT - 30))

    pygame.display.flip()
    CLOCK.tick(60)

pygame.quit()
