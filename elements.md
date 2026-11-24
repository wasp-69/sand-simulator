<!--markdownlint-disable-->
# Elements Documentation

> **Notes on Mechanics (from source):**
> - **Directions (`up`, `down`, `left`, `right`)** are relative to the active **gravity orientation**.
> - **Orthogonal neighbors** = 4 cardinal neighbors (`up`, `down`, `left`, `right`).
> - **Adjacent neighbors** = all 8 surrounding cells (orthogonal + diagonals).
> - **Transparency** = how much dynamic light intensity (starting at `100`) is subtracted per cell along a light ray (`0` = no loss, `-1` = increases light, `100` = completely opaque).
> - **Weight** = used solely by **Obsidian** to calculate overhead crushing load.

---

## 0. Air

### Main Quirk
Empty space. Air has no update handler of its own and acts as the default medium for powders, liquids, gases, and fire to move through or spawn into. Dynamic lighting skips value-dimming on Air, though it can still receive Crystal hue tinting (`add_hue`) and flash white when contaminated by Uranium radiation.

### Reactions
- **Movement Medium:** Powders fall into Air; liquids fall and spread into Air; gases rise and spread into Air; Fire rises into Air.
- **Fire + Dry Wood / Oil:** Nearby Air cells have a 75% chance each to ignite into **Fire** when Dry Wood or Oil catches fire.
- **Lava:** Has a 5% chance every 3rd frame to spawn **Fire** in the Air cell directly above it.
- **Pump:** Outputs into the cell below it only when that cell is **Air**.

### Profile
| Property | Value |
| :--- | :--- |
| **ID** | `0` (`AIR`) |
| **Symbol** | `∙` |
| **Type** | `air` |
| **Color (HSV)** | `(0, 0, 6)` |
| **Transparency** | `0.5` |
| **Weight** | `0` |

---

## 1. Sand

### Main Quirk
Classic falling powder. Falls straight down into **Air**, or diagonally down-left / down-right (randomized check order) into **Air**. Sinks through **Water** and **Oil** by swapping downward or diagonally downward. Supports a secret rainbow gradient mode (`RAINBOW_SAND`) toggled by typing `itchio` (unlocks `"Eye Candy"`).

### Reactions
- **Water / Oil:** Swaps downward or diagonally downward (sinks).
- **Steam / Fumes:** Can be displaced downward by rising Steam or Fumes.
- **Acid (orthogonal):** Destroys both Acid and Sand into **Air**.
- **Lava (orthogonal):** Converts Sand into **Glass**.
- **Uranium (radiation ray):** On a triggered hit (`0.2 / (1 + dist / 10)`), has an extra 30% chance to turn into **Air** and increase the emitter Uranium's decay stage by `1`.
- **Graphite:** If directly above Graphite, can be pushed sideways away from a blocked side.

### Profile
| Property | Value |
| :--- | :--- |
| **ID** | `1` (`SAND`) |
| **Symbol** | `▩` |
| **Type** | `powder` |
| **Color (HSV)** | Dynamic: `(38, 36, 80)` normally; rainbow hue `(avg * 360) + HUE` when `RAINBOW_SAND` is active |
| **Transparency** | `7` |
| **Weight** | `2` |

---

## 2. Water

### Main Quirk
Standard liquid. Falls straight down into **Air** or **Oil**, or spreads left/right (randomized order) into **Air** or **Oil**.

### Reactions
- **Sand / Gunpowder / Uranium:** Powders sink downward/diagonally through Water.
- **Oil:** Water sinks through and horizontally displaces Oil.
- **Steam / Fumes:** Rising Steam and Fumes can swap through Water.
- **Acid (orthogonal):** Acid turns into **Air** and Water boils into **Steam** (unlocks `"Chemistry!"`).
- **Dry Wood (orthogonal):** Absorbed by Dry Wood, turning Dry Wood into **Wet Wood** and Water into **Air**.
- **Fire (adjacent):** Extinguishes Fire into **Air**.
- **Lava (orthogonal):** Water turns into **Air** and Lava cools into **Obsidian** (unlocks `"Flint... and Steel..."`).
- **Gunpowder / Fuse (adjacent):** Turns Gunpowder or Fuse into **Wet Wood** and consumes Water into **Air**.
- **Crystal (orthogonal):** Crystallizes into **Crystal** (`crystal_glow = 250`) when the Crystal's `light_level == 0`, or with probability `1 / (light_level ** 2)`.
- **Ice (orthogonal):** 1% chance per update to freeze into **Ice**.
- **Uranium (radiation ray):** On a triggered hit, turns into **Acid** and increases emitter decay stage by `1`.

### Profile
| Property | Value |
| :--- | :--- |
| **ID** | `2` (`WATER`) |
| **Symbol** | `■` |
| **Type** | `liquid` |
| **Color (HSV)** | `(215, 78, 100)` |
| **Transparency** | `4` |
| **Weight** | `1` |

---

## 3. Steel

### Main Quirk
Passive, immovable solid. Has no update logic of its own and resists Fire, gravity, and crushing.

### Reactions
- **Acid (orthogonal):** 1% chance per update to dissolve into **Air** (Acid is not consumed).
- **Lava (orthogonal):** 15% chance every 3rd frame to melt into **Air**.
- **Uranium (radiation ray):** On a triggered hit, degrades into **Sand** and increases emitter decay stage by `1`.

### Profile
| Property | Value |
| :--- | :--- |
| **ID** | `3` (`STEEL`) |
| **Symbol** | `◙` |
| **Type** | `solid` |
| **Color (HSV)** | `(0, 0, 55)` |
| **Transparency** | `7` |
| **Weight** | `0` |

---

## 4. Acid

### Main Quirk
Corrosive liquid. Before moving, checks its 4 orthogonal neighbors for reactions; afterward, falls straight down or spreads left/right into **Air** only.

### Reactions
- **Sand (orthogonal):** Both Acid and Sand turn into **Air**.
- **Water (orthogonal):** Acid turns into **Air** and Water turns into **Steam** (unlocks `"Chemistry!"`).
- **Steel (orthogonal):** 1% chance per update to destroy Steel into **Air**.
- **Dry Wood (orthogonal):** Acid turns into **Air** and Dry Wood ignites into **Fire**.
- **Wet Wood (orthogonal):** Acid turns into **Air** and Wet Wood turns into **Steam**.
- **Fire (orthogonal):** Extinguishes Fire into **Air**.
- **Gunpowder / Fuse (orthogonal):** 50% chance per update to ignite them into **Fire**.
- **Uranium (orthogonal):** If Uranium's `uraniumdecaystage > 7`, resets Uranium's decay stage to `0` and neutralizes Acid into **Water**.
- **Crystal (orthogonal):** Increases Crystal's `crystal_glow` by `+2`.
- **Oil (orthogonal):** Both Oil and Acid turn into **Air**.
- **Lava (orthogonal):** Lava turns all 4 of its orthogonal neighbors into **Fire** and itself into **Air**.
- **Steam / Fumes:** Can be swapped upward through by rising Steam or Fumes.

### Profile
| Property | Value |
| :--- | :--- |
| **ID** | `4` (`ACID`) |
| **Symbol** | `■` |
| **Type** | `liquid` |
| **Color (HSV)** | `(128, 100, 100)` |
| **Transparency** | `4` |
| **Weight** | `1` |

---

## 5. Steam

### Main Quirk
Condensing gas. Rises straight up or diagonally up through **Air**, **Sand**, **Water**, **Acid**, **Fire**, **Gunpowder**, **Uranium**, **Oil**, and **Fumes**, or spreads left/right into **Air**. If the cell directly above it is out of bounds or has type `"solid"`, `"glass"`, or `"pump"`, Steam has a 1% chance per update to condense into **Water**.

### Reactions
- **Dry Wood:** Dry Wood falling straight down swaps places with Steam.
- **Lava (orthogonal):** Destroyed into **Air**.
- **Ice (orthogonal):** Immediately condenses into **Water**.

### Profile
| Property | Value |
| :--- | :--- |
| **ID** | `5` (`STEAM`) |
| **Symbol** | `◌` |
| **Type** | `gas` |
| **Color (HSV)** | `(80, 2, 40)` |
| **Transparency** | `4` |
| **Weight** | `0` |

---

## 6. Dry Wood

### Main Quirk
Vertically falling, absorbent flammable block. Unlike Sand, it does **not** slide diagonally—it only falls straight down by swapping with **Air**, **Steam**, or **Fire**. Checks orthogonal neighbors for **Water** only when it is not falling straight down.

### Reactions
- **Water (orthogonal, when resting):** Absorbs Water, turning Dry Wood into **Wet Wood** and Water into **Air**.
- **Acid (orthogonal):** Ignites into **Fire** while Acid turns into **Air**.
- **Fire (adjacent):** 10% chance per update to ignite nearby **Air** cells into **Fire** (75% each, unlocks `"Spontaneous Combustion!"`), with a nested 1% chance (0.1% overall) to burn away into **Air**.
- **Lava (orthogonal):** 7.5% chance every 3rd frame to ignite into **Fire**.
- **Uranium (radiation ray):** On a triggered hit, ignites into **Fire** and increases emitter decay stage by `1`.
- **Graphite:** Treated as `powder` (`symbol: "▩"`), so it can be slid sideways when resting directly on Graphite.

### Profile
| Property | Value |
| :--- | :--- |
| **ID** | `6` (`DRYWOOD`) |
| **Symbol** | `▩` |
| **Type** | `powder` |
| **Color (HSV)** | `(28, 51, 46)` |
| **Transparency** | `7` |
| **Weight** | `3` |

---

## 7. Wet Wood

### Main Quirk
Uranium-resistant, immovable solid created when **Dry Wood**, **Gunpowder**, or **Fuse** absorbs **Water**. Has no update handler of its own.

### Reactions
- **Acid (orthogonal):** Turns into **Steam** while Acid becomes **Air**.
- **Fire (adjacent):** 1% chance per update to dry back into **Dry Wood** while extinguishing the Fire cell into **Steam**.
- **Lava (orthogonal):** 5% chance every 3rd frame to ignite into **Fire** (with a 50% chance the Lava cell becomes **Air**).

### Profile
| Property | Value |
| :--- | :--- |
| **ID** | `7` (`WETWOOD`) |
| **Symbol** | `◙` |
| **Type** | `solid` |
| **Color (HSV)** | `(25, 80, 25)` |
| **Transparency** | `7` |
| **Weight** | `0` |

---

## 8. Fire

### Main Quirk
Self-illuminating flame (`illuminate`, exempt from dynamic light darkening). Checks all 8 adjacent cells: if surrounded exclusively by non-flammable elements (`Air`, `Water`, `Steel`, `Sand`, `Acid`, `Steam`, `Fire`, `Lava`, `Obsidian`, `Uranium`, `Crystal`, `Glass`, `Graphite`, `Morph`, `Pump`), it has a 20% chance per update to burn out into **Air**, otherwise rises straight up into **Air**.

### Reactions
- **Water (adjacent):** Extinguishes Fire into **Air**.
- **Gunpowder / Fuse (adjacent):** Immediately ignites them into **Fire**.
- **Ice (adjacent):** Immediately melts Ice into **Water**.
- **Dry Wood (adjacent):** 10% chance to turn adjacent **Air** cells into **Fire** (75% each, unlocks `"Spontaneous Combustion!"`), plus 1% nested chance to destroy Dry Wood into **Air**.
- **Oil (adjacent):** 10% chance to turn adjacent **Air** cells into **Fire** (75% each, unlocks `"Spontaneous Combustion!"`), plus 10% nested chance to destroy Oil into **Air**.
- **Wet Wood (adjacent):** 1% chance to turn Wet Wood into **Dry Wood** and Fire into **Steam**.
- **Fumes (adjacent):** Immediately ignites Fumes into **Fire**.
- **Acid (orthogonal):** Acid extinguishes Fire into **Air**.
- **Dry Wood / Oil / Lava:** Can fall downward through Fire (swapping places); **Steam** and **Fumes** can rise through Fire.

### Profile
| Property | Value |
| :--- | :--- |
| **ID** | `8` (`FIRE`) |
| **Symbol** | `●` |
| **Type** | `fire` |
| **Color (HSV)** | `(35, 100, 100)` |
| **Transparency** | `0` |
| **Weight** | `0` |

---

## 9. Lava

### Main Quirk
Slow, self-illuminating, superheated liquid (`illuminate`, exempt from dynamic light darkening). Updates only every 3rd frame (`FRAMENUM % 3 == 0`). On each active update, has a 5% chance to turn the **Air** cell directly above it into **Fire**, swaps downward with **Fire** if directly below, and otherwise flows like **Water** (into **Air** or **Oil**).

### Reactions
- **Sand (orthogonal):** Melts Sand into **Glass**.
- **Water (orthogonal):** Water turns into **Air** and Lava solidifies into **Obsidian** (unlocks `"Flint... and Steel..."`).
- **Steel (orthogonal):** 15% chance per active update to destroy Steel into **Air**.
- **Acid (orthogonal):** Turns all 4 of Lava's orthogonal neighbors into **Fire** and Lava itself into **Air**.
- **Steam (orthogonal):** Destroys Steam into **Air**.
- **Dry Wood / Gunpowder / Fuse (orthogonal):** 7.5% chance per active update to ignite into **Fire** (note: Gunpowder and Fuse also self-ignite immediately on adjacent contact in their own handlers).
- **Uranium (orthogonal):** 10% chance per active update to add `+3` to Uranium's `uraniumdecaystage`.
- **Wet Wood (orthogonal):** 5% chance per active update to turn Wet Wood into **Fire** (50% chance Lava turns into **Air**).
- **Ice (orthogonal):** Melts Ice into **Water**.
- **Graphite (orthogonal):** 0.1% chance (`0.001`) per active update to convert Graphite into **Gunpowder**.
- **Oil / Fumes (orthogonal):** Immediately ignites them into **Fire**.

### Profile
| Property | Value |
| :--- | :--- |
| **ID** | `9` (`LAVA`) |
| **Symbol** | `■` |
| **Type** | `liquid` |
| **Color (HSV)** | `(17, 100, 100)` |
| **Transparency** | `0` |
| **Weight** | `3` |

---

## 10. Obsidian

### Main Quirk
Radiation-shielding solid that can collapse under excessive vertical weight. Blocks **Uranium** radiation rays completely. Every update, sums the `weight` of up to `15` contiguous non-zero-weight cells directly above it (stopping at the first cell with `weight == 0` or the grid edge). If the summed weight exceeds `20`, Obsidian breaks into **Air**.

### Reactions
- **Uranium (radiation ray):** Terminates the radiation ray on impact without taking damage.
- **Overhead Weight > 20 (within 15 cells up):** Crushes into **Air**.

### Profile
| Property | Value |
| :--- | :--- |
| **ID** | `10` (`OBSIDIAN`) |
| **Symbol** | `◙` |
| **Type** | `solid` |
| **Color (HSV)** | `(250, 70, 70)` |
| **Transparency** | `7` |
| **Weight** | `0` |

---

## 11. Gunpowder

### Main Quirk
Highly flammable falling powder. Checks its 8 adjacent neighbors for **Water** or **Lava** before falling/sliding like **Sand**.

### Reactions
- **Water (adjacent):** Turns into **Wet Wood** and consumes Water into **Air**.
- **Lava (adjacent):** Immediately ignites into **Fire**.
- **Fire (adjacent):** Immediately ignites into **Fire**.
- **Acid (orthogonal):** 50% chance per update to ignite into **Fire**.
- **Uranium (radiation ray):** On a triggered hit, ignites into **Fire** and increases emitter decay stage by `1`.
- **Steam / Fumes:** Can be swapped through by rising Steam or Fumes.
- **Graphite:** As a `powder`, can be pushed sideways if sitting directly above Graphite.

### Profile
| Property | Value |
| :--- | :--- |
| **ID** | `11` (`GUNPOWDER`) |
| **Symbol** | `▩` |
| **Type** | `powder` |
| **Color (HSV)** | `(5, 0, 5)` |
| **Transparency** | `7` |
| **Weight** | `2` |

---

## 12. Fuse

### Main Quirk
Stationary flammable solid. Stays fixed in place regardless of gravity and checks its 8 adjacent neighbors for **Water** or **Lava**.

### Reactions
- **Water (adjacent):** Turns into **Wet Wood** and consumes Water into **Air**.
- **Lava (adjacent):** Immediately ignites into **Fire**.
- **Fire (adjacent):** Immediately ignites into **Fire**.
- **Acid (orthogonal):** 50% chance per update to ignite into **Fire**.
- **Uranium (radiation ray):** On a triggered hit, ignites into **Fire** and increases emitter decay stage by `1`.

### Profile
| Property | Value |
| :--- | :--- |
| **ID** | `12` (`FUSE`) |
| **Symbol** | `◙` |
| **Type** | `solid` |
| **Color (HSV)** | `(55, 80, 20)` |
| **Transparency** | `7` |
| **Weight** | `0` |

---

## 13. Uranium

### Main Quirk
Radioactive falling powder (`handle_sand`). Tracks an internal `uraniumdecaystage` (brightens as it increases: `value = 20 + uraniumdecaystage * 5`, and resets to `0` if the cell stops being Uranium). Each update has a `0.01 + (uraniumdecaystage / 200)` chance to emit a radiation ray toward a random grid border coordinate. If `uraniumdecaystage > 11`, Uranium dies from over-decay into **Air**.

### Reactions
- **Radiation Ray Pathing:**
  - **Obsidian:** Stops the ray.
  - **Graphite:** Reflects the ray (up to recursion depth `100`).
  - **Glass:** Redirects the ray toward the player's pointer `(pointer_x, pointer_y)` (up to recursion depth `100`).
  - **Crystal:** Adds `+50` to Crystal's `crystal_glow`.
- **Radiation Ray Mutations** (trigger chance `0.2 / (1 + dist / 10)`; each triggered reaction adds `+1` to the emitting Uranium's `uraniumdecaystage`):
  - **Water** → **Acid**
  - **Steel** → **Sand**
  - **Dry Wood** → **Fire**
  - **Sand** → **Air** (30% additional chance)
  - **Gunpowder / Fuse** → **Fire**
  - **Ice** → **Water**
  - **Oil** → **Fumes**
  - **Fumes** → **Fire**
  - **Morph** → random element from `PROFILE`
  - **Pump** → sets the cell directly above the Pump (`up(hit_cell)`) to a random element from `PROFILE`
- **Acid (orthogonal):** If `uraniumdecaystage > 7`, resets `uraniumdecaystage` to `0` and turns Acid into **Water**.
- **Lava (orthogonal):** 10% chance every 3rd frame to add `+3` to `uraniumdecaystage`.
- **Ice (orthogonal):** Decreases `uraniumdecaystage` by `1` (minimum `0`) and may melt Ice into **Water**.
- **Steam / Fumes / Graphite:** Can be swapped through by rising Steam/Fumes, and pushed sideways by Graphite below it.

### Profile
| Property | Value |
| :--- | :--- |
| **ID** | `13` (`URANIUM`) |
| **Symbol** | `▩` |
| **Type** | `powder` |
| **Color (HSV)** | Dynamic: `(75, 100, 20 + uraniumdecaystage * 5)` |
| **Transparency** | `7` |
| **Weight** | `7` |

---

## 14. Crystal

### Main Quirk
Luminescent, light-amplifying, and slow-growing solid (`illuminate`). Has negative transparency (`-1`), meaning dynamic light rays **gain** `+1` light level per Crystal cell traversed, and tints downstream cells with an oscillating hue (`240 + 60 * sin(FRAMENUM * 0.05 * crystal_glow)`). Its own color oscillates between hues `200` and `250`. Its `crystal_glow` decays back toward `1` each update (`-1`, plus `-2` if `> 50`, plus `-3` if `> 100`); if `crystal_glow > 5000`, Crystal turns into **Glass**.

### Reactions
- **Water (orthogonal):** In darkness (`light_level == 0`) or with probability `1 / (light_level ** 2)`, grows into adjacent Water, converting it into **Crystal** (`crystal_glow = 250`).
- **Acid (orthogonal):** Increases `crystal_glow` by `+2`.
- **Uranium (radiation ray):** Increases `crystal_glow` by `+50` (and converts Crystal into **Glass** if `crystal_glow > 5000`).

### Profile
| Property | Value |
| :--- | :--- |
| **ID** | `14` (`CRYSTAL`) |
| **Symbol** | `◙` |
| **Type** | `solid` |
| **Color (HSV)** | Dynamic: `(200–250, 75, 75)` oscillating with `FRAMENUM` and `crystal_glow` |
| **Transparency** | `-1` |
| **Weight** | `0` |

---

## 15. Glass

### Main Quirk
Fully transparent (`transparency: 0`) solid that focuses **Uranium** radiation toward the player's pointer. Updating a Glass cell unlocks the `"Transparent"` achievement.

### Reactions
- **Uranium (radiation ray):** Redirects the incoming radiation ray toward the player's current pointer coordinates `(pointer_x, pointer_y)` and extends it onward (up to recursion depth `100`).
- *(Formed when **Sand** touches **Lava**, or when **Crystal** exceeds `crystal_glow > 5000`.)*

### Profile
| Property | Value |
| :--- | :--- |
| **ID** | `15` (`GLASS`) |
| **Symbol** | `▢` |
| **Type** | `glass` |
| **Color (HSV)** | `(0, 0, 80)` |
| **Transparency** | `0` |
| **Weight** | `0` |

---

## 16. Graphite

### Main Quirk
Completely opaque solid (`transparency: 100`), radiation mirror, and powder diverter. If a `"powder"` cell sits directly above Graphite, and one side of that powder cell (`left(above)` or `right(above)`) is occupied (not **Air**) while the opposite side is not `"solid"`, `"fire"`, `"glass"`, `"pump"`, or `"cloner"`, Graphite swaps the overhead powder cell into that opposite side.

### Reactions
- **Uranium (radiation ray):** Reflects incoming radiation rays based on step direction and neighboring Graphite cells (up to recursion depth `100`).
- **Lava (orthogonal):** 0.1% chance (`0.001`) every 3rd frame to convert Graphite into **Gunpowder**.
- **Powders above it:** Slides **Sand**, **Dry Wood**, **Gunpowder**, or **Uranium** sideways away from blocked neighbors.

### Profile
| Property | Value |
| :--- | :--- |
| **ID** | `16` (`GRAPHITE`) |
| **Symbol** | `◙` |
| **Type** | `solid` |
| **Color (HSV)** | `(200, 65, 45)` |
| **Transparency** | `100` |
| **Weight** | `0` |

---

## 17. Ice

### Main Quirk
Freezing solid. Checks its 4 orthogonal neighbors in a randomized order each update to cool nearby **Water**, **Steam**, and **Uranium**.

### Reactions
- **Water (orthogonal):** 1% chance per update to freeze Water into **Ice**.
- **Steam (orthogonal):** Immediately condenses Steam into **Water**.
- **Uranium (orthogonal):** Decreases Uranium's `uraniumdecaystage` by `1` (min `0`); if `uraniumdecaystage < 20`, Ice melts into **Water** with probability `1 / (20 - uraniumdecaystage)`.
- **Fire (adjacent):** Immediately melts Ice into **Water**.
- **Lava (orthogonal):** Immediately melts Ice into **Water** every 3rd frame.
- **Uranium (radiation ray):** On a triggered hit, melts Ice into **Water** and increases emitter decay stage by `1`.

### Profile
| Property | Value |
| :--- | :--- |
| **ID** | `17` (`ICE`) |
| **Symbol** | `◙` |
| **Type** | `solid` |
| **Color (HSV)** | `(200, 80, 100)` |
| **Transparency** | `4` |
| **Weight** | `0` |

---

## 18. Oil

### Main Quirk
Light, flammable liquid. Falls straight down into **Air** or **Fire**, or spreads left/right into **Air**. Less dense than **Water** and **Sand**, which both sink through it.

### Reactions
- **Sand / Water:** Displaced upward as Sand or Water swaps downward through Oil.
- **Steam / Fumes:** Can be swapped through by rising Steam or Fumes.
- **Fire (adjacent):** 10% chance per update to ignite nearby **Air** cells into **Fire** (75% each, unlocks `"Spontaneous Combustion!"`), with a nested 10% chance (1% overall) to burn Oil away into **Air**.
- **Lava (orthogonal):** Immediately ignites Oil into **Fire** every 3rd frame.
- **Acid (orthogonal):** Destroys both Oil and Acid into **Air**.
- **Uranium (radiation ray):** On a triggered hit, vaporizes Oil into **Fumes** and increases emitter decay stage by `1`.

### Profile
| Property | Value |
| :--- | :--- |
| **ID** | `18` (`OIL`) |
| **Symbol** | `■` |
| **Type** | `liquid` |
| **Color (HSV)** | `(230, 80, 20)` |
| **Transparency** | `6` |
| **Weight** | `2` |

---

## 19. Fumes

### Main Quirk
Non-condensing, flammable gas. Rises straight up or diagonally up through **Air**, **Sand**, **Water**, **Acid**, **Fire**, **Gunpowder**, **Uranium**, and **Oil**, or spreads left/right into **Air**. Never condenses back into liquid.

### Reactions
- **Fire (adjacent):** Immediately ignites into **Fire**.
- **Lava (orthogonal):** Immediately ignites into **Fire** every 3rd frame.
- **Uranium (radiation ray):** On a triggered hit, ignites into **Fire** and increases emitter decay stage by `1`.
- **Steam:** Steam can swap upward through Fumes.

### Profile
| Property | Value |
| :--- | :--- |
| **ID** | `19` (`FUMES`) |
| **Symbol** | `◌` |
| **Type** | `gas` |
| **Color (HSV)** | `(60, 100, 50)` |
| **Transparency** | `4` |
| **Weight** | `0` |

---

## 20. Morph

### Main Quirk
Immovable shapeshifter. Checks its 4 orthogonal neighbors each update and transforms itself into the first neighboring element that is not **Air** or **Morph** (provided that neighbor's `update` flag is `True`), unlocking `"Copy Cat!"`.

### Reactions
- **Any non-Air, non-Morph element (orthogonal):** Morph converts itself into a copy of that element.
- **Uranium (radiation ray):** On a triggered hit, mutates into a random element from `PROFILE` and increases emitter decay stage by `1`.

### Profile
| Property | Value |
| :--- | :--- |
| **ID** | `20` (`MORPH`) |
| **Symbol** | `⧆` |
| **Type** | `cloner` |
| **Color (HSV)** | `(300, 100, 100)` |
| **Transparency** | `0` |
| **Weight** | `0` |

---

## 21. Pump

### Main Quirk
Gravity-aligned element duplicator. Checks the cell directly "above" it (`up(cell)`) and directly "below" it (`down(cell)`). If the cell above is neither **Air** nor **Pump**, and the cell below is **Air**, Pump copies the above cell's state into the cell below without consuming the source cell.

### Reactions
- **Any non-Air, non-Pump element above + Air below:** Continuously duplicates that element into the Air cell below.
- **Uranium (radiation ray):** On a triggered hit, sets the cell directly above the Pump (`up(hit_cell)`) to a random element from `PROFILE` and increases emitter decay stage by `1`.

### Profile
| Property | Value |
| :--- | :--- |
| **ID** | `21` (`PUMP`) |
| **Symbol** | `▣` |
| **Type** | `pump` |
| **Color (HSV)** | `(350, 80, 70)` |
| **Transparency** | `6` |
| **Weight** | `0` |

---

## 22. Void

### Main Quirk
Immovable matter-eraser. Checks its 4 orthogonal neighbors each update and deletes every neighbor that is neither **Air** nor **Void** (provided `current.update` is `True`), turning it into **Air** and unlocking `"His Gluttony Sickens Me."`.

### Reactions
- **Any non-Air, non-Void element (orthogonal):** Immediately erases the neighbor into **Air**.

### Profile
| Property | Value |
| :--- | :--- |
| **ID** | `22` (`VOID`) |
| **Symbol** | `▦` |
| **Type** | `void` |
| **Color (HSV)** | `(270, 60, 30)` |
| **Transparency** | `0` |
| **Weight** | `0` |
