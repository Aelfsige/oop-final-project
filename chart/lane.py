import pygame
from utils import time_to_screen_y


class Lane:
    """One of a player's four key columns."""
    LOOKAHEAD = 1.6      # seconds a note is visible before its hit time
    WIDTH = 70
    SPAWN_Y = 270
    MISS_LINGER = 0.4    # missed notes keep falling this long, then vanish

    def __init__(self, key, x, hit_line_y, judgement, notes=(), color=(255, 255, 255)):
        self.key = key
        self.x = x
        self.hit_line_y = hit_line_y
        self.judgement = judgement
        self.color = color
        self._queue = sorted(notes, key=lambda n: n.time)  # not yet spawned
        self.active_notes = []
        self._song_time = 0.0
        self._pressed_at = -99.0
        self._font = None

    def spawn_notes(self, song_time):
        while self._queue and self._queue[0].time - song_time <= self.LOOKAHEAD:
            self.active_notes.append(self._queue.pop(0))

    def update(self, song_time):
        """Auto-miss late notes, drop finished ones. Returns newly missed notes."""
        self._song_time = song_time
        newly_missed = []
        keep = []
        for note in self.active_notes:
            was_pending = note.state == "pending"
            note.update(song_time, self.judgement.late_window)
            if was_pending and note.state == "missed":
                newly_missed.append(note)
            if note.state == "hit":
                continue
            if note.state == "missed" and song_time > note.time + self.MISS_LINGER:
                continue
            keep.append(note)
        self.active_notes = keep
        return newly_missed

    def try_hit(self, press_time):
        """Grade the nearest pending note. Returns a grade string, or None if no note in range."""
        self._pressed_at = press_time
        pending = [n for n in self.active_notes if n.state == "pending"]
        if not pending:
            return None
        note = min(pending, key=lambda n: abs(n.time - press_time))
        if abs(note.time - press_time) > self.judgement.late_window:
            return None                      # ghost tap: nothing close enough
        grade = self.judgement.judge(press_time, note.time)
        note.state = "missed" if grade == "miss" else "hit"
        return grade

    @property
    def finished(self):
        return not self._queue and not self.active_notes

    def draw(self, screen):
        if self._font is None:
            self._font = pygame.font.Font(None, 32)
        top = self.SPAWN_Y
        rect = pygame.Rect(self.x, top, self.WIDTH, self.hit_line_y + 40 - top)
        pygame.draw.rect(screen, (28, 28, 40), rect, border_radius=8)
        pressed = self._song_time - self._pressed_at < 0.10
        line_rect = pygame.Rect(self.x, self.hit_line_y - 12, self.WIDTH, 24)
        pygame.draw.rect(screen, self.color if pressed else (70, 70, 90), line_rect,
                         width=0 if pressed else 3, border_radius=8)
        for note in self.active_notes:
            y = time_to_screen_y(note.time, self._song_time, self.hit_line_y,
                                 self.SPAWN_Y, self.LOOKAHEAD)
            col = (90, 90, 100) if note.state == "missed" else self.color

            note = pygame.image.load('assets/Wet Hands/mania-note1@2x.png').convert()
            note = pygame.transform.scale(note, (self.WIDTH - 12, 22))

            screen.blit(note, (self.x + 6, y - 11))

            # pygame.draw.rect(screen, col,
            #                  pygame.Rect(self.x + 6, y - 11, self.WIDTH - 12, 22),
            #                  border_radius=8)
        label = self._font.render(pygame.key.name(self.key).upper(), True, (230, 230, 240))
        screen.blit(label, label.get_rect(center=(self.x + self.WIDTH // 2, self.hit_line_y + 28)))