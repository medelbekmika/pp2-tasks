import pygame
import math
# draw circle using radius from drag distance
def draw_circle(surface, start, end, color, thickness):
    radius = int(((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5)
    if radius > 0:
        pygame.draw.circle(surface, color, start, radius, thickness)

# draw square with equal sides
def draw_square(surface, start, end, color, thickness):
    size = min(abs(end[0] - start[0]), abs(end[1] - start[1]))
    if size > 0:
        rect = pygame.Rect(start[0], start[1], size, size)
        pygame.draw.rect(surface, color, rect, thickness)

# draw right triangle
def draw_right_triangle(surface, start, end, color, thickness):
    points = [
        start,
        (start[0], end[1]),
        (end[0], end[1])
    ]
    pygame.draw.polygon(surface, color, points, thickness)

# draw equilateral triangle
def draw_equilateral_triangle(surface, start, end, color, thickness):
    side = abs(end[0] - start[0])
    if side == 0:
        return
    height = int(side * math.sqrt(3) / 2)
    points = [
        (start[0], start[1]),
        (start[0] + side, start[1]),
        (start[0] + side // 2, start[1] - height)
    ]
    pygame.draw.polygon(surface, color, points, thickness)

# draw rhombus (diamond shape)
def draw_rhombus(surface, start, end, color, thickness):
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2
    dx = abs(end[0] - start[0]) // 2
    dy = abs(end[1] - start[1]) // 2
    points = [
        (cx, cy - dy),
        (cx + dx, cy),
        (cx, cy + dy),
        (cx - dx, cy)
    ]
    pygame.draw.polygon(surface, color, points, thickness)

# flood fill using BFS
def flood_fill(surface, pos, fill_color):
    x = pos[0]
    y = pos[1]
    width = surface.get_width()
    height = surface.get_height()

    if x < 0 or x >= width or y < 0 or y >= height:
        return

    target_color = surface.get_at((x, y))[:3]
    fill_rgb = fill_color[:3]

    if target_color == fill_rgb:
        return

    queue = []
    queue.append((x, y))
    visited = set()
    visited.add((x, y))

    while len(queue) > 0:
        cx, cy = queue.pop(0)
        surface.set_at((cx, cy), fill_color)

        # check 4 neighbors
        neighbors = [(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)]
        for nx, ny in neighbors:
            if 0 <= nx < width and 0 <= ny < height:
                if (nx, ny) not in visited:
                    if surface.get_at((nx, ny))[:3] == target_color:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
