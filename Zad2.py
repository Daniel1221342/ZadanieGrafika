import pygame
import sys
import math

pygame.init()
win = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Transformacje wielokąta foremnego")

BIALY = (255, 255, 255)
CZERWONY = (255, 0, 0)
CZARNY = (0, 0, 0)

font = pygame.font.SysFont(None, 24)
center_pos = (300, 300)

n = 15  # liczba boków
radius = 150


def create_polygon_surface():
    surface = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
    center = (radius, radius)
    points = []
    for i in range(n):
        angle = 2 * math.pi * i / n
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y))
    pygame.draw.polygon(surface, CZERWONY, points)
    return surface

original_surface = create_polygon_surface()

angle = 0
scale = 1.0
flip_h = False
flip_v = False
current_surface = original_surface.copy()

def draw_instructions():
    lines = [
        "1: Skalowanie 50%",
        "2: Obrót 45°",
        "3: Obrót 90°",
        "4: Pochylenie w lewo (symulacja)",
        "5: Odbicie poziome",
        "6: Pochylenie w prawo (symulacja)",
        "7: Odbicie pionowe",
        "8: Obrót 135°",
        "9: Skalowanie 150%",
        "R: Reset",
        "ESC: Wyjście"
    ]
    for i, line in enumerate(lines):
        text = font.render(line, True, CZARNY)
        win.blit(text, (10, 10 + i * 20))

def update_surface():
    global current_surface
    surface = original_surface.copy()
    surface = pygame.transform.flip(surface, flip_h, flip_v)
    size = surface.get_size()
    new_size = (int(size[0] * scale), int(size[1] * scale))
    if new_size[0] < 1 or new_size[1] < 1:
        new_size = (1, 1)
    surface = pygame.transform.scale(surface, new_size)
    surface = pygame.transform.rotate(surface, angle)
    current_surface = surface

def apply_transformation(key):
    global angle, scale, flip_h, flip_v
    if key == pygame.K_1:
        scale *= 0.5
    elif key == pygame.K_2:
        angle += 45
    elif key == pygame.K_3:
        angle += 90
    elif key == pygame.K_4:
        angle += 15  # symulacja pochylenia w lewo
    elif key == pygame.K_5:
        flip_h = not flip_h
    elif key == pygame.K_6:
        angle -= 15  # symulacja pochylenia w prawo
    elif key == pygame.K_7:
        flip_v = not flip_v
    elif key == pygame.K_8:
        angle += 135
    elif key == pygame.K_9:
        scale *= 1.5
    elif key == pygame.K_r:
        angle = 0
        scale = 1.0
        flip_h = False
        flip_v = False
    update_surface()

update_surface()
run = True
while run:
    win.fill(BIALY)
    draw_instructions()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            else:
                apply_transformation(event.key)

    rect = current_surface.get_rect(center=center_pos)
    win.blit(current_surface, rect.topleft)
    pygame.display.update()

pygame.quit()
sys.exit()
