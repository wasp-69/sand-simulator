import sys
import random
from time import sleep, perf_counter
from colorsys import hsv_to_rgb
import math
from collections import deque
import pygame.mixer as mixer
import json
import pyautogui

AIR, SAND, WATER, STEEL, ACID, STEAM, DRYWOOD, WETWOOD, FIRE, LAVA, OBSIDIAN, GUNPOWDER, FUSE, URANIUM, CRYSTAL, GLASS, GRAPHITE, ICE, OIL, FUMES, MORPH, PUMP, VOID = \
      0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22

class Timer:

    def __init__(self):
        self.starting_time = perf_counter()
        self.current_time = perf_counter()

    def reset(self):
        self.starting_time = perf_counter()

    def diff(self):
        self.current_time = perf_counter()
        return self.current_time - self.starting_time

class Popup:
    instances = []
    def __init__(self, text):
        self.text = text
        self.alpha = 0
        Popup.instances.append(self)

    def display(self):
        self.alpha = 100

    def update(self, dec):
        self.alpha = max(0, self.alpha - dec)

    @classmethod
    def updateall(cls, dec):
        for instance in cls.instances:
            instance.update(dec)

class TitleScreen:

    def __init__(self):
        global SFX_VOL, MUSIC_VOL, PERFORMANCE_MODE, DYNAMIC_LIGHTING, UNDO_LIST
        # FONT -> Title: Lingahoulic Rounded | Options: Future (modified)
        self.TITLE = """
╭───────╮ ╭─╮       ╭─╮   ╭─────╮   ╭─╮     ╭─╮                             ╭───────╮                             ╭─╮ 
│ ╭─────╯ │ ╰─────╮ ╰─╯   │ ╭───╯ ╭─╯ ╰─╮   ╰─╯ ╭───────╮ ╭───────╮         │ ╭─────╯ ╭───────╮   ╭───────╮ ╭─────╯ │ 
│ ╰─────╮ │ ╭───╮ │ ╭─╮ ╭─╯ ╰─╮   ╰─╮ ╭─╯   ╭─╮ │ ╭───╮ │ │ ╭───╮ │         │ ╰─────╮ │ ╭───╮ │   │ ╭───╮ │ │ ╭───╮ │ 
╰─────╮ │ │ │   │ │ │ │ ╰─╮ ╭─╯     │ │     │ │ │ │   │ │ │ │   │ │         ╰─────╮ │ │ │   │ │   │ │   │ │ │ │   │ │ 
╭─────╯ │ │ │   │ │ │ │   │ │       │ ╰───╮ │ │ │ │   │ │ │ ╰───╯ │         ╭─────╯ │ │ ╰───╯ ╰─╮ │ │   │ │ │ ╰───╯ │ 
╰───────╯ ╰─╯   ╰─╯ ╰─╯   ╰─╯       ╰─────╯ ╰─╯ ╰─╯   ╰─╯ ╰─────╮ │         ╰───────╯ ╰─────────╯ ╰─╯   ╰─╯ ╰───────╯ 
                                                            ╭───╯ │                                                   
                                                            ╰─────╯    
"""
        self.options = ["PLAY", "SETTINGS", "ABOUT", "EXIT"]
        self.settings = ["PERFORMANCE MODE", "MUSIC VOL", "SFX VOL", "DEFAULT"]
        self.empty_ascii_dict = {
        "PLAY": """
┏━┓   ┏━┓ ╻   ┏━┓ ╻ ╻\033[K
┃ ┃   ┣━┛ ┃   ┣━┫ ┗┳┛\033[K
┗━┛   ╹   ┗━╸ ╹ ╹  ╹ \033[K
""",
        "SETTINGS": """
┏━┓   ┏━┓ ┏━╸ ╺┳╸ ╺┳╸ ╻ ┏┓╻ ┏━╸ ┏━┓\033[K
┃ ┃   ┗━┓ ┣╸   ┃   ┃  ┃ ┃┃┃ ┃╺┓ ┗━┓\033[K
┗━┛   ┗━┛ ┗━╸  ╹   ╹  ╹ ╹┗┛ ┗━┛ ┗━┛\033[K
""",
        "ABOUT": """
┏━┓   ┏━┓ ┏━┓ ┏━┓ ╻ ╻ ╺┳╸\033[K
┃ ┃   ┣━┫ ┣━┫ ┃ ┃ ┃ ┃  ┃ \033[K
┗━┛   ╹ ╹ ┗━┛ ┗━┛ ┗━┛  ╹ \033[K
""", 
        "EXIT": """
┏━┓   ┏━╸ ╻ ╻ ╻ ╺┳╸\033[K
┃ ┃   ┣╸  ┏╋┛ ┃  ┃ \033[K
┗━┛   ┗━╸ ╹ ╹ ╹  ╹ \033[K
"""
    }
        self.check_ascii_dict = {
        "PLAY": """
┏━┓    ┏━┓ ╻   ┏━┓ ╻ ╻\033[K
┃┃┃    ┣━┛ ┃   ┣━┫ ┗┳┛\033[K
┗━┛    ╹   ┗━╸ ╹ ╹  ╹ \033[K
""",
        "SETTINGS": """
┏━┓    ┏━┓ ┏━╸ ╺┳╸ ╺┳╸ ╻ ┏┓╻ ┏━╸ ┏━┓\033[K
┃┃┃    ┗━┓ ┣╸   ┃   ┃  ┃ ┃┃┃ ┃╺┓ ┗━┓\033[K
┗━┛    ┗━┛ ┗━╸  ╹   ╹  ╹ ╹┗┛ ┗━┛ ┗━┛\033[K
""",
        "ABOUT": """
┏━┓    ┏━┓ ┏━┓ ┏━┓ ╻ ╻ ╺┳╸\033[K
┃┃┃    ┣━┫ ┣━┫ ┃ ┃ ┃ ┃  ┃ \033[K
┗━┛    ╹ ╹ ┗━┛ ┗━┛ ┗━┛  ╹ \033[K
""", 
        "EXIT": """
┏━┓    ┏━╸ ╻ ╻ ╻ ╺┳╸\033[K
┃┃┃    ┣╸  ┏╋┛ ┃  ┃ \033[K
┗━┛    ┗━╸ ╹ ╹ ╹  ╹ \033[K
"""
    }
        self.check_setting_dict = { 
     "PERFORMANCE MODE":
"""
╭─╮      ╭─╮╭─╴╭─╮╭─╴╭─╮╭─╮╭┬╮╭─╮╭╮╷╭─╴╭─╴   ╭┬╮╭─╮╶┬╮╭─╴\033[K
│││      ├─╯├╴ ├┬╯├╴ │ │├┬╯│││├─┤│╰┤│  ├╴    ││││ │ ││├╴ \033[K
╰─╯      ╵  ╰─╴╵╰╴╵  ╰─╯╵╰╴╵ ╵╵ ╵╵ ╵╰─╴╰─╴   ╵ ╵╰─╯╶┴╯╰─╴\033[K
""", "MUSIC VOL":
"""
╭─╮      ╭┬╮╷ ╷╭─╮╷╭─╴   ╷  ╷╭─╮╷  \033[K
│││      ││││ │╰─╮││     ╰╮╭╯│ ││  \033[K
╰─╯      ╵ ╵╰─╯╰─╯╵╰─╴    ╰╯ ╰─╯╰─╴\033[K
""", "SFX VOL":
"""
╭─╮      ╭─╮╭─╴╷ ╷   ╷  ╷╭─╮╷  \033[K
│││      ╰─╮├╴ ╭┼╯   ╰╮╭╯│ ││  \033[K
╰─╯      ╰─╯╵  ╵ ╵    ╰╯ ╰─╯╰─╴\033[K
""", "DEFAULT":
"""
╭─╮      ╶┬╮╭─╴╭─╴╭─╮╷ ╷╷  ╶┬╴\033[K
│││       ││├╴ ├╴ ├─┤│ ││   │ \033[K
╰─╯      ╶┴╯╰─╴╵  ╵ ╵╰─╯╰─╴ ╵ \033[K
"""
        }
        self.empty_setting_dict = {
     "PERFORMANCE MODE":
"""
╭─╮     ╭─╮╭─╴╭─╮╭─╴╭─╮╭─╮╭┬╮╭─╮╭╮╷╭─╴╭─╴   ╭┬╮╭─╮╶┬╮╭─╴\033[K
│ │     ├─╯├╴ ├┬╯├╴ │ │├┬╯│││├─┤│╰┤│  ├╴    ││││ │ ││├╴ \033[K
╰─╯     ╵  ╰─╴╵╰╴╵  ╰─╯╵╰╴╵ ╵╵ ╵╵ ╵╰─╴╰─╴   ╵ ╵╰─╯╶┴╯╰─╴\033[K
""", "MUSIC VOL":
"""
╭─╮     ╭┬╮╷ ╷╭─╮╷╭─╴   ╷  ╷╭─╮╷  \033[K
│ │     ││││ │╰─╮││     ╰╮╭╯│ ││  \033[K
╰─╯     ╵ ╵╰─╯╰─╯╵╰─╴    ╰╯ ╰─╯╰─╴\033[K
""", "SFX VOL":
"""
╭─╮     ╭─╮╭─╴╷ ╷   ╷  ╷╭─╮╷  \033[K
│ │     ╰─╮├╴ ╭┼╯   ╰╮╭╯│ ││  \033[K
╰─╯     ╰─╯╵  ╵ ╵    ╰╯ ╰─╯╰─╴\033[K
""", "DEFAULT":
"""
╭─╮     ╶┬╮╭─╴╭─╴╭─╮╷ ╷╷  ╶┬╴\033[K
│ │      ││├╴ ├╴ ├─┤│ ││   │ \033[K
╰─╯     ╶┴╯╰─╴╵  ╵ ╵╰─╯╰─╴ ╵ \033[K
"""
        }
        self.variable_dict = {
            "PERFORMANCE MODE": PERFORMANCE_MODE,
            "MUSIC VOL": MUSIC_VOL*100,
            "SFX VOL": SFX_VOL*100,
            "DEFAULT": "---"
        }

        self.rgb = 0
        self.ht = 0
        self.pointer = 0
        self.key = None
        self.screentype = "main"
        self.running = True
        self.lower = ""

        self.playsound = mixer.Sound("sounds/sfx/about.wav")
        self.playsound.set_volume(SFX_VOL - 0.3)
        self.exitsound = mixer.Sound("sounds/sfx/exit.wav")
        self.exitsound.set_volume(SFX_VOL)
        self.aboutsound = mixer.Sound("sounds/sfx/menutogame.wav")
        self.aboutsound.set_volume(SFX_VOL)
        self.settingssound = mixer.Sound("sounds/sfx/settings.wav")
        self.settingssound.set_volume(SFX_VOL)

    def tick(self):
        self.rgb += 0.001
        if random.random() < 0.1: self.ht += 0.01

        self.key = get_keypress()
        self.handle_pointer()
        if self.screentype == "settings":
            self.handle_settings_pointer()
        else:
            self.handle_action()

    def refresh(self):
        reset_terminal_cursor_pos()

        sys.stdout.write(self.handle_gradient())
        self.handle_options()
        sys.stdout.write(self.lower)

        sys.stdout.flush()

    def handle_pointer(self):
        if self.screentype == "main":
            if self.key in ("DOWN", "S", "s"):
                self.pointer = (self.pointer + 1) % len(self.options)
            elif self.key in ("UP", "W", "w"):
                self.pointer = (self.pointer - 1) % len(self.options)

    def handle_action(self):
        if self.screentype == "main":
            if self.key in ("enter", " ", "RIGHT"):    
                selected = self.options[self.pointer]
                if selected == "PLAY":
                    self.handle_play()
                elif selected == "SETTINGS":
                    self.handle_settings()
                elif selected == "ABOUT":
                    self.handle_about()
                elif selected == "EXIT":
                    self.handle_exit()

        elif self.key in ("esc", "del", "backspace", "LEFT"):
            wipe_terminal_screen()
            self.screentype = "main"

    def handle_play(self):
        self.playsound.play()
        self.running = False

    def handle_settings(self):
        self.settingssound.play()
        self.pointer = 0
        self.screentype = "settings"

    def handle_about(self):
        self.aboutsound.play()
        self.screentype = "about"
        self.lower ="""

╭─╮╭─╮╭─╮╷ ╷╶┬╴
├─┤├─┤│ ││ │ │ 
╵ ╵╰─╯╰─╯╰─╯ ╵ 

A sandbox simulation game with 23 interactive elements, 4-way rotatable gravity, dynamic lighting, 11 brush shapes.
Best played in Windows Terminal (TrueColor & Unicode). Game will restore terminal settings upon exit.
Check out Controls.md for detailed documentation of the controls in the simulation.
Check out Elements.md for detailed documentation on the various elements in the game.
This game was made for the 2026 itch.io game off. Made entirely by Artemis689 in about one month. 


╷ ╷╭─╮╭─╴   ╭─╮╭─╴   ╭─╮  ╷ 
│ │╰─╮├╴    │ │├╴    ├─┤  │ 
╰─╯╰─╯╰─╴   ╰─╯╵     ╵ ╵╵ ╵╵

A.I. was used very sparingly in the development of this game. Only one or two functions were written by the help of A.I. 
A.I. was extensively used as the playtester for this game and to report bugs.


╭─╮╭─╮╭─╮╭─╴╶┬╴╭─╮
├─┤╰─╮╰─╮├╴  │ ╰─╮
╵ ╵╰─╯╰─╯╰─╴ ╵ ╰─╯

ASCII Fonts: Lingahoulic Rounded, Future Rounded, Future (modified)
Music: [Kowloon by DIGITAL DESCENDANT] [https://open.spotify.com/track/4RTvCdg3jpSkwkejofKjb1] | SFX: mixkit.co






\x1b[2m[Press ESC, Backspace, or ← to return]\x1b[22m
""" 
        wipe_terminal_screen()

    def handle_exit(self):
        self.exitsound.play()
        show_terminal_cursor()
        while mixer.get_busy():
            sleep(0.1)
        wipe_terminal_screen()
        pyautogui.hotkey("f11")
        pyautogui.hotkey("ctrl","0")
        mixer.quit()
        sys.exit(0)

    def handle_settings_pointer(self):
        global PERFORMANCE_MODE, UNDO_LIST, DYNAMIC_LIGHTING, SFX_VOL, MUSIC_VOL, MAX_UNDO

        if self.key in ("DOWN", "S", "s"):
            self.pointer = (self.pointer + 1) % len(self.settings)
        elif self.key in ("UP", "W", "w"):
            self.pointer = (self.pointer - 1) % len(self.settings)

        screen = ""

        for i, sett in enumerate(self.settings):
            if i == self.pointer:   
                screen +=  self.check_setting_dict[sett]
                screen += " "
            else: 
                screen += self.empty_setting_dict[sett]
            value = self.variable_dict[sett]
            if sett == "PERFORMANCE MODE": value = "ON" if value else "OFF"
            screen += "        [" + str(value) + "]"

            screen += "\033[K\n\033[K\n"
        screen += """







\x1b[2m[Press ESC, Backspace, or ← to return]\x1b[22m"""

        self.lower = screen

        selected = self.settings[self.pointer]
        if self.key in (" ", "enter", "RIGHT"):

            if selected == "PERFORMANCE MODE":
                PERFORMANCE_MODE = not PERFORMANCE_MODE
                DYNAMIC_LIGHTING = not DYNAMIC_LIGHTING
                if PERFORMANCE_MODE:
                    UNDO_LIST = deque(UNDO_LIST, maxlen=100)
                else:
                    UNDO_LIST = deque(UNDO_LIST, maxlen=MAX_UNDO)

            elif selected == "MUSIC VOL":
                MUSIC_VOL = round((MUSIC_VOL + 0.01) % 1, 2)
                mixer.music.set_volume(MUSIC_VOL)

            elif selected == "SFX VOL":
                SFX_VOL = round((SFX_VOL + 0.01) % 1, 2)
                self.playsound.set_volume(SFX_VOL - 0.3)
                self.aboutsound.set_volume(SFX_VOL)
                self.settingssound.set_volume(SFX_VOL)
                self.exitsound.set_volume(SFX_VOL)

            elif selected == "DEFAULT":
                PERFORMANCE_MODE = False
                DYNAMIC_LIGHTING = True
                UNDO_LIST = deque(UNDO_LIST, maxlen=MAX_UNDO)
                MUSIC_VOL = 0.2
                SFX_VOL = 0.5
                mixer.music.set_volume(MUSIC_VOL)
                self.playsound.set_volume(SFX_VOL - 0.3)
                self.aboutsound.set_volume(SFX_VOL)
                self.settingssound.set_volume(SFX_VOL)
                self.exitsound.set_volume(SFX_VOL)

        if self.key in ("esc", "del", "backspace", "LEFT"):
            wipe_terminal_screen()
            self.pointer = 1
            self.screentype = "main"

        self.variable_dict = {
            "PERFORMANCE MODE": PERFORMANCE_MODE,
            "MUSIC VOL": MUSIC_VOL*100,
            "SFX VOL": SFX_VOL*100,
            "DEFAULT": "---"
        }
            
    def handle_options(self) -> str:
        if self.screentype != "main":
            return ""
        screen = ""

        for i, opt in enumerate(self.options):
            if i == self.pointer:    screen +=  self.check_ascii_dict[opt]
            else: screen += self.empty_ascii_dict[opt]
            screen += "\033[K\n\033[K\n"

        self.lower = screen

    def handle_gradient(self) -> str:
        gradient = []
        title = self.TITLE.split("\n")
        b = 0
        s = math.sin
        c = math.cos

        for y, line in enumerate(title):
            a = b
            for x, letter in enumerate(line):
                h = (s(self.ht) + c(2*self.rgb) - c(4*self.rgb) - s(self.rgb))
                txt = color(letter, (h*100 + a + x+y, 50, 100))
                gradient.append(txt)
            b += 1
            gradient.append("\n")

        return "".join(gradient)
    
class Cell:

    def __init__(self, row, col, state=AIR):
        self.state = state
        self.row = row
        self.col = col
        self.update = True
        self.uraniumdecaystage = 0
        self.contaminated = False
        self.light_level = 100
        self.add_hue = None
        self.crystal_glow = 1

    def get_sand_hue(self, height, length):
        global RAINBOW_SAND, HUE
        theta = math.radians(HUE)
        if not RAINBOW_SAND:
            return 38
        else:
            avg = average(math.sin(theta)*(self.row / height), math.cos(theta)*(self.col / length))
            return (avg * 360 ) + HUE 

    def type(self):
        global PROFILE, TYPE_DICT
        symbol = PROFILE[self.state]["symbol"]
        return TYPE_DICT[symbol]

class Grid:

    def __init__(self, length, height):
        global DEFAULT_BRUSH_SIZE, MAX_BRUSH_SIZE, MIN_BRUSH_SIZE
        self.length = length
        self.height = height

        self.show_pointer = 1
        self.pointer_x = 0
        self.pointer_y = 0

        self.min_brush_size = MIN_BRUSH_SIZE
        self.max_brush_size = MAX_BRUSH_SIZE
        self.brush_size = DEFAULT_BRUSH_SIZE
        self.brush_type = 1
        self.brush_shape = 0

        self.show_radiation_lines = True

        self.orientation = "up"

        self.matrix = [[Cell(row=row, col=col) for col in range(length)]
                       for row in range(height)]
        self.edges = self.get_edges(True)                                      # with the top one

        self.glow_kernel = [[0] * 11 for _ in range(11)] 
        for y, row in enumerate(self.glow_kernel):
            for x, cell in enumerate(row):
                relx = abs(5 - x)   
                rely = abs(5 - y)
                dist = relx + rely
                inv_dist = 10 - dist
                biased = inv_dist * 5
                final = biased ** 0.5
                self.glow_kernel[y][x] = final

    def swap(self, cell1: Cell, cell2: Cell):
        cell1.state, cell2.state = cell2.state, cell1.state
        cell1.uraniumdecaystage, cell2.uraniumdecaystage = cell2.uraniumdecaystage, cell1.uraniumdecaystage
        cell1.crystal_glow, cell2.crystal_glow = cell2.crystal_glow, cell1.crystal_glow

    def reset_update_flags(self):
        for x in range(0, self.length):
            for y in range(0, self.height):
                self.matrix[y][x].update = True

    def reset_radiation_flags(self):
        for x in range(0, self.length):
            for y in range(0, self.height):
                c = self.matrix[y][x]
                c.contaminated = False
                if c.state != CRYSTAL:
                    c.crystal_glow = 1

    def reset_add_hue(self):
        for x in range(0, self.length):
            for y in range(0, self.height):
                self.matrix[y][x].add_hue = None

    def up(self, cell, n: int = 1, static = False) -> Cell:
        if not cell:
            return None
        if static:
            top = "up"
        else:
            top = self.orientation
        x = cell.col
        y = cell.row
        if top == "up":
            if y - n >= 0:
                return self.matrix[y - n][x]
        elif top == "down":
            if y + n < self.height:
                return self.matrix[y + n][x]
        elif top == "left":
            if x - n >= 0:
                return self.matrix[y][x - n]
        elif top == "right":
            if x + n < self.length:
                return self.matrix[y][x + n]
        else:
            return None

    def down(self, cell, n: int = 1, static = False) -> Cell:
        if not cell:
            return None
        if static:
            top = "up"
        else:
            top = self.orientation
        x = cell.col
        y = cell.row
        if top == "up":
            if y + n < self.height:
                return self.matrix[y + n][x]
        elif top == "down":
            if y - n >= 0:
                return self.matrix[y - n][x]
        elif top == "left":
            if x + n < self.length:
                return self.matrix[y][x + n]
        elif top == "right":
            if x - n >= 0:
                return self.matrix[y][x - n]
        else:
            return None

    def left(self, cell, n: int = 1, static = False) -> Cell:
        if not cell:
            return None
        if static:
            top = "up"
        else:
            top = self.orientation
        x = cell.col
        y = cell.row
        if top == "up":
            if x - n >= 0:
                return self.matrix[y][x - n]
        elif top == "down":
            if x + n < self.length:
                return self.matrix[y][x + n]
        elif top == "left":
            if y + n < self.height:
                return self.matrix[y + n][x]
        elif top == "right":
            if y - n >= 0:
                return self.matrix[y - n][x]
        else:
            return None

    def right(self, cell, n: int = 1, static = False) -> Cell:
        if not cell:
            return None
        if static:
            top = "up"
        else:
            top = self.orientation
        x = cell.col
        y = cell.row
        if top == "up":
            if x + n < self.length:
                return self.matrix[y][x + n]
        elif top == "down":
            if x - n >= 0:
                return self.matrix[y][x - n]
        elif top == "left":
            if y - n >= 0:
                return self.matrix[y - n][x]
        elif top == "right":
            if y + n < self.height:
                return self.matrix[y + n][x]
        else:
            return None

    def update(self):
        global FRAMENUM
        self.reset_update_flags()

        vertical = self.orientation in ("up", "down")
        if vertical:
            outer_range = range(self.height - 1, -1, -1) if self.orientation == "up" else range(self.height)
            inner_len = self.length
        else:
            outer_range = range(self.length - 1, -1, -1) if self.orientation == "left" else range(self.length)
            inner_len = self.height

        for outer in outer_range:
            if (outer + FRAMENUM) % 2 == 0:
                inner_range = range(inner_len - 1, -1, -1)
            else:
                inner_range = range(inner_len)

            for inner in inner_range:
                x, y = (inner, outer) if vertical else (outer, inner)
                cell = self.matrix[y][x]

                if cell.state != URANIUM:
                    cell.uraniumdecaystage = 0
                if cell.state == SAND:
                    self.handle_sand(cell)
                elif cell.state == WATER:
                    self.handle_water(cell)
                elif cell.state == ACID:
                    self.handle_acid(cell)
                elif cell.state == STEAM:
                    self.handle_steam(cell)
                elif cell.state == DRYWOOD:
                    self.handle_drywood(cell)
                elif cell.state == FIRE:
                    self.handle_fire(cell)
                elif cell.state == LAVA:
                    self.handle_lava(cell)
                elif cell.state == OBSIDIAN:
                    self.handle_obsidian(cell)
                elif cell.state == GUNPOWDER:
                    self.handle_gunpowder(cell)
                elif cell.state == FUSE:
                    self.handle_fuse(cell)
                elif cell.state == URANIUM:
                    self.handle_uranium(cell)
                elif cell.state == GLASS:
                    self.handle_glass(cell)
                elif cell.state == CRYSTAL:
                    self.handle_crystal(cell)
                elif cell.state == GRAPHITE:
                    self.handle_graphite(cell)
                elif cell.state == ICE:
                    self.handle_ice(cell)
                elif cell.state == OIL:
                    self.handle_oil(cell)
                elif cell.state == FUMES:
                    self.handle_fumes(cell)
                elif cell.state == MORPH:
                    self.handle_cloner(cell)
                elif cell.state == PUMP:
                    self.handle_pump(cell)
                elif cell.state == VOID:
                    self.handle_void(cell)

# MARK: Elements

    def handle_sand(self, cell: Cell):
        if random.randint(0,1):
            first = self.left(cell)
            second = self.right(cell)
        else:
            first = self.right(cell)
            second = self.left(cell)

        # for normal gravity 
        if self.down(cell) and self.down(cell).state == AIR:
            self.swap(cell, self.down(cell))
        elif cell.update and self.down(cell) and first and self.down(first).state == AIR:
            self.swap(cell, self.down(first))
            self.down(first).update = False
        elif cell.update and self.down(cell) and second and self.down(second).state == AIR:
            self.swap(cell, self.down(second))
            self.down(second).update = False

        # for swapping with water (density swap)
        elif self.down(cell) and self.down(cell).state in (WATER, OIL):
            self.swap(cell, self.down(cell))
        elif cell.update and self.down(cell) and first and self.down(first).state in (WATER, OIL):
            self.swap(cell, self.down(first))
            self.down(first).update = False
        elif cell.update and self.down(cell) and second and self.down(second).state in (WATER, OIL):
            self.swap(cell, self.down(second))
            self.down(second).update = False

    def handle_water(self, cell: Cell):
        if random.randint(0,1):
            first = self.left(cell)
            second = self.right(cell)
        else:
            first = self.right(cell)
            second = self.left(cell)

        # for normal gravity 
        if self.down(cell) and self.down(cell).state in (AIR, OIL):
            self.swap(cell, self.down(cell))
            self.down(cell).update = False 
        elif cell.update and first and first.state in (AIR, OIL):
            self.swap(cell, first)
            first.update = False
        elif cell.update and second and second.state in (AIR, OIL):
            self.swap(cell, second)
            second.update = False

        # plan to add better behaviour:
        # find to which side, left or right, does more empty cells exist
        # then move to that side

    def handle_acid(self, cell: Cell):
        if random.randint(0,1):
            first = self.left(cell)
            second = self.right(cell)
        else:
            first = self.right(cell)
            second = self.left(cell)

        # for acid dissoulution
        n: tuple[Cell] = neighbours(cell, self, 3, True)

        for nearby in n:
            if nearby.state == SAND:
                cell.state = AIR
                nearby.state = AIR
                return
            elif nearby.state == WATER:
                cell.state = AIR
                nearby.state = STEAM
                handle_achievement("Chemistry!")
                return
            elif nearby.state == STEEL:
                if random.random() < 0.01:
                    nearby.state = AIR
            elif nearby.state == DRYWOOD:
                cell.state = AIR
                nearby.state = FIRE
                return
            elif nearby.state == WETWOOD:
                cell.state = AIR
                nearby.state = STEAM
                return
            elif nearby.state == FIRE:
                nearby.state = AIR
            elif nearby.state in (GUNPOWDER, FUSE):
                if random.random() < 0.5:
                    nearby.state = FIRE
            elif nearby.state == URANIUM:
                if nearby.uraniumdecaystage > 7:
                    nearby.uraniumdecaystage = 0
                    cell.state = WATER
                    return
            elif nearby.state == CRYSTAL:
                nearby.crystal_glow += 2
            elif nearby.state == OIL:
                nearby.state = AIR
                cell.state = AIR
                return              

        # for normal gravity 
        if self.down(cell) and self.down(cell).state == AIR:
            self.swap(cell, self.down(cell))
            self.down(cell).update = False 
        elif cell.update and first and first.state == AIR:
            self.swap(cell, first)
            first.update = False
        elif cell.update and second and second.state == AIR:
            self.swap(cell, second)
            second.update = False

    def handle_steam(self, cell: Cell):
        # condensation
        up_cell = self.up(cell)
        if (up_cell is None) or (up_cell.type() in ("solid", "glass", "pump")):
            if random.random() < 0.01:
                cell.state = WATER
                return
            
        swappable = (AIR, SAND, WATER, ACID, FIRE, GUNPOWDER, URANIUM, OIL, FUMES)
        self.gas_behavior(cell, up_cell, swappable)

    def gas_behavior(self, cell: Cell, up_cell: Cell, swappable):
        if random.randint(0,1):
            first = self.left(cell)
            second = self.right(cell)
        else:
            first = self.right(cell)
            second = self.left(cell)

        # normal gravity
        if up_cell and cell.update and up_cell.state in swappable:
            self.swap(cell, up_cell)
            up_cell.update = False 
        elif cell.update and up_cell and first and self.up(first).state in swappable:
            self.swap(cell, self.up(first))
            self.up(first).update = False
        elif cell.update and up_cell and second and self.up(second).state in swappable:
            self.swap(cell, self.up(second))
            self.up(second).update = False
        elif cell.update and first and first.state == AIR:
            self.swap(cell, first)
            first.update = False
        elif cell.update and second and second.state == AIR:
            self.swap(cell, second)
            second.update = False

    def handle_drywood(self, cell: Cell):
        # for normal gravity 
        if self.down(cell) and self.down(cell).state in (AIR, STEAM, FIRE):
            self.swap(cell, self.down(cell))
        else:
            n: tuple[Cell] = neighbours(cell, self, 3, True)
            for nearby in n:
                if nearby.state == WATER:
                    cell.state = WETWOOD
                    nearby.state = AIR
                    return

    def handle_fire(self, cell: Cell):
        n: tuple[Cell] = neighbours(cell, self, 5, True)
        not_flammables = (AIR, WATER, STEEL, SAND, ACID, STEAM, FIRE, LAVA, OBSIDIAN, URANIUM, CRYSTAL, GLASS, GRAPHITE, MORPH, PUMP)

        if all(cell.state in not_flammables for cell in n): # fire is surrounded by non-flammable materials
            if random.random() < 0.2:
                cell.state = AIR
                return
            if self.up(cell) and cell.update and self.up(cell).state == AIR:
                self.swap(cell, self.up(cell))
                self.up(cell).update = False

        for current in n: # else,
            if current.state == WATER:
                cell.state = AIR
                return
            if cell.update:
                if current.state in (GUNPOWDER, FUSE):
                    current.state = FIRE
                    current.update = False
                if current.state == ICE:
                    current.state = WATER
                    current.update = False
                if current.state in (DRYWOOD, OIL) and random.random() < 0.1:
                    for nearby in n:
                        if nearby.state == AIR and random.random() < 0.75:
                            nearby.state = FIRE
                            nearby.update = False
                            handle_achievement("Spontaneous Combustion!")
                    if current.state == DRYWOOD and random.random() < 0.01:
                        current.state = AIR
                    if current.state == OIL and random.random() < 0.1:
                        current.state = AIR
                if current.state == WETWOOD and random.random() < 0.01:
                    current.state = DRYWOOD
                    cell.state = STEAM
                    current.update = False
                    return
                if current.state == FUMES:
                    current.state = FIRE
                    current.update = False

    def handle_lava(self, cell: Cell):
        global FRAMENUM

        if FRAMENUM%3 == 0:
            if random.random() < 0.05:
                above = self.up(cell)
                if above and above.state == AIR:
                    above.state = FIRE
            n: tuple[Cell] = neighbours(cell, self, 3, True)

            for nearby in n:
                if nearby.state == SAND:
                    nearby.state = GLASS
                elif nearby.state == WATER:
                    nearby.state = AIR
                    cell.state = OBSIDIAN
                    handle_achievement("Flint... and Steel...")
                    return
                elif nearby.state == STEEL and random.random() < 0.15:
                    nearby.state = AIR
                elif nearby.state == ACID:
                    for i in n:
                        i.state = FIRE
                    cell.state = AIR
                    return
                elif nearby.state == STEAM:
                    nearby.state = AIR
                elif nearby.state in (DRYWOOD, GUNPOWDER, FUSE) and random.random() < 0.075:
                    nearby.state = FIRE
                elif nearby.state == URANIUM and random.random() < 0.1:
                    nearby.uraniumdecaystage += 3
                elif nearby.state == WETWOOD and random.random() < 0.05:
                    nearby.state = FIRE
                    if random.random() < 0.5:
                        cell.state = AIR
                        return
                elif nearby.state == ICE:
                    nearby.state = WATER
                elif nearby.state == GRAPHITE and random.random() < 0.001:
                    nearby.state = GUNPOWDER
                elif nearby.state in (OIL, FUMES):
                    nearby.state = FIRE
                    
            below = self.down(cell)
            if below and below.state == FIRE:
                self.swap(cell, below)
                return
            self.handle_water(cell)

    def handle_obsidian(self, cell: Cell):
        global PROFILE
        w = 0
        cells = []
        for i in range(1, 16):
            cells.append(self.up(cell, i))
        for above_cell in cells:
            if not above_cell:
                break
            above = above_cell.state

            weight = PROFILE[above]["weight"]
            if weight == 0: break
            else: w+= weight

        if w > 20:
            cell.state = AIR

    def handle_gunpowder(self, cell: Cell):
        n: tuple[Cell] = neighbours(cell, self, 5, True)

        for nearby in n:
            if nearby.state == WATER:
                cell.state = WETWOOD
                nearby.state = AIR
                return
            elif nearby.state == LAVA:
                cell.state = FIRE
                return
        self.handle_sand(cell)

    def handle_fuse(self, cell: Cell):
        n: tuple[Cell] = neighbours(cell, self, 5, True)

        for nearby in n:
            if nearby.state == WATER:
                cell.state = WETWOOD
                nearby.state = AIR
                return
            elif nearby.state == LAVA:
                cell.state = FIRE

    def handle_uranium(self, cell: Cell):
        global PAUSED
        if cell.uraniumdecaystage > 11: # death by over-decay
            cell.state = AIR
            return

        if random.random() < 0.01 + (cell.uraniumdecaystage / 200): # random chance to SHOOT radiation ray
            depth = random.randint(0, min(self.length-1, self.height-1))
            if random.random() < 0.5:
                coords = (random.choice([0, self.length-1]), depth)
            else:
                coords = (depth, random.choice([0, self.height-1]))

            to_cell = self.matrix[coords[1]][coords[0]]
            self.handle_raycast(cell, to_cell, extended=False)

        self.handle_sand(cell)

    def handle_raycast(self, from_cell: Cell, to_cell: Cell, extended, recursed=False, to_coords: tuple = None, depth:int = 0, emitter: Cell = None):
        global PROFILE
        if depth >= 100:
            return
        if emitter is None:
            emitter = from_cell

        if to_coords is not None:
            raycast = line(from_cell.col, from_cell.row, to_coords[0], to_coords[1], extend=extended, grid=self)
        else:
            raycast = line(from_cell.col, from_cell.row, to_cell.col, to_cell.row, extend=extended, grid=self)

        for index, ray in enumerate(raycast): # traversing that ray for cells
            if recursed and index == 0:
                continue

            hit_cell = self.matrix[ray[1]][ray[0]]
            dist = get_dist(from_cell, hit_cell, True)
            hit_cell.contaminated = True

            if hit_cell.state == OBSIDIAN: # sheilding effect of obsidian
                break
            elif hit_cell.state == GRAPHITE: # bounce the ray into the correct direction
                dx = hit_cell.col - raycast[0][0]
                dy = hit_cell.row - raycast[0][1]
                toflip = ""
                stepx = hit_cell.col - raycast[index-1][0]
                stepy = hit_cell.row - raycast[index-1][1]

                if stepy == 0:      toflip = "x"
                elif stepx == 0:    toflip = "y"
                else:
                    hor_state = self.matrix[hit_cell.row][hit_cell.col - stepx].state
                    ver_state = self.matrix[hit_cell.row - stepy][hit_cell.col].state

                    if hor_state == GRAPHITE and ver_state != GRAPHITE:     toflip = "y"
                    elif hor_state != GRAPHITE and ver_state == GRAPHITE:   toflip = "x"
                    elif hor_state == ver_state == GRAPHITE:    toflip = "xy"
                    else:
                        if abs(dx) > abs(dy):   toflip = "x"
                        elif abs(dx) < abs(dy):   toflip = "y"
                        else: toflip = "xy"

                rx = -dx if "x" in toflip else dx
                ry = -dy if "y" in toflip else dy
                target = (hit_cell.col + rx, hit_cell.row + ry)

                self.handle_raycast(hit_cell, None, extended=True, recursed=True, to_coords=target, depth=depth+1, emitter=emitter)
                return
            elif hit_cell.state == GLASS:
                target = (self.pointer_x, self.pointer_y)
                self.handle_raycast(hit_cell, None, extended=True, recursed=True, to_coords=target, depth=depth+1, emitter=emitter)
                return
            elif hit_cell.state == CRYSTAL:
                hit_cell.crystal_glow += 50

            if random.random() < 0.2 / (1 + dist / 10): # random chance to have a reaction happen
                if hit_cell.state == WATER:
                    hit_cell.state = ACID
                    emitter.uraniumdecaystage += 1
                elif hit_cell.state == STEEL:
                    hit_cell.state = SAND
                    emitter.uraniumdecaystage += 1
                elif hit_cell.state == DRYWOOD:
                    hit_cell.state = FIRE
                    emitter.uraniumdecaystage += 1
                elif hit_cell.state == SAND and random.random() < 0.3:
                    hit_cell.state = AIR
                    emitter.uraniumdecaystage += 1
                elif hit_cell.state in (GUNPOWDER, FUSE):
                    hit_cell.state = FIRE
                    emitter.uraniumdecaystage += 1
                elif hit_cell.state == ICE:
                    hit_cell.state = WATER
                    emitter.uraniumdecaystage += 1
                elif hit_cell.state == OIL:
                    hit_cell.state = FUMES
                    emitter.uraniumdecaystage += 1
                elif hit_cell.state == FUMES:
                    hit_cell.state = FIRE
                    emitter.uraniumdecaystage += 1
                elif hit_cell.state == MORPH:
                    hit_cell.state = random.choice(list(PROFILE.keys()))
                    emitter.uraniumdecaystage += 1
                elif hit_cell.state == PUMP:
                    if self.up(hit_cell):
                        self.up(hit_cell).state = random.choice(list(PROFILE.keys()))
                        emitter.uraniumdecaystage += 1

    def handle_crystal(self, cell: Cell):
        if cell.crystal_glow > 5000:
            cell.state = GLASS
            return
        if cell.crystal_glow > 1:
            cell.crystal_glow -= 1
            if cell.crystal_glow > 50:
                cell.crystal_glow -= 2
                if cell.crystal_glow > 100:
                    cell.crystal_glow -= 3
        if (cell.light_level == 0) or (random.random() < 1/(cell.light_level**2)):
            n: tuple[Cell, ...] = neighbours(cell, self, 3, True)
            for nearby in n:
                if nearby.state == WATER:
                    nearby.state = CRYSTAL
                    nearby.crystal_glow = 250

    def handle_glass(self, cell: Cell):
        handle_achievement("Transparent")

    def handle_graphite(self, cell: Cell):
        above: Cell = self.up(cell)
        if random.randint(0,1):
            first: Cell = self.left(above)
            second: Cell = self.right(above)
        else:
            first: Cell = self.right(above)
            second: Cell = self.left(above)

        if first is None or second is None:
            return

        immovables = ("solid", "fire", "glass", "pump", "cloner")
        if above and above.type() == "powder":
            if second.update and first.state != AIR:
                if (second.type() not in immovables):
                    if (first.type() not in immovables):
                        self.swap(above, second)
                        second.update = False
            elif first.update and second.state != AIR:
                if (first.type() not in immovables):
                    if (second.type() not in immovables):
                        self.swap(above, first)
                        first.update = False

    def handle_ice(self, cell: Cell):
        global FRAMENUM
        n: list[Cell] = list(neighbours(cell, self, 3, True))
        random.shuffle(n)
        for nearby in n:
            if nearby.state == WATER and random.random() < 0.01:
                nearby.state = ICE
            if nearby.state == STEAM:
                nearby.state = WATER
            if nearby.state == URANIUM:
                nearby.uraniumdecaystage = max(0, nearby.uraniumdecaystage - 1)
                if nearby.uraniumdecaystage < 20 and random.random() < 1/(20-nearby.uraniumdecaystage):
                    cell.state = WATER

    def handle_oil(self, cell: Cell):
        if random.randint(0,1):
            first = self.left(cell)
            second = self.right(cell)
        else:
            first = self.right(cell)
            second = self.left(cell)

        # for normal gravity 
        if self.down(cell) and self.down(cell).state in (AIR, FIRE):
            self.swap(cell, self.down(cell))
            self.down(cell).update = False 
        elif cell.update and first and first.state == AIR:
            self.swap(cell, first)
            first.update = False
        elif cell.update and second and second.state == AIR:
            self.swap(cell, second)
            second.update = False

    def handle_fumes(self, cell: Cell):
        up_cell = self.up(cell)
        swappable = (AIR, SAND, WATER, ACID, FIRE, GUNPOWDER, URANIUM, OIL)
        self.gas_behavior(cell, up_cell, swappable)

    def handle_cloner(self, cell: Cell):
        n: tuple[Cell] = neighbours(cell, self, 3, True)
        for current in n:
            if current.update:
                if current.state not in (AIR, MORPH):
                    cell.update = False
                    cell.state = current.state
                    handle_achievement("Copy Cat!")

    def handle_pump(self, cell: Cell):
        up_cell = self.up(cell)
        down_cell = self.down(cell)

        if up_cell and down_cell and up_cell.state != AIR and down_cell.state in (AIR,):
            if up_cell.state != PUMP:
                down_cell.state = up_cell.state
        
    def handle_void(self, cell: Cell):
        n: tuple[Cell] = neighbours(cell, self, 3, True)
        for current in n:
            if current.update:
                if current.state not in (AIR, VOID):
                    cell.update = False
                    current.state = AIR
                    handle_achievement("His Gluttony Sickens Me.")

# MARK: End Elements

    def handle_pointer(self, key):
        global HUE_CHANGE
        if key == "`":
            HUE_CHANGE = 1 - HUE_CHANGE
        if key == "/":
            self.show_radiation_lines = not self.show_radiation_lines

        if key == "w":
            self.pointer_y = (self.pointer_y - 1) % self.height
        if key == "s":
            self.pointer_y = (self.pointer_y + 1) % self.height
        if key == "a":
            self.pointer_x = (self.pointer_x - 1) % self.length
        if key == "d":
            self.pointer_x = (self.pointer_x + 1) % self.length

        if key in ("W","A","S","D"):
            look = {"W": self.up, "A": self.left, "S": self.down, "D": self.right}[key]
            cur = self.matrix[self.pointer_y][self.pointer_x]

            if look(cur, static=True) is None:
                return
            
            self.handle_pointer(key.lower())
            cur = self.matrix[self.pointer_y][self.pointer_x]
            while True:
                nxt = look(cur, static=True)

                if nxt is None or nxt.state != cur.state:
                    break

                self.handle_pointer(key.lower())
                cur = self.matrix[self.pointer_y][self.pointer_x]

    def handle_action(self, key):
        global ACT_SFX
        brush_size = self.brush_size - 1

        if key in ("backspace", "del"):
            self.matrix[self.pointer_y][self.pointer_x].state = AIR
            return

        if key == "enter":
            self.matrix[self.pointer_y][self.pointer_x].state = self.brush_type
            return

        if key != " " or brush_size < 0:
            return
        self.record_undo()
        ACT_SFX.play()

        # continue work on this
        # complete refactor of the loops, new vars for avg, etc
        min_x = self.pointer_x - brush_size
        max_x = self.pointer_x + brush_size
        min_y = self.pointer_y - brush_size
        max_y = self.pointer_y + brush_size

        # shape: Solid Square
        if self.brush_shape == 0:
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    if y >= 0 and y <= self.height - 1:         # These 2 checks are required for all brush shapes,
                        if x >= 0 and x <= self.length - 1:     # Because they are out-of-bound checks.
                            self.matrix[y][x].state = self.brush_type

        # shape: Hollow Square
        elif self.brush_shape == 1:
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    if abs(x - self.pointer_x) == brush_size or abs(y - self.pointer_y) == brush_size:
                        if y >= 0 and y <= self.height - 1:         # These 2 checks are required for all brush shapes,
                            if x >= 0 and x <= self.length - 1:     # Because they are out-of-bound checks.
                                self.matrix[y][x].state = self.brush_type

        # shape: Solid Circle
        elif self.brush_shape == 2:
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    if ((x - self.pointer_x)**2 + (y - self.pointer_y)**2 - brush_size**2 < brush_size) or brush_size == 0:
                        if y >= 0 and y <= self.height - 1:         # These 2 checks are required for all brush shapes,
                            if x >= 0 and x <= self.length - 1:     # Because they are out-of-bound checks.
                                self.matrix[y][x].state = self.brush_type

        # shape: Hollow Circle
        elif self.brush_shape == 3:
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    omega = (x - self.pointer_x)**2 + (y - self.pointer_y)**2 - brush_size**2
                    if (-brush_size <= omega < brush_size and omega != -brush_size**2) or brush_size == 0:
                        if y >= 0 and y <= self.height - 1:         # These 2 checks are required for all brush shapes,
                            if x >= 0 and x <= self.length - 1:     # Because they are out-of-bound checks.
                                self.matrix[y][x].state = self.brush_type

        # shape: Solid Diamond
        elif self.brush_shape == 4:
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    if abs(x - self.pointer_x) + abs(y - self.pointer_y) <= brush_size:
                        if y >= 0 and y <= self.height - 1:         # These 2 checks are required for all brush shapes,
                            if x >= 0 and x <= self.length - 1:     # Because they are out-of-bound checks.
                                self.matrix[y][x].state = self.brush_type

        # shape: Hollow Diamond
        elif self.brush_shape == 5:
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    if abs(x - self.pointer_x) + abs(y - self.pointer_y) == brush_size:
                        if y >= 0 and y <= self.height - 1:         # These 2 checks are required for all brush shapes,
                            if x >= 0 and x <= self.length - 1:     # Because they are out-of-bound checks.
                                self.matrix[y][x].state = self.brush_type

        # shape: Horizontal Line
        elif self.brush_shape == 6:
            for x in range(min_x, max_x + 1):
                if x >= 0 and x <= self.length - 1:     # Just one check this time.
                    self.matrix[self.pointer_y][x].state = self.brush_type

        # shape: Vertical Line
        elif self.brush_shape == 7:
            for y in range(min_y, max_y + 1):
                if y >= 0 and y <= self.height - 1:     # Just one check this time.
                    self.matrix[y][self.pointer_x].state = self.brush_type

        # shape: Main diagonal
        elif self.brush_shape == 8:
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    if self.pointer_x - x == self.pointer_y - y:
                        if y >= 0 and y <= self.height - 1:         # These 2 checks are required for all brush shapes,
                            if x >= 0 and x <= self.length - 1:     # Because they are out-of-bound checks.
                                self.matrix[y][x].state = self.brush_type

        # shape: Anti diagonal
        elif self.brush_shape == 9:
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    if (self.pointer_x - x) + (self.pointer_y - y ) == 0:
                        if y >= 0 and y <= self.height - 1:         # These 2 checks are required for all brush shapes,
                            if x >= 0 and x <= self.length - 1:     # Because they are out-of-bound checks.
                                self.matrix[y][x].state = self.brush_type
                                
        # shape: Fill Tool
        elif self.brush_shape == 10:
           handle_achievement("Fill!")
           current = self.matrix[self.pointer_y][self.pointer_x]
           target = self.brush_type
           empty = current.state
           self.flood_fill(target, empty, current)

        if self.brush_type == LAVA:
            handle_achievement("Hell Juice")

    def flood_fill(self, target: int, empty: int, origin: Cell):
        if target == empty:
            return

        limit = self.brush_size
        if limit == 1:
            limit = None
        origin.state = target
        stack = [origin]

        while stack:
            cell = stack.pop()
            neighbours = (self.up(cell),self.down(cell), self.left(cell), self.right(cell))
            for n in neighbours:
                if not n or n.state != empty:
                    continue
                if limit is not None and max(get_dist(n, origin)) > limit:
                    continue

                n.state = target
                stack.append(n)

    def handle_brush_attributes(self, key, shapes):
        global PROFILE
        # Type
        if key == "q":
            self.brush_type = (self.brush_type - 1) % len(PROFILE)
        if key == "e":
            self.brush_type = (self.brush_type + 1) % len(PROFILE)

        # Shape
        if key == "Q":
            self.brush_shape = (self.brush_shape - 1) % len(shapes)
        if key == "E":
            self.brush_shape = (self.brush_shape + 1) % len(shapes)

        # Size
        if key == "-":
            self.brush_size = max(self.min_brush_size, self.brush_size - 1)
        if key == "=":
            self.brush_size = min(self.brush_size + 1, self.max_brush_size)
        if key == "+":
            self.brush_size = self.max_brush_size
        if key == "_":
            self.brush_size = self.min_brush_size

        if self.brush_size == 0:
            self.show_pointer = 0
        else:
            self.show_pointer = 1

        if self.brush_size == self.max_brush_size:
            handle_achievement("Fill?")

    def handle_orientation(self, key):
        if key == "UP":
            self.orientation = "down"
        elif key == "DOWN":
            self.orientation = "up"
        elif key == "LEFT":
            self.orientation = "right"
        elif key == "RIGHT":
            self.orientation = "left"

    def handle_clear(self, key):
        if key == "C":
            self.record_undo()
            self.matrix = [[Cell(row=row, col=col) for col in range(self.length)]
                       for row in range(self.height)]

    def handle_paused(self, key):
        global PAUSED
        if key == "\\":
            PAUSED = not PAUSED
            if PAUSED:
                handle_achievement("Za Wurado!")

        if PAUSED:
            if key == "]":
                self.record_undo()
                self.update()
            elif key == "[" and UNDO_LIST:
                handle_achievement("Shift + Z")
                self.restore_undo()

    def handle_bulbpos(self, key):
        global BULB_POS
        if key == "SHIFTUP":
            BULB_POS[1] -= 1
        elif key == "SHIFTDOWN":
            BULB_POS[1] += 1
        elif key == "SHIFTLEFT":
            BULB_POS[0] -= 1
        elif key == "SHIFTRIGHT":
            BULB_POS[0] += 1
        
    def record_undo(self):
        global UNDO_LIST
        raw = (c.state for row in self.matrix for c in row)
        snapshot = bytes(raw)
        UNDO_LIST.append(snapshot)

    def restore_undo(self):
        global UNDO_LIST
        states = UNDO_LIST.pop()

        i = 0
        for row in self.matrix:
            for c in row:
                c.state = states[i]
                i += 1

    def handle_shuffle(self, key):
        if key != 'tab':
            return
        handle_achievement("Natural landscaping!")
        for x in range(0, self.length):
            for y in range(0, self.height):
                this = self.matrix[y][x]
                other = random.choice(random.choice(self.matrix))
                self.swap(this, other)

    def get_edges(self, top=False, limit=None, cell: Cell = None):
        edges = []
        if limit is None:
            edges.extend(self.matrix[-1])
            if top:
                edges.extend(self.matrix[0])

            for y in range(1, self.height - 1):
                edges.append(self.matrix[y][0])
                edges.append(self.matrix[y][-1])

        else:
            upbound = max(0, cell.row - limit)
            downbound = min(self.length - 1, cell.row + limit)
            leftbound = max(0, cell.col - limit)
            rightbound = min(self.height - 1, cell.col + limit)
            edges.extend(self.matrix[upbound])
            edges.extend(self.matrix[downbound])

            for x in range(leftbound, rightbound + 1):
                edges.append(self.matrix[upbound][x])
                if upbound != downbound:
                    edges.append(self.matrix[downbound][x])

            for y in range(upbound + 1, downbound):
                edges.append(self.matrix[y][leftbound])
                if leftbound != rightbound:
                    edges.append(self.matrix[y][rightbound])

        return edges

    def color_depth_variance(self, cell, hsv: tuple):
        global DYNAMIC_LIGHTING 
        if not DYNAMIC_LIGHTING or cell.state in (FIRE, LAVA):
            return hsv
        
        h, s, v = hsv

        v *= (cell.light_level * 0.01)
        
        return (h, s, max(15 , v))

    def illuminate(self, cell: Cell):
        n: tuple[Cell] = neighbours(cell, self, 7, True, size=5)

        for nearby in neighbours(cell, self, 5, True):
            if nearby.state != LAVA:
                break
        else:
            return

        for current in n:
            kx = current.col - cell.col + 5
            ky = current.row - cell.row + 5

            if 0 <= ky < 11 and 0 <= kx < 11:
                final = self.glow_kernel[ky][kx]

                if final > 0:
                    light = current.light_level + final
                    current.light_level = round(min(100, light))

    def dynamic_lights(self):
        global DYNAMIC_LIGHTING, BULB_POS, PROFILE, FRAMENUM, PERFORMANCE_MODE
        if not DYNAMIC_LIGHTING:
            return
        
        if FRAMENUM%2 and PERFORMANCE_MODE: return

        lights = (FIRE, LAVA, CRYSTAL)

        bulb = BULB_POS
        max_light = 100

        for edge_cell in self.edges: # for every cell that is on the edge,
            prev_light = max_light
            add_hue = None
            ray = line(bulb[0], bulb[1], edge_cell.col, edge_cell.row)
            for ray_dist,current in enumerate(ray): # make a ray from bulb to that specific edge cell and traverse it
                x, y = current

                if not (0 <= x < self.length and 0 <= y < self.height):
                    continue

                current_cell: Cell = self.matrix[y][x]
                t = PROFILE[current_cell.state]["transparency"]
                prev_light -= t

                current_cell.light_level = max(0, round(prev_light))

                if add_hue is not None:
                    current_cell.add_hue = add_hue * prev_light//100
                if current_cell.state == CRYSTAL:
                    add_hue = 240 + 60 * math.sin(FRAMENUM * 0.05 * current_cell.crystal_glow)

        for row in self.matrix:
            for cell in row:
                if cell.state in lights:
                    self.illuminate(cell)

    def display(self, cell: Cell):
        global HUE, PROFILE, FRAMENUM

        symbol: str = None
        hsv: tuple[int] = None

        s = cell.state
        on_pointer = (cell.row == self.pointer_y and cell.col == self.pointer_x)
        symbol = PROFILE[s]["symbol"]
        if on_pointer and self.show_pointer:
            if s in (AIR, FIRE):
                symbol = "⛶"
            elif symbol == "▩":
                symbol = "❖" 
            elif symbol == "■":
                symbol = "◈"
            elif symbol in ("◙", "▣"):
                symbol = "◆"
            elif symbol in ("▢","◌"):
                symbol = "◇"
            elif symbol == "⧆":
                symbol = "⧆"
            elif symbol == "▦":
                symbol = " "
            else:
                symbol = "?"

            hsv = (HUE, 100, 100)

        else:
            # sand, uranium, crystal
            hsv = PROFILE[s]["color"]
            if hsv is None:
                if s == SAND:
                    hsv = (cell.get_sand_hue(self.height, self.length) % 360, 36, 80)
                elif s == URANIUM:
                    hsv = (75, 100, 20 + cell.uraniumdecaystage*5)
                elif s == CRYSTAL:
                    min_hue = 200
                    max_hue = 250
                    center = (min_hue + max_hue) / 2  # 240
                    amplitude = (max_hue - min_hue) / 2  # 60
                    speed = 0.05
                    hue = center + amplitude * math.sin(FRAMENUM * speed * cell.crystal_glow)
                    hsv = (hue, 75, 75)

            if s != AIR:
                hsv = self.color_depth_variance(cell, hsv)

        if cell.add_hue is not None and cell.state not in (LAVA, FIRE, CRYSTAL): # crystal hue addition
            h, s, v = hsv
            new_h = average(h, cell.add_hue)
            final = max(new_h, h)
            hsv = (final, s, v)

        if cell.contaminated and self.show_radiation_lines:
            hsv = (0, 0, 100)

        # if not random.random() < 1/cell.crystal_glow:
        #     hsv = (random.randint(0, 360), random.randint(1, 100), random.randint(1, 100))

        return (symbol, hsv)

    def show(self, extra=[], padding="     ", popup: Popup = None):
        global HUE, FRAMENUM
        self.dynamic_lights()
        span = max_len(extra)+6
        grid = "╔" + ("═"*(2*self.length+1)) + "╗" + padding + "   " + " "*span + "\n"

        for rownum, row in enumerate(self.matrix):
            grid += "║ "
            for element in row:

                symbol, clr = self.display(element)
                grid += color(symbol, clr)
                grid += " "

            if rownum == 0:
                grid += f"║{padding}" + "╭" + "─" * span + "╮\033[K" + "\n"
            elif rownum == len(extra) + 1:
                grid += f"║{padding}" + "╰" + "─" * span + "╯\033[K" + "\n"
            elif extra and rownum != 0 and rownum < len(extra) + 1:
                grid += f"║{padding}│   " + extra[rownum-1] + " " * (span-len(extra[rownum-1])-3) + "│\033[K" + "\n"
            elif rownum == self.height - 3:
                grid += f"║{padding}" + color("╭" + "─" * (len(popup.text)+6) + "╮\033[K", hsv= (50,100,popup.alpha)) + "\n"
            elif rownum == self.height - 2:
                grid += f"║{padding}" + color("│   " + popup.text + "   │", hsv=(50, 100,popup.alpha)) + "\033[K" + "\n"
            elif rownum == self.height - 1:
                grid += f"║{padding}" + color("╰" + "─" * (len(popup.text)+6) + "╯\033[K", hsv= (50, 100,popup.alpha)) + "\n"
            else:
                grid += "║" + " "*2*span + "\n"
        
        reset_terminal_cursor_pos()
        sys.stdout.write(grid)
        sys.stdout.write("╚" + ("═"*(2*self.length+1)) + "╝" + "\n")
        sys.stdout.flush()
        self.reset_radiation_flags()
        self.reset_add_hue()

def line(x0: int, y0: int, x1: int, y1: int, extend: bool = False, grid: Grid = None) -> list[tuple[int, int]]:
    dx = abs(x1 - x0)
    sx = 1 if x0 < x1 else -1
    dy = -abs(y1 - y0)
    sy = 1 if y0 < y1 else -1
    error = dx + dy
    points: list[tuple[int, int]] = []

    while True:
        if extend:
            if grid is None or not (0 <= x0 < grid.length and 0 <= y0 < grid.height): break
        
        points.append((x0, y0))

        if not extend and x0 == x1 and y0 == y1: break
        if dx == dy == 0: break

        e2 = 2 * error
        if e2 >= dy:
            error += dy
            x0 += sx
        if e2 <= dx:
            error += dx
            y0 += sy

    return points

def neighbours(cell: Cell, grid: Grid, method, filter=False, size = None):
    if method == 1: # sides
        n = (grid.left(cell), grid.right(cell))
    elif method == 2: # up-down
        n = (grid.up(cell), grid.down(cell))
    elif method == 3: # all four
        n = (grid.up(cell), grid.down(cell), grid.left(cell), grid.right(cell))
    elif method == 4: # triangle
        d = grid.down(cell)
        n = (grid.up(cell), grid.down(cell), grid.left(cell), grid.right(cell), grid.left(d), grid.right(d))
    elif method == 5: # all 8 with diagonals
        d = grid.down(cell)
        u = grid.up(cell)
        n = (u, d, grid.left(cell), grid.right(cell), grid.left(d), grid.right(d), grid.left(u), grid.right(u))
    elif method == 6: # diagonals only
        d = grid.down(cell)
        u = grid.up(cell)
        n = (grid.left(d), grid.right(d), grid.left(u), grid.right(u))
    elif method == 7: # big range (2-I-2)
        n = []
        for x in range(cell.col - size, cell.col + 1 + size):
            for y in range(cell.row - size, cell.row + 1 + size):
                if y >= 0 and y <= grid.height - 1:
                    if x >= 0 and x <= grid.length - 1:
                        n.append(grid.matrix[y][x])
    else:
        raise ValueError("Method out of bounds.")

    if not filter:
        return tuple(n)
    else:
        return tuple(i for i in n if i)

def get_dist(cell1: Cell, cell2: Cell, direct=False, signed=False) -> tuple[int]:
    if signed:
        xdist = cell1.col - cell2.col
        ydist = cell1.row - cell2.row
    else:
        xdist = abs(cell1.col - cell2.col)
        ydist = abs(cell1.row - cell2.row)
    if direct:
        return xdist + ydist
    return (xdist, ydist)

def max_len(iter: list) -> int:
    maxlen = 0
    for item in iter:
        if len(item) > maxlen:
            maxlen = len(item)
    return maxlen

def average(*args):
    s = 0
    for num in args:
        s += num
    return s / len(args)

def handle_RBS(key):
    global RAINBOW_SAND, RBS_COUNTER
    code = "itchio"

    if key is None:
        return
    key = key.lower()
    
    if key in code:
        if RBS_COUNTER < len(code) and code[RBS_COUNTER] == key:
            RBS_COUNTER += 1
        elif key == code[0]:
            RBS_COUNTER = 1
        else:
            RBS_COUNTER = 0
    else:
        RBS_COUNTER = 0

    if RBS_COUNTER == len(code):
        RAINBOW_SAND = not RAINBOW_SAND
        RBS_COUNTER = 0
        handle_achievement("Eye Candy")

def handle_framerate(key): 
    global FRAMERATE, PAUSED

    if not PAUSED:
        if key == "]":
            FRAMERATE = min(500, FRAMERATE + 1)
        elif key == "[":
            FRAMERATE = max(1, FRAMERATE - 1)
    if FRAMERATE == 1:
        handle_achievement("Precarious Analyst")
    elif FRAMERATE == 500:
        handle_achievement("TRUE HUSSER")

def handle_achievement(ach):
    global MSG, ACHIEVEMENTS, ACH_SFX
    if not ACHIEVEMENTS.get(ach, True):
        ACHIEVEMENTS[ach] = True
        MSG.text = ach
        MSG.display()
        ACH_SFX.play()
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(ACHIEVEMENTS, file, indent=4)

def color(text: str, hsv: tuple = None, rgb: tuple = None):
    '''Provide a string, and a RGB or HSV tuple to add that color to the string. 
    RGB: 0-255 values for R, G & B color channels.
    HSV: hue (0-360), saturation & value (0-100).'''
    if rgb:
        r, g, b = rgb
    else:
        h, s, v = hsv
        r, g, b = hsv_to_rgb((h % 360) / 360, max(0, min(1, s / 100)), max(0, min(1, v / 100)))
        r, g, b = round(r * 255), round(g * 255), round(b * 255)
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def get_keypress():
  '''Silently checks for input.
    Tab: tab
    Enter: enter
    Backspace: backspace
    Delete: del'''
  if sys.platform == 'win32':
    import ctypes
    import msvcrt

    if not msvcrt.kbhit():
      return None

    ch = msvcrt.getch()

    # Handle extended keys / Alt combinations (start with \x00 or \xe0)
    if ch in (b'\x00', b'\xe0'):
      ch2 = msvcrt.getch()
      key_char = ch2.decode('utf-8', errors='ignore')

      # Map standard arrow keys (+ Shift detection via Win32 API)
      arrow_map = {'H': 'UP', 'P': 'DOWN', 'K': 'LEFT', 'M': 'RIGHT'}
      if key_char in arrow_map:
        shift_held = bool(ctypes.windll.user32.GetAsyncKeyState(0x10) & 0x8000)
        prefix = 'SHIFT' if shift_held else ''
        return f'{prefix}{arrow_map[key_char]}'

      # Handle delete key
      if ch2 == b'S':
        return 'del'

      # Map Alt + letter scan codes on Windows (e.g., Alt + x is scan code 45)
      alt_scan_codes = {
          30: 'a',
          48: 'b',
          46: 'c',
          32: 'd',
          18: 'e',
          33: 'f',
          34: 'g',
          35: 'h',
          23: 'i',
          36: 'j',
          37: 'k',
          38: 'l',
          50: 'm',
          49: 'n',
          24: 'o',
          25: 'p',
          16: 'q',
          19: 'r',
          31: 's',
          20: 't',
          22: 'u',
          47: 'v',
          17: 'w',
          45: 'x',
          21: 'y',
          44: 'z',
      }
      code = ord(ch2)
      if code in alt_scan_codes:
        return f'*{alt_scan_codes[code]}'

      return None

    # Handle Enter key
    if ch in (b'\r', b'\n'):
      return 'enter'

    # Handle Tab key
    if ch == b'\t':
      return 'tab'

    # Handle Backspace key
    if ch == b'\x08':
      return 'backspace'
    
    # Handle Ctrl + key (ASCII values 1 to 26 represent Ctrl+A through Ctrl+Z)
    val = ord(ch)
    if 1 <= val <= 26:
      letter = chr(val + 96)
      return f'^{letter}'

    if ch == b"\x1b":
        return "esc"

    decoded = ch.decode('utf-8', errors='ignore')

    return decoded
  
def hide_terminal_cursor():
    sys.stdout.write("\033[?25l")

def show_terminal_cursor():
    sys.stdout.write("\033[?25h")

def wipe_terminal_screen():
    sys.stdout.write("\033[H\033[2J")

def clear_terminal_line():
    sys.stdout.write("\033[2K")

def reset_terminal_cursor_pos():
    sys.stdout.write("\033[H")

def terminal_background():
    sys.stdout.write("\033]11;#000000\007")
    sys.stdout.flush()

# MARK: mains

def menu_loop():
    global ACHIEVEMENTS
    TS = TitleScreen()

    while TS.running:
        TS.tick()
        TS.refresh()
    wipe_terminal_screen()

def game_loop(HUE_CHANGE, gravity_set, pause_set, shapes_set, grid: Grid, timer):
    global HUE, FRAMENUM, PERFORMANCE_MODE, UNDO_LIST, PROFILE, PAUSED, BULB_POS, MSG
    MSG = Popup("")
    while True:
        pressed_key = get_keypress()

        if pressed_key == "esc":
            wipe_terminal_screen()
            ESC_SFX.play()
            break

        Popup.updateall(0.25)

        ticked = False

        if timer.diff() > (1/FRAMERATE):
            if not PAUSED:
                grid.record_undo()
                grid.update()
                timer.reset()
                HUE += HUE_CHANGE
                FRAMENUM += 1
            ticked = True

        grid.handle_pointer(pressed_key)
        grid.handle_action(pressed_key)
        grid.handle_brush_attributes(pressed_key, shapes_set)
        grid.handle_orientation(pressed_key)
        grid.handle_clear(pressed_key)
        grid.handle_paused(pressed_key)
        grid.handle_shuffle(pressed_key)
        grid.handle_bulbpos(pressed_key)

        handle_RBS(pressed_key)
        handle_framerate(pressed_key)

        if ticked or pressed_key is not None:
            grid.show(extra=[   
        f"Pointer: ({grid.pointer_x}, {grid.pointer_y}) [{PROFILE[grid.matrix[grid.pointer_y][grid.pointer_x].state]["name"]}]", 
        f"Brush: <{grid.brush_size}px> ({PROFILE[grid.brush_type]["name"]}) [{shapes_set[grid.brush_shape]}]",
        f"Frame Rate: [{FRAMERATE}]",
        f"Gravity: {gravity_set[grid.orientation]} ",
        f"Simulation: {pause_set[PAUSED]}",
        f"Bulb: {BULB_POS}",
    ], popup=MSG)
        else:
            sleep(0.002)
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(ACHIEVEMENTS, file, indent=4)
    wipe_terminal_screen()

def main():
    global FRAMENUM, FRAMERATE, DYNAMIC_LIGHTING, BULB_POS, \
        PAUSED, UNDO_LIST, MAX_UNDO, MUSIC_VOL, \
        MIN_BRUSH_SIZE, MAX_BRUSH_SIZE, DEFAULT_BRUSH_SIZE, \
        RAINBOW_SAND, HUE, RBS_COUNTER, PROFILE, TYPE_DICT, PERFORMANCE_MODE, \
        ACHIEVEMENTS, ACH_SFX, ACT_SFX, ESC_SFX, MUSIC_VOL, SFX_VOL

    L, B = 30, 30 # length and height of the grid [default: 30x30]

    MIN_BRUSH_SIZE = 0 # [default: 0]
    MAX_BRUSH_SIZE = 10 # [default: 7]
    DEFAULT_BRUSH_SIZE = 1

    FRAMERATE = 60 # decrease if experiencing stutter [default: 60]
    FRAMENUM = 0

    HUE = 0
    HUE_CHANGE = 1

    PAUSED = False

    DYNAMIC_LIGHTING = True # [default: True]
    BULB_POS = [L//2, -5] # the position of the main light source [default: (L//2, -B)]

    RAINBOW_SAND = False
    RBS_COUNTER = 0

    MAX_UNDO = 1000 # the max cap of undo recordings, set this to low if experience performance issues [default: 1000]
    UNDO_LIST = deque(maxlen=MAX_UNDO) 
    PERFORMANCE_MODE = False

    MUSIC_VOL = 0.2 # 0.2
    SFX_VOL = 0.5 # 0.5

    with open("data.json", "r", encoding="utf-8") as file:
        ACHIEVEMENTS = json.load(file)

    PROFILE = {
        AIR : {"name": "Air",
               "symbol": "∙",
               "color": (0, 0, 6),
               "transparency": 0.5,
               "weight": 0},
        SAND : {"name": "Sand",
               "symbol": "▩",
               "color": None,
               "transparency": 7,
               "weight": 2},
        WATER : {"name": "Water",
               "symbol": "■",
               "color": (215, 78, 100),
               "transparency": 4,
               "weight": 1},
        STEEL : {"name": "Steel",
               "symbol": "◙",
               "color": (0, 0, 55),
               "transparency": 7,
               "weight": 0},
        ACID : {"name": "Acid",
               "symbol": "■",
               "color": (128, 100, 100),
               "transparency": 4,
               "weight": 1},
        STEAM : {"name": "Steam",
               "symbol": "◌",
               "color": (80, 2, 40),
               "transparency": 4,
               "weight": 0},
        DRYWOOD : {"name": "Dry Wood",
               "symbol": "▩",
               "color": (28, 51, 46),
               "transparency": 7,
               "weight": 3},
        WETWOOD : {"name": "Wet Wood",
               "symbol": "◙",
               "color": (25, 80, 25),
               "transparency": 7,
               "weight": 0},
        FIRE : {"name": "Fire",
               "symbol": "●",
               "color": (35, 100, 100),
               "transparency": 0,
               "weight": 0},
        LAVA : {"name": "Lava",
               "symbol": "■",
               "color": (17, 100, 100),
               "transparency": 0,
               "weight": 3},
        OBSIDIAN : {"name": "Obsidian",
               "symbol": "◙",
               "color": (250, 70, 70),
               "transparency": 7,
               "weight": 0},
        URANIUM : {"name": "Uranium",
               "symbol": "▩",
               "color": None,
               "transparency": 7,
               "weight": 7},
        GUNPOWDER : {"name": "Gunpowder",
               "symbol": "▩",
               "color": (5, 0 , 5),
               "transparency": 7,
               "weight": 2},
        FUSE : {"name": "Fuse",
               "symbol": "◙",
               "color": (55, 80, 20),
               "transparency": 7,
               "weight": 0},
        CRYSTAL : {"name": "Crystal",
               "symbol": "◙",
               "color": None,
               "transparency": -1,
               "weight": 0},
        GLASS : {"name": "Glass",
               "symbol": "▢",
               "color": (0, 0, 80),
               "transparency": 0,
               "weight": 0},
        GRAPHITE : {"name": "Graphite",
               "symbol": "◙",
               "color": (200, 65, 45),
               "transparency": 30,
               "weight": 0},
        ICE : {"name": "Ice",
               "symbol": "◙",
               "color": (200, 80, 100),
               "transparency": 4,
               "weight": 0},
        OIL : {"name": "Oil",
               "symbol": "■",
               "color": (230, 80, 20),
               "transparency": 6,
               "weight": 2},
        FUMES : {"name": "Fumes",
               "symbol": "◌",
               "color": (60, 100, 50),
               "transparency": 4,
               "weight": 0},
        MORPH : {"name": "Morph",
               "symbol": "⧆",
               "color": (300, 100, 100),
               "transparency": 0,
               "weight": 0},
        PUMP : {"name": "Pump",
               "symbol": "▣",
               "color": (350, 80, 70),
               "transparency": 6,
               "weight": 0},
        VOID : {"name": "Void",
               "symbol": "▦",
               "color": (270, 60, 30),
               "transparency": 100,
               "weight": 0}
    }

    gravity_set = {"up": "↧", "down": "↥", "left": "↦", "right": "↤"}
    pause_set = {False: "Running", True: "Paused"}
    shapes_set = {0: "Solid Square", 1: "Hollow Square", 2: "Solid Circle", 3: "Hollow Circle", 4: "Solid Diamond", 5: "Hollow Diamond", 6: "Horizontal Line", 7: "Vertical Line", 8: "Primary Diagonal", 9: "Secondary Diagonal", 10: "Fill Tool"}
    TYPE_DICT = {
                "∙": "air",
                "▩": "powder",
                "■": "liquid",
                "◙": "solid",
                "●": "fire",
                "▢": "glass",
                PROFILE[STEAM]["symbol"]: "gas",
                "⧆": "cloner",
                "▣": "pump",
                "▦": "void"
            }

    wipe_terminal_screen()
    hide_terminal_cursor()
    clear_terminal_line()
    terminal_background()
    grid : Grid = Grid(L,B)

    timer = Timer()

    mixer.init()
    mixer.music.load("sounds/music/Kowloon.mp3")
    ACH_SFX = mixer.Sound("sounds/sfx/achievement.wav")
    ACH_SFX.set_volume(SFX_VOL)
    ACT_SFX = mixer.Sound("sounds/sfx/enter.wav")
    ACT_SFX.set_volume(SFX_VOL)
    ESC_SFX = mixer.Sound("sounds/sfx/esc.wav")
    ESC_SFX.set_volume(SFX_VOL + 0.3)
    mixer.music.set_volume(MUSIC_VOL)
    mixer.music.play(-1)

    # setting up the terminal
    pyautogui.hotkey("f11")
    pyautogui.hotkey("ctrl","-")
    pyautogui.hotkey("ctrl","-")

    # main loops
    while True:
        menu_loop()
        game_loop(HUE_CHANGE, gravity_set, pause_set, shapes_set, grid, timer)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        show_terminal_cursor()
    finally:
        show_terminal_cursor()
    mixer.quit()
    pyautogui.hotkey("ctrl","0")
    pyautogui.hotkey("f11")
# master
