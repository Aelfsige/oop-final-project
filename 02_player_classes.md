# Player Classes

Files: `player/player.py`, `player/hand.py`, `player/face.py`

## Player
**Purpose:** One competitor.

**Attributes:** `side` ("left" or "right"), `keys` (4 key bindings), `lanes` (4 `Lane` objects), `combo`, `score`, `face`

**Methods:**
- `press(lane_index, time)`: forwards to the lane, returns the judgement
- `add_combo()`
- `reset_combo()`

**Instructions:**
- Left and right players use different key sets (e.g. left: `A S D F`, right: `J K L ;`).
- A player knows nothing about the other player. `PlayScene` coordinates both.

## Hand
**Purpose:** The middle cream-pie hand.

**Attributes:** `position` (-1.0 = left face, +1.0 = right face, 0 = center), `controlling_side`, `animation_state`

**Methods:**
- `pass_to(side)`: gives control to that side
- `push(direction, amount)`: moves `position` toward a face
- `update(dt)`: smooth movement and animation
- `reached(side)`: True if the hand touches that face

**Instructions:**
- Clamp `position` to [-1, 1] (use `utils.clamp`).
- Decide early: tug-of-war (continuous position) or hard flip of control on each tap. Start with tug-of-war plus `controlling_side`.

## Face
**Purpose:** The character that can get hit.

**Attributes:** `side`, `state` ("idle", "hit", "cream_pied")

**Methods:** `set_state(state)`, `draw(screen)`

**Instructions:**
- "hit" is a short reaction, "cream_pied" is final and triggers game over.
- Keep the splat animation inside `Face`, not `Hand`.
