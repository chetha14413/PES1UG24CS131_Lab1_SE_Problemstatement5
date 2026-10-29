"""
Balloon: falls from the top of the screen. The player must pop it
before it reaches the bottom. Balloons vary in size - this matters for
how click detection should work.
"""

import pygame


BALLOON_TYPES = {
    "normal": {"color": (220, 90, 120), "points": 10},
    "bonus": {"color": (255, 190, 40), "points": 25},
    "penalty": {"color": (90, 110, 220), "points": -15},
}


class Balloon:
    def __init__(self, x, y, radius, speed, balloon_type="normal"):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.balloon_type = balloon_type
        self.color = BALLOON_TYPES[balloon_type]["color"]
        self.points = BALLOON_TYPES[balloon_type]["points"]

    def update(self):
        self.y += self.speed

    def is_past_bottom(self, height):
        return self.y - self.radius > height

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.radius), int(self.y - self.radius),
            self.radius * 2, self.radius * 2,
        )
