# Shifting Sand

A terminal-based falling-sand sandbox simulation written in Python, featuring **23 interactive elements**, **4-way rotatable gravity**, **dynamic colored lighting**, **uranium radiation raycasting**, and **11 brush shapes**—all rendered in 24-bit TrueColor and Unicode inside your terminal.

> Made for the **2026 itch.io Game Off** by [**Artemis689**](https://artemis689.itch.io).

---

## Features

* **23 Interactive Elements:** Powders, liquids, gases, solids, combustibles, crystals, radiation, cloners, pumps, and voids—with rich chemical and physical interactions. *(See [Elements.md](Elements.md) for full details.)*
* **4-Way Rotatable Gravity:** Shift gravity **Down**, **Up**, **Left**, or **Right** on the fly.
* **Dynamic Lighting & Glow:** Real-time raycast lighting from a movable light source, per-element light transparency, emissive glow from **Fire**, **Lava**, and **Crystal**, plus oscillating chromatic hue tinting from Crystals.
* **Radiation & Optics:** **Uranium** emits radiation rays that react with matter, reflect off **Graphite** mirrors, focus toward your pointer through **Glass**, and are shielded by **Obsidian**.
* **11 Brush Shapes & Flood Fill:** Draw with squares, circles, diamonds (solid or hollow), horizontal/vertical/diagonal lines, or a bounded/unbounded Fill Tool, with brush sizes from `0` to `10`.
* **Time & History Controls:** Pause simulation, adjust speed from `1` to `500` FPS, step forward frame-by-frame, or step backward through up to `1000` undo states.
* **Achievements & Audio:** Persistent achievement tracking (`data.json`) with animated fade-out popups, background music, and sound effects.
* **Performance Mode:** Toggles dynamic lighting off and trims undo history for smoother performance on slower terminals.

---

## Requirements

* **OS:** Windows (input handling uses `msvcrt` and `ctypes` Win32 APIs)
* **Terminal:** **Windows Terminal** (recommended for full 24-bit TrueColor & Unicode box-drawing support)
* **Python:** **Python 3.12+**
* **Dependencies:**
  * `pygame` (for `pygame.mixer` audio)
  * `pyautogui` (for automatic fullscreen `F11` and zoom scaling on launch/exit)

---

## Installation & Running

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```

2. **Install dependencies:**
   ```bash
   pip install pygame pyautogui
   ```

3. **Verify required asset files are present:**
   ```text
   ├── data.json
   ├── Elements.md
   ├── Controls.md
   └── sounds/
       ├── music/
       │   └── Kowloon.mp3
       └── sfx/
           ├── about.wav
           ├── achievement.wav
           ├── enter.wav
           ├── esc.wav
           ├── exit.wav
           ├── menutogame.wav
           └── settings.wav
   ```

4. **Run the game** (in Windows Terminal):
   ```bash
   python main.py
   ```
   *(Replace `main.py` with your entry script filename if different. The game automatically toggles fullscreen and terminal zoom on startup, and restores them when exiting cleanly.)*

---

## Controls Quick Reference

For complete documentation, see [Controls.md](Controls.md).

### Main Menu & Settings
| Key | Action |
| :--- | :--- |
| `W` / `S` or `↑` / `↓` | Navigate menu options |
| `Space` / `Enter` / `→` | Select option / adjust setting |
| `Esc` / `Backspace` / `Del` / `←` | Return to previous menu |

### Simulation
| Key | Action |
| :--- | :--- |
| `w` `a` `s` `d` | Move pointer |
| `W` `A` `S` `D` *(Shift + WASD)* | Jump pointer across contiguous cells of the same element |
| `Space` | Draw with current brush shape, size, and element |
| `Enter` | Place single cell at pointer |
| `Del` | Erase single cell at pointer |
| `q` / `e` | Previous / next element |
| `Q` / `E` | Previous / next brush shape |
| `-` / `=` | Decrease / increase brush size |
| `_` / `+` | Set brush size to min (`0`) / max (`10`) |
| `↑` `↓` `←` `→` | Rotate gravity direction |
| `Shift` + `↑` `↓` `←` `→` | Move light source (bulb) position |
| `\` | Pause / resume simulation |
| `[` / `]` *(Running)* | Decrease / increase frame rate (`1–500` FPS) |
| `[` / `]` *(Paused)* | Undo one frame / step forward one frame |
| `C` | Clear the grid |
| `Tab` | Shuffle all cells on the grid |
| `` ` `` | Toggle pointer / sand hue cycling |
| `/` | Toggle radiation ray visibility |
| `Esc` / `Backspace` | Return to main menu |

---

## Elements

All 23 elements—**Air**, **Sand**, **Water**, **Steel**, **Acid**, **Steam**, **Dry Wood**, **Wet Wood**, **Fire**, **Lava**, **Obsidian**, **Gunpowder**, **Fuse**, **Uranium**, **Crystal**, **Glass**, **Graphite**, **Ice**, **Oil**, **Fumes**, **Morph**, **Pump**, and **Void**—have unique mechanics and reactions.

Read the full breakdown in **[Elements.md](Elements.md)**.

---

## Credits

* **Developer:** Artemis689
* **Music:** *Kowloon* by DIGITAL DESCENDANT ([Spotify](https://open.spotify.com/track/4RTvCdg3jpSkwkejofKjb1))
* **Sound Effects:** [mixkit.co](https://mixkit.co)
* **ASCII Fonts:** *Lingahoulic Rounded*, *Future Rounded*, *Future (modified)*
* **AI Usage Note:** AI was used very sparingly in writing code (only one or two helper functions) and extensively for playtesting and bug reporting.
```
