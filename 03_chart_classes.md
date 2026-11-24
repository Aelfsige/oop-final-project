# Chart Classes

Files: `chart/conductor.py`, `chart/note.py`, `chart/chart.py`, `chart/lane.py`

## Conductor
**Purpose:** The single source of timing truth.

**Attributes:** `bpm`, `offset`, `start_time`

**Methods:**
- `start()`: records start time and starts the music
- `song_time()`: seconds since start, minus offset
- `current_beat()`: `seconds_to_beats(song_time, bpm)`

**Instructions:** Prefer the mixer's playback position when available; fall back to `time.perf_counter()`.

## Note
**Purpose:** One hittable beat.

**Attributes:** `time` (seconds), `lane` (0-3), `owner` (side), `state` ("pending", "hit", "missed")

**Methods:**
- `update(song_time)`
- `is_missed(song_time)`: True once past the late hit window

**Instructions:** Notes hold data only; they do not decide judgement.

## Chart
**Purpose:** Stores and loads a song's notes.

**Attributes:** `notes`, `bpm`, `offset`, `title`

**Methods:**
- `load(path)`: reads JSON
- `notes_for(player)`: notes belonging to one side

**Example JSON:**
```json
{
  "title": "Demo",
  "bpm": 120,
  "offset": 0.0,
  "notes": [
    {"time": 1.0, "lane": 0, "owner": "left"},
    {"time": 1.5, "lane": 2, "owner": "right"}
  ]
}
```

**Instructions:** Start with one shared chart for both players, then try separate patterns.

## Lane
**Purpose:** One of a player's 4 key columns.

**Attributes:** `key`, `x`, `active_notes`, `hit_line_y`

**Methods:**
- `spawn_notes(song_time)`: activates notes entering the look-ahead window
- `update(song_time)`: auto-miss late notes, remove finished ones
- `try_hit(press_time)`: finds the nearest pending note and grades it
- `draw(screen)`

**Instructions:** Use `time_to_screen_y` so note position depends on song time, not frames.
