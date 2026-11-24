# Rhythm Cream-Pie Game: Class Documentation

Two-player rhythm game in Python (pygame). Each player has 4 keys. A hand sits in the middle; every successful tap passes control to the opposite side. The first player to get cream-pied loses.

| File | Group | Classes |
|---|---|---|
| `01_game_classes.md` | Game | Game, Scene, MenuScene, PlayScene, GameOverScene, HUD |
| `02_player_classes.md` | Player | Player, Hand, Face |
| `03_chart_classes.md` | Chart | Conductor, Note, Chart, Lane |
| `04_logic_classes.md` | Logic | JudgementSystem, InputHandler, AudioManager, Assets |

## Dependency direction
- Game classes depend on everything else.
- Player classes depend on Chart classes (through `Lane`).
- Chart classes depend only on `Conductor` and `utils`.
- Logic classes depend on nothing in the game (no circular imports).

## Standalone helpers (`utils.py`)
`beats_to_seconds`, `seconds_to_beats`, `time_to_screen_y`, `load_json`, `clamp`
