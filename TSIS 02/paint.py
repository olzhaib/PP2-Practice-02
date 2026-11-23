
import os
from datetime import datetime

import pygame
from tools import draw_shape, flood_fill, draw_text

pygame.init()

WIDTH = 900
HEIGHT = 600
TOOLBAR_HEIGHT = 100

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()
pygame.key.set_repeat(400, 40)

font = pygame.font.SysFont("arial", 16)
text_font = pygame.font.SysFont("arial", 28)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (210, 210, 210)

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

tools = [
    ("Pencil", "pencil"),
    ("Line", "line"),
    ("Rect", "rectangle"),
    ("Square", "square"),
    ("Circle", "circle"),
    ("R-Tri", "right_triangle"),
    ("Eq-Tri", "equilateral_triangle"),
    ("Rhombus", "rhombus"),
    ("Eraser", "eraser"),
    ("Fill", "fill"),
    ("Text", "text")
]

tool_buttons = []
for i, (label, name) in enumerate(tools):
    rect = pygame.Rect(5 + i * 81, 8, 78, 32)
    tool_buttons.append((label, name, rect))

colors = [
    BLACK, WHITE, (255, 0, 0), (0, 160, 0), (0, 0, 255),
    (255, 255, 0), (255, 140, 0), (150, 0, 200),
    (140, 80, 20), (128, 128, 128)
]

color_buttons = []
for i, c in enumerate(colors):
    rect = pygame.Rect(5 + i * 34, 55, 28, 28)
    color_buttons.append((c, rect))

sizes = [2, 5, 10]

size_buttons = []
for i, value in enumerate(sizes):
    rect = pygame.Rect(370 + i * 125, 55, 120, 28)
    size_buttons.append((value, rect))

tool = "pencil"
color = BLACK
size = 5

drawing = False
start_pos = None
last_pos = None

typing = False
text = ""
text_pos = None

message = ""
message_time = 0


def stroke(start, end, draw_color, width):
    pygame.draw.line(canvas, draw_color, start, end, width)
    pygame.draw.circle(canvas, draw_color, end, width // 2)


def draw_toolbar():
    screen.fill(GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    for label, name, rect in tool_buttons:
        button_color = (120, 190, 255) if name == tool else WHITE
        pygame.draw.rect(screen, button_color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        screen.blit(font.render(label, True, BLACK),
                    (rect.x + 8, rect.y + 7))

    for c, rect in color_buttons:
        pygame.draw.rect(screen, c, rect)

        border = (255, 0, 255) if c == color else BLACK
        pygame.draw.rect(screen, border, rect, 3)

    for value, rect in size_buttons:
        button_color = (120, 190, 255) if value == size else WHITE
        pygame.draw.rect(screen, button_color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        label = f"{value} px"
        screen.blit(font.render(label, True, BLACK),
                    (rect.x + 35, rect.y + 5))

    hint = message if pygame.time.get_ticks() < message_time else "Ctrl+S - Save"
    screen.blit(font.render(hint, True, BLACK), (5, 85))


running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if typing:

                if event.key == pygame.K_RETURN:
                    if text:
                        draw_text(canvas, text_font, text, text_pos, color)
                    typing = False

                elif event.key == pygame.K_ESCAPE:
                    typing = False

                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]

                elif event.unicode and event.unicode.isprintable():
                    text += event.unicode

            elif event.key == pygame.K_s and event.mod & pygame.KMOD_CTRL:

                filename = "paint_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"

                path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

                pygame.image.save(canvas, path)

                message = "Saved: " + filename
                message_time = pygame.time.get_ticks() + 3000

            elif event.key == pygame.K_1:
                size = 2

            elif event.key == pygame.K_2:
                size = 5

            elif event.key == pygame.K_3:
                size = 10

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            mx, my = event.pos

            if my < TOOLBAR_HEIGHT:

                typing = False

                for label, name, rect in tool_buttons:
                    if rect.collidepoint(event.pos):
                        tool = name

                for c, rect in color_buttons:
                    if rect.collidepoint(event.pos):
                        color = c

                for value, rect in size_buttons:
                    if rect.collidepoint(event.pos):
                        size = value

            # Canvas
            else:

                pos = (mx, my - TOOLBAR_HEIGHT)

                if tool == "text":
                    typing = True
                    text = ""
                    text_pos = pos

                elif tool == "fill":
                    flood_fill(canvas, pos, color)

                else:
                    drawing = True
                    start_pos = pos
                    last_pos = pos

                    if tool == "pencil":
                        stroke(pos, pos, color, size)

                    elif tool == "eraser":
                        stroke(pos, pos, WHITE, size * 3)

        elif event.type == pygame.MOUSEMOTION and drawing:

            mx, my = event.pos
            pos = (mx, my - TOOLBAR_HEIGHT)

            if tool == "pencil":
                stroke(last_pos, pos, color, size)
                last_pos = pos

            elif tool == "eraser":
                stroke(last_pos, pos, WHITE, size * 3)
                last_pos = pos

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drawing:

            end_pos = (event.pos[0], event.pos[1] - TOOLBAR_HEIGHT)

            if tool not in ("pencil", "eraser"):
                draw_shape(canvas, tool, color, start_pos, end_pos, size)

            drawing = False

  
    picture = canvas.copy()

    if drawing and tool not in ("pencil", "eraser"):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        end_pos = (mouse_x, mouse_y - TOOLBAR_HEIGHT)

        draw_shape(picture, tool, color, start_pos, end_pos, size)

    screen.blit(picture, (0, TOOLBAR_HEIGHT))


    if typing:
        cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""
        shown_text = text_font.render(text + cursor, True, color)

        screen.blit(shown_text,
                    (text_pos[0], text_pos[1] + TOOLBAR_HEIGHT))

    draw_toolbar()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
