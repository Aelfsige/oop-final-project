import math
import os
import re

import pygame

from .note import Note


class Chart:
    """A song's notes plus its music and sound effects."""

    SFX_NAMES = ("hit", "miss", "splat")

    def __init__(self):
        self.title = ''
        self.bpm = 120
        self.offset = 0.0           # audio sync offset in seconds (note times are already audio time)
        self.audio = ''             # music file path
        self.notes: list[Note] = []
        self.sfx = {}

    # ------------------------------------------------------------ loading
    def load_file(self, path):
        """Load a 4K osu!mania .osu file. Raises ValueError if it is not one."""
        with open(path, encoding='utf-8-sig') as f:
            contents = f.read()

        mode = re.search(r"^Mode:\s*(\d+)", contents, re.MULTILINE)
        keys = re.search(r"^CircleSize:\s*(\d+)", contents, re.MULTILINE)
        if not mode or int(mode.group(1)) != 3 or not keys or int(keys.group(1)) != 4:
            raise ValueError(f"{os.path.basename(path)} is not a 4K osu!mania map (Mode 3, CircleSize 4)")

        title = re.search(r"^Title:\s*(.+?)\s*$", contents, re.MULTILINE)
        self.title = title.group(1) if title else os.path.basename(path)

        # BPM from the first uninherited timing point (field 7 == 1)
        timing = re.search(r"^\[TimingPoints\][ \t]*\r?\n(.*?)(?=^\[|\Z)", contents, re.DOTALL | re.MULTILINE)
        for line in (timing.group(1).splitlines() if timing else []):
            parts = line.strip().split(",")
            if len(parts) >= 7 and parts[6].strip() == "1" and float(parts[1]) > 0:
                self.bpm = 60000 / float(parts[1])
                break

        # Music file named by the map, relative to the .osu file
        audio = re.search(r"^AudioFilename:\s*(.+?)\s*$", contents, re.MULTILINE)
        if audio:
            self.load_audio(os.path.join(os.path.dirname(path), audio.group(1)))

        # Hit objects
        hit_objects = re.search(r"^\[HitObjects\][ \t]*\r?\n(.*?)(?=^\[|\Z)", contents, re.DOTALL | re.MULTILINE)
        lines = hit_objects.group(1).splitlines() if hit_objects else []

        parsed = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith("//"):
                continue
            mo = re.match(r"^(\d+),(\d+),(-?\d+),(\d+),(\d+)(?:,(\d+))?", line)
            if not mo:
                continue
            x, time, typ = int(mo.group(1)), int(mo.group(3)), int(mo.group(4))
            end_time = int(mo.group(6)) if typ & 128 and mo.group(6) else None
            lane = min(3, math.floor(x * 4 / 512))
            parsed.append((time / 1000, typ, lane, end_time / 1000 if end_time else None))
        parsed.sort(key=lambda p: p[0])

        # Alternate the owner per timestamp, so a chord stays with one player
        self.notes = []
        owner = 'right'
        last_time = None
        for time, typ, lane, end_time in parsed:
            if last_time is None or abs(time - last_time) > 0.001:
                owner = 'right' if owner == 'left' else 'left'
                last_time = time
            self.notes.append(Note(time, typ, lane, end_time, owner))

    def load_audio(self, path):
        self.audio = path

    def load_sfx(self, folder):
        """Load hit.wav / miss.wav / splat.wav (or .ogg) from a folder. Missing files are skipped."""
        if not pygame.mixer.get_init():
            return
        for name in self.SFX_NAMES:
            for ext in (".wav", ".ogg"):
                path = os.path.join(folder, name + ext)
                if os.path.exists(path):
                    self.sfx[name] = pygame.mixer.Sound(path)
                    break

    # ------------------------------------------------------------ playback
    @property
    def has_music(self):
        return bool(self.audio) and pygame.mixer.get_init() is not None

    def play_music(self):
        if not self.has_music:
            return
        pygame.mixer.music.load(self.audio)
        pygame.mixer.music.play()

    def music_position(self):
        """Seconds the music has been playing, or None if it is not playing."""
        if not pygame.mixer.get_init() or not pygame.mixer.music.get_busy():
            return None
        pos = pygame.mixer.music.get_pos()
        return pos / 1000 if pos >= 0 else None

    def stop(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()

    def play_sfx(self, sfx):
        sound = self.sfx.get(sfx)
        if sound is not None:
            sound.play()

    def notes_for(self, side):
        return [n for n in self.notes if n.owner == side]