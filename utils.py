"""Standalone helpers shared by every group. Depends on nothing in the game."""
import json


def beats_to_seconds(beats, bpm):
    return beats * 60.0 / bpm


def seconds_to_beats(seconds, bpm):
    return seconds * bpm / 60.0


def time_to_screen_y(note_time, song_time, hit_line_y, spawn_y, lookahead):
    """Notes fall from spawn_y to hit_line_y; position depends on time only."""
    progress = (note_time - song_time) / lookahead  # 1.0 = just spawned, 0 = on line
    return hit_line_y - progress * (hit_line_y - spawn_y)


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def clamp(value, lo, hi):
    return max(lo, min(hi, value))
