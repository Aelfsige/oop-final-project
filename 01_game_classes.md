# Game Classes

Files: `game/game.py`, `game/scenes.py`

## Game
**Purpose:** Owns the window, clock, and main loop. Switches between scenes.

**Attributes:** `screen`, `clock`, `current_scene`, `running`

**Methods:**
- `run()`: main loop: poll events, `update(dt)`, `draw(screen)`, flip display
- `change_scene(scene)`: swaps `current_scene`

**Instructions:**
- Compute `dt` once per frame and pass it to the scene.
- Never put gameplay logic here.

## Scene (base class)
**Purpose:** Common interface for every screen.

**Methods (override in subclasses):** `handle_event(event)`, `update(dt)`, `draw(screen)`

**Instructions:** Each scene receives a reference to `Game` so it can call `change_scene`.

## MenuScene
**Purpose:** Title screen with a start option.

**Attributes:** menu options, selected index

**Instructions:** On start, create a new `PlayScene` and call `game.change_scene(...)`.

## PlayScene
**Purpose:** Runs the match. This is where the other groups are wired together.

**Attributes:** `players` (2), `hand`, `faces` (2), `conductor`, `chart`, `judgement`, `input_handler`, `hud`

**Per-frame flow:**
1. `handle_event`: `InputHandler` converts a key press into `(player, lane)` plus a timestamp.
2. The player's `Lane` calls `try_hit`, using `JudgementSystem` to grade it.
3. Hit: `Player.add_combo()`, `Hand.pass_to(opponent)` and push toward the opponent.
4. Miss: `Player.reset_combo()`, and the hand moves toward the player's own face.
5. `update`: update conductor, lanes, notes (auto-miss late notes), and hand.
6. If `Hand.reached(side)`, set that `Face` to cream-pied and go to `GameOverScene`.

**Instructions:**
- Drive everything from `Conductor.song_time()`, never from frame count.
- Keep rule decisions (who gets hit) here, not in `Hand`.

## GameOverScene
**Purpose:** Shows the winner and offers restart or menu.

**Attributes:** `winner`

**Instructions:** Restart creates a fresh `PlayScene`; do not reuse the old one.

## HUD
**Purpose:** Draws combo, judgement popups, and the tug-of-war indicator. Owned by `PlayScene`.

**Methods:** `show_judgement(text, side)`, `draw(screen)`

**Instructions:** Read-only: it displays state and never changes it.
