# Logic Classes

Files: `logic/judgement.py`, `logic/input_handler.py`, `logic/audio.py`, `logic/assets.py`

These classes are independent of the rest of the game, which avoids circular imports.

## JudgementSystem
**Purpose:** Grades a key press against a note.

**Attributes:** timing windows, e.g. `perfect = 0.050`, `good = 0.100` (seconds)

**Methods:** `judge(press_time, note_time)` returns "perfect", "good", or "miss"

**Instructions:** Use `abs(press_time - note_time)`. Keep windows configurable for difficulty.

## InputHandler
**Purpose:** Turns raw keys into game input.

**Attributes:** `key_map` {key: (player_side, lane_index)}

**Setup:** `InputHandler(key_map=None)` defaults to `A S D F` for left and `J K L ;` for right. Pass a mapping to customize it.

**Methods:** `map_key(key)` returns `(side, lane)` or `None`

**Instructions:**
- Timestamp the press with the conductor time as soon as the event arrives, not later in the frame.
- Ignore key repeat (use KEYDOWN only).

## AudioManager
**Purpose:** Music and sound effects.

**Attributes:** loaded music path, sfx dictionary, volume

**Setup:** `AudioManager(sfx_paths=None, volume=1.0)` preloads the provided `{name: path}` sound effects.

**Methods:** `play_music(path)`, `play_sfx(name)`, `stop()`

**Instructions:** Preload sfx (hit, miss, splat) at startup to avoid lag. Initialize the mixer with a small buffer for low latency.

## Assets
**Purpose:** Loads and caches images, sounds, and fonts.

**Attributes:** `images` and `sounds` keyed by path; `fonts` keyed by `(path, size)`

**Methods:** `load_image(path)`, `load_sound(path)`, `load_font(path, size)`

**Instructions:** Return the cached object if the path was already loaded. Call `convert_alpha()` on images once, at load time.
