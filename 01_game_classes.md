# Game Classes

Files: `game/game.py`, `game/scenes.py`

## Game
Owns the pygame window, frame clock, current scene, and main loop.

**Attributes:** `screen`, `clock`, `current_scene`, `running`, `match_factory`

**Methods:**
- `run()`: compute `dt` once per frame, route events to the scene, then update and draw.
- `change_scene(scene)`: set the current `Scene` instance.
- `new_match()`: call the optional `match_factory(game)` and return the match dependencies. Starting a match requires a factory.

The factory returns `players` keyed by side, `hand`, `chart`, `conductor`, `judgement`, `input_handler`, `audio`, and `assets`. It wires chart notes into each player's lanes and shares one `JudgementSystem` across them. `PlayScene` creates its `HUD` from `players` and `hand`.

Keep gameplay rules in `PlayScene` and pass `dt` to `update()` in seconds.

## Scene
Base class for screens. Each scene keeps a reference to `game` and implements:

- `handle_event(event)`
- `update(dt)`
- `draw(screen)`

## MenuScene
Shows the title and start option. On start, switch with `game.change_scene(PlayScene(game))`.

## PlayScene
Coordinates one match; it owns the game rules and connects the other classes.

**Attributes:** `players` (`{"left": Player, "right": Player}`), `hand`, `chart`, `conductor`, `judgement`, `input_handler`, `audio`, `assets`, `hud`

**Input flow:** On `KEYDOWN`, map the key to `(side, lane_index)`. Ignore key repeats and timestamp it immediately with `conductor.song_time()`. Call `players[side].press(lane_index, time)`; the lane selects a note and `JudgementSystem` returns `"perfect"`, `"good"`, or `"miss"`.

**Result flow:**
- Hit: call `players[side].add_combo()`, show the judgement, call `players[side].face.set_state("hit")`, then pass the hand to that side and push it toward the opponent.
- Miss: call `players[side].reset_combo()` and push the hand toward that player's face.
- Auto-miss: apply the same miss response when a lane expires a late note.
- If `hand.reached(side)`, call `players[side].face.set_state("cream_pied")` and switch to `GameOverScene` with the other player as winner.

**Update:** Read song time from the conductor, update each lane to spawn notes and detect auto-misses, apply the miss response to new misses, then update the hand with `dt`.

Use `AudioManager` for playback and sound effects, and `Assets` for cached images, sounds, and fonts. Keep hit, miss, and winner decisions here; `Player`, `Hand`, `Face`, `Lane`, and `HUD` handle their own state or display.

## GameOverScene
Shows `winner` and offers restart or menu. Restart with a fresh `PlayScene(game)`; return to `MenuScene(game)` for the menu.

## HUD
Displays player combos, judgement popups, and the hand position. `PlayScene` owns it and gives it read-only access to match state.

**Methods:** `show_judgement(text, side)`, `draw(screen)`

HUD draws state only; it never changes the match.
