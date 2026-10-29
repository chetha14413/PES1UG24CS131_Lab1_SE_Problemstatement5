"""
GameEngine: owns all balloons, spawns new ones, and handles clicks.

Balloons have normal, bonus, and penalty types with different point
values. Click detection uses the balloon's visible circular radius.
"""

import random
import math

from game.balloon import Balloon
from game.click_detection import check_pop
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 45
STARTING_LIVES = 3
ROUND_DURATION_SECONDS = 30


class GameEngine:
    def __init__(self):
        self.start_new_round()

    def start_new_round(self):
        self.balloons = []
        self.frames_until_spawn = 0
        self.score = 0
        self.lives = STARTING_LIVES
        self.time_remaining = ROUND_DURATION_SECONDS
        self.is_active = True

    def _spawn_balloon(self):
        radius = random.randint(16, 44)
        x = random.randint(radius + 10, WIDTH - radius - 10)
        speed = random.uniform(1.5, 3.0)
        balloon_type = random.choice(("normal", "bonus", "penalty"))
        self.balloons.append(
            Balloon(
                x=x,
                y=-radius,
                radius=radius,
                speed=speed,
                balloon_type=balloon_type,
            )
        )

    def handle_click(self, pos):
        if not self.is_active:
            return

        popped = check_pop(self.balloons, pos)
        if popped is not None:
            self.balloons.remove(popped)
            self.score += popped.points

    def update(self, delta_seconds):
        if not self.is_active:
            return

        self.time_remaining = max(0, self.time_remaining - delta_seconds)
        if self.time_remaining == 0:
            self.is_active = False
            return

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_balloon()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for b in self.balloons:
            b.update()

        missed = [b for b in self.balloons if b.is_past_bottom(HEIGHT)]
        self.balloons = [b for b in self.balloons if not b.is_past_bottom(HEIGHT)]
        self.lives = max(0, self.lives - len(missed))
        if self.lives == 0:
            self.is_active = False

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.balloons)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Lives: {self.lives}", (10, 38))
        remaining_seconds = math.ceil(self.time_remaining)
        renderer.draw_text(surface, font, f"Time: {remaining_seconds}", (10, 66))
        if not self.is_active:
            renderer.draw_banner(surface, font, "Game Over")
            final_score = f"Final Score: {self.score}"
            final_score_width = font.size(final_score)[0]
            renderer.draw_text(
                surface,
                font,
                final_score,
                ((WIDTH - final_score_width) // 2, HEIGHT // 2 + 24),
            )
            renderer.draw_text(
                surface,
                font,
                "Press R to start a new round",
                (WIDTH // 2 - 150, HEIGHT // 2 + 54),
            )
