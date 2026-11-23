import pygame
import math

def make_rect(start, end):
    x = min(start[0], end[0])
    y = min(start[1], end[1])

    width = abs(end[0] - start[0])
    height = abs(end[1] - start[1])

    return pygame.Rect(x, y, width, height)

def draw_shape(surface, tool, color, start, end, size):

    x1, y1 = start
    x2, y2 = end

    if tool == "line":
        pygame.draw.line(surface, color, start, end, size)

    elif tool == "rectangle":
        pygame.draw.rect(surface, color, make_rect(start, end), size)

    elif tool == "square":
        side = min(abs(x2 - x1), abs(y2 - y1))

        x = x1 + side if x2 >= x1 else x1 - side
        y = y1 + side if y2 >= y1 else y1 - side

        pygame.draw.rect(surface, color,
                         make_rect(start, (x, y)), size)

    elif tool == "circle":
        radius = int(math.hypot(x2 - x1, y2 - y1))

        if radius > 0:
            pygame.draw.circle(surface, color, start, radius, size)

    elif tool == "right_triangle":
        points = [(x1, y1), (x1, y2), (x2, y2)]
        pygame.draw.polygon(surface, color, points, size)

    elif tool == "equilateral_triangle":
        height = abs(x2 - x1) * math.sqrt(3) / 2

        y = y1 - height if y2 < y1 else y1 + height

        points = [(x1, y1), (x2, y1), ((x1 + x2) / 2, y)]

        pygame.draw.polygon(surface, color, points, size)

    elif tool == "rhombus":
        middle_x = (x1 + x2) / 2
        middle_y = (y1 + y2) / 2

        points = [
            (middle_x, y1),
            (x2, middle_y),
            (middle_x, y2),
            (x1, middle_y)
        ]

        pygame.draw.polygon(surface, color, points, size)

def flood_fill(surface, pos, new_color):

    x, y = pos
    width, height = surface.get_size()

    if not (0 <= x < width and 0 <= y < height):
        return

    old_color = surface.get_at((x, y))[:3]
    new_color = tuple(new_color[:3])

    if old_color == new_color:
        return

    stack = [(x, y)]

    while stack:

        x, y = stack.pop()

        if 0 <= x < width and 0 <= y < height:

            if surface.get_at((x, y))[:3] == old_color:

                surface.set_at((x, y), new_color)

                stack.append((x + 1, y))
                stack.append((x - 1, y))
                stack.append((x, y + 1))
                stack.append((x, y - 1))

def draw_text(surface, font, text, pos, color):

    image = font.render(text, True, color)
    surface.blit(image, pos)
