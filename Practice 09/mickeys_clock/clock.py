import os
from datetime import datetime

import pygame

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")


class MickeyClock:
    def __init__(self):
        self.face = pygame.image.load(os.path.join(IMG, "clock_face.png")).convert_alpha()
        hand = pygame.image.load(os.path.join(IMG, "mickey_hand.png")).convert_alpha()
        self.center = pygame.math.Vector2(self.face.get_rect().center)

        self.minute_hand = self._scaled(hand, 170)
        self.second_hand = self._scaled(hand, 200)

    @staticmethod
    def _scaled(image, length):
        w, h = image.get_size()
        return pygame.transform.smoothscale(image, (round(w * length / h), length))

    def _draw_hand(self, screen, image, angle):
        offset = pygame.math.Vector2(0, -image.get_height() / 2).rotate(angle)
        rotated = pygame.transform.rotate(image, -angle)  
        screen.blit(rotated, rotated.get_rect(center=self.center + offset))

    def draw(self, screen):
        now = datetime.now()
        seconds = min(now.second, 59)        
        screen.blit(self.face, (0, 0))
        self._draw_hand(screen, self.minute_hand, (now.minute + seconds / 60) * 6)  
        self._draw_hand(screen, self.second_hand, seconds * 6)                   
        
