"""Competitors and the shared pie hand for the rhythm game."""

from time import monotonic


FACE_POSITIONS = {"left": -1.0, "right": 1.0}


class Player:
    """Track one competitor's input bindings, lanes, and match state."""

    def __init__(self, side, keys, lanes, face=None):
        if side not in FACE_POSITIONS:
            raise ValueError("side must be 'left' or 'right'")
        self.keys = tuple(keys)
        self.lanes = tuple(lanes)
        if len(self.keys) != 4 or len(self.lanes) != 4:
            raise ValueError("a player needs four keys and four lanes")

        self.side = side
        self.combo = 0
        self.score = 0
        self.face = face if face is not None else Face(side)

    def press(self, lane_index, time):
        if not 0 <= lane_index < len(self.lanes):
            raise IndexError("lane index must be between 0 and 3")
        return self.lanes[lane_index].try_hit(time)

    def add_combo(self):
        self.combo += 1

    def reset_combo(self):
        self.combo = 0


class Hand:
    """Move the shared pie hand along the line between the two faces."""

    MOVE_SPEED = 4.0  # Position units per second.

    def __init__(self):
        self.position = 0.0
        self.controlling_side = None
        self.animation_state = "idle"
        self._target_position = 0.0

    def pass_to(self, side):
        if side not in FACE_POSITIONS:
            raise ValueError("side must be 'left' or 'right'")
        self.controlling_side = side

    def push(self, direction, amount):
        """Queue a move using a side name or a sign (-1 left, +1 right)."""
        direction = FACE_POSITIONS.get(direction, direction)
        if direction not in (-1, 1):
            raise ValueError("direction must be 'left', 'right', -1, or 1")
        if amount < 0:
            raise ValueError("amount must be non-negative")
        target = self._target_position + direction * amount
        self._target_position = max(-1.0, min(1.0, target))
        self.animation_state = (
            "moving" if self.position != self._target_position else "idle"
        )

    def update(self, dt):
        """Advance the animation by dt seconds without overshooting."""
        distance = self._target_position - self.position
        step = self.MOVE_SPEED * max(0.0, dt)
        if abs(distance) <= step:
            self.position = self._target_position
            self.animation_state = "idle"
        elif distance > 0:
            self.position += step
        else:
            self.position -= step

    def reached(self, side):
        return self.position == FACE_POSITIONS[side]


class Face:
    """Draw one competitor and time their hit and pie-splat reactions."""

    HIT_DURATION = 0.18
    SPLAT_DURATION = 0.22

    def __init__(self, side):
        if side not in FACE_POSITIONS:
            raise ValueError("side must be 'left' or 'right'")
        self.side = side
        self.state = "idle"
        self._state_started = monotonic()

    def set_state(self, state):
        if state not in ("idle", "hit", "cream_pied"):
            raise ValueError("state must be 'idle', 'hit', or 'cream_pied'")
        if self.state == "cream_pied":
            return
        self.state = state
        self._state_started = monotonic()

    def draw(self, screen):
        import pygame

        elapsed = monotonic() - self._state_started
        if self.state == "hit" and elapsed >= self.HIT_DURATION:
            self.set_state("idle")

        width, height = screen.get_size()
        x = width // 7 if self.side == "left" else width * 4 // 5
        y = height // 5.5

        face = pygame.image.load('assets/Wet Hands/big-villager-face.png')
        face = pygame.transform.scale(face, (100, 100))
        screen.blit(face, (x, y))
        # radius = max(1, min(width, height) // 12)
        # ink = (46, 30, 29)
        # skin = (239, 149, 131) if self.state == "hit" else (247, 188, 139)
        # pygame.draw.circle(screen, skin, (x, y), radius)

        # eye_radius = max(1, radius // 9)
        # for eye_x in (x - radius // 3, x + radius // 3):
        #     pygame.draw.circle(screen, ink, (eye_x, y - radius // 4), eye_radius)
        # mouth = pygame.Rect(
        #     x - radius // 3, y, max(1, radius * 2 // 3), max(1, radius // 2)
        # )
        # pygame.draw.ellipse(screen, ink, mouth, width=0 if self.state == "hit" else eye_radius)

        if self.state == "cream_pied":
            progress = min(1.0, elapsed / self.SPLAT_DURATION)
            cream = (255, 248, 227)
            drops = (
                (0, 0, 0.8),
                (-0.65, -0.5, 0.3),
                (0.7, -0.3, 0.33),
                (-0.45, 0.65, 0.28),
                (0.45, 0.6, 0.35),
            )
            for dx, dy, size in drops:
                center = (x + round(dx * radius * progress), y + round(dy * radius * progress))
                pygame.draw.circle(screen, cream, center, max(1, round(size * radius * progress)))