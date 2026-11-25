import time
from utils import seconds_to_beats


class Conductor:
    """Single source of timing truth. Uses mixer position when music plays,
    otherwise falls back to time.perf_counter()."""

    def __init__(self, bpm=120, offset=0.0, audio=None, lead_in=2.0):
        self.bpm = bpm
        self.offset = offset
        self.audio = audio
        self.lead_in = lead_in      # seconds of negative song_time before the start
        self.start_time = None
        self._music_started = False

    def start(self):
        self.start_time = time.perf_counter() + self.lead_in
        self._music_started = False

    def _raw_time(self):
        if self.start_time is None:
            return -self.lead_in
        return time.perf_counter() - self.start_time

    def update(self):
        """Call once per frame: starts the music when the lead-in ends."""
        if (self.start_time is not None and not self._music_started
                and self._raw_time() >= 0 and self.audio and self.audio.has_music):
            self.audio.play_music()
            self._music_started = True

    def song_time(self):
        if self._music_started and self.audio:
            pos = self.audio.music_position()
            if pos is not None:
                return pos - self.offset
        return self._raw_time() - self.offset

    def current_beat(self):
        return seconds_to_beats(self.song_time(), self.bpm)
