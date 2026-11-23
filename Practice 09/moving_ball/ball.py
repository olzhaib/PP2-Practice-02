import pygame

RED = (255, 0, 0)


class Ball:
    RADIUS = 25
    STEP = 20

    def __init__(self, x, y):
        self.x = x 
        self.y = y

    def move(self, dx, dy, screen_w, screen_h):
        new_x = self.x + dx * self.STEP
        new_y = self.y + dy * self.STEP
        inside = (self.RADIUS <= new_x <= screen_w - self.RADIUS and
                  self.RADIUS <= new_y <= screen_h - self.RADIUS)
        if inside:
            self.x, self.y = new_x, new_y
        return inside

    def draw(self, surface):
        pygame.draw.circle(surface, RED, (self.x, self.y), self.RADIUS)
