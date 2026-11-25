import re, math
from .note import Note
from .lane import Lane

class Chart:
    def __init__(self):
        self.title = ''
        self.bpm = 120
        self.offset = 0.0
        self.audio = ''
        self.notes: list[Note] = []
    
    def load_file(self, path):
        f = open(path, 'r')
        contents = f.read()
        # Get the title
        self.title = re.search(r"^Title:\s*(.+?)\s*$", contents, re.MULTILINE).group(1)

        # Get hit objects
        hit_objects = re.search(r"^\[HitObjects\][ \t]*\r?\n(.*?)(?=^\[|\Z)", contents, re.DOTALL | re.MULTILINE)
        lines = hit_objects.group(1).splitlines() if hit_objects else []

        owner = 'left'

        for line in lines:
            line = line.strip()
            if not line or line.startswith("//"):
                continue
                
            # Extract x, time, type, and end time (for long notes)
            mo = re.match(r"^(\d+),(\d+),(-?\d+),(\d+),(\d+)(?:,(\d+))?", line)

            if not mo:
                continue
            
            x, time, typ = int(mo.group(1)), int(mo.group(3)), int(mo.group(4))
            end_time = int(mo.group(6)) if typ & 128 and mo.group(6) else None

            lane = math.floor(x * 4 / 512)

            # Store the corresponding key depending on which lane
            if lane == 0: key = 'A'
            elif lane == 1: key = 'S'
            elif lane == 2: key = 'D'
            elif lane == 3: key = 'F'

            owner = 'right' if owner == 'left' else 'left'

            self.notes.append(
                Note(time, typ, lane, end_time, owner)
            )
    
    def load_audio(self, path):
        self.audio = path

    def play_sfx(self, sfx):
        pass


