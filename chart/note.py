from enum import Enum

class Note:
    def __init__(self, time, typ, lane, end_time, owner):
        self.time = time            # when will it appear (in ms)
        self.typ = typ              # note type (1 = normal, 128 = long note)
        self.lane = lane            # where the notes will fall
        self.end_time = end_time    # for long note
        self.owner = owner          # which side should hit it
        self.state = 'pending'      # pending | hit | missed

    def is_missed(self, song_time, late_window):
        return self.state == "pending" and song_time > self.time + late_window

    def update(self, song_time, late_window):
        if self.is_missed(song_time, late_window):
            self.state = "missed"