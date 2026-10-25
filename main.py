import sys
import random
from time import sleep
from colorsys import hsv_to_rgb
import math


class Cell:

    def __init__(self, row, col, state=0, sand_color=None):
        self.state = state
        self.row = row
        self.col = col
        self.update = True
        if sand_color is None:
            self.sand_color = random.randint(-10, 20)
        else:
            self.sand_color = sand_color

    def get_sand_hue(self, height, length):
        global RAINBOW_SAND, HUE
        theta = math.radians(HUE)
        if not RAINBOW_SAND:
            return 38
        else:
            avg = average(math.sin(theta)*(self.row / height), math.cos(theta)*(self.col / length))
            return (avg * 360 ) + HUE 

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

        self.orientation = "up"

        self.matrix = [[Cell(row=row, col=col) for col in range(length)]
                       for row in range(height)]

    def swap(self, cell1: Cell, cell2: Cell):
        cell1.state, cell2.state = cell2.state, cell1.state
        cell1.sand_color, cell2.sand_color = cell2.sand_color, cell1.sand_color

    def reset_update_flags(self):
        for x in range(0, self.length):
            for y in range(0, self.height):
                self.matrix[y][x].update = True

    def up(self, cell, n: int = 1, static = False):
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
            return False

    def down(self, cell, n: int = 1, static = False):
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
            return False

    def left(self, cell, n: int = 1, static = False):
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
            return False

    def right(self, cell, n: int = 1, static = False):
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
            return False

    def update(self):
        if self.orientation == "up":
            matrixrange = (range(0, self.length), range(self.height-1, -1, -1))
        elif self.orientation == "down":
            matrixrange = (range(0, self.length), range(0, self.height))
        elif self.orientation == "left":
            matrixrange = (range(self.length-1 , -1, -1), range(0, self.height))
        elif self.orientation == "right":
            matrixrange = (range(0, self.length), range(0, self.height))

        for x in matrixrange[0]:
            for y in matrixrange[1]:

                cell = self.matrix[y][x] 

                if cell.state == 1:
                    self.handle_sand(cell)
                elif cell.state == 2:
                    self.handle_water(cell)
                elif cell.state == 4:
                    self.handle_acid(cell)
                elif cell.state == 5:
                    self.handle_steam(cell)

                # sleep(1)

    def handle_sand(self, cell: Cell):
        if random.randint(0,1):
            first = self.left(cell=cell)
            second = self.right(cell=cell)
        else:
            first = self.right(cell=cell)
            second = self.left(cell=cell)

        # for normal gravity 
        if self.down(cell=cell) and self.down(cell=cell).state == 0:
            self.swap(cell, self.down(cell=cell))
        elif cell.update and self.down(cell=cell) and first and self.down(cell=first).state == 0:
            self.swap(cell, self.down(cell=first))
            self.down(cell=first).update = False
        elif cell.update and self.down(cell=cell) and second and self.down(cell=second).state == 0:
            self.swap(cell, self.down(cell=second))
            self.down(cell=second).update = False

        # for swapping with water (density swap)
        elif self.down(cell=cell) and self.down(cell=cell).state == 2:
            self.swap(cell, self.down(cell=cell))
        elif cell.update and self.down(cell=cell) and first and self.down(cell=first).state == 2:
            self.swap(cell, self.down(cell=first))
            self.down(cell=first).update = False
        elif cell.update and self.down(cell=cell) and second and self.down(cell=second).state == 2:
            self.swap(cell, self.down(cell=second))
            self.down(cell=second).update = False

    def handle_water(self, cell):
        if random.randint(0,1):
            first = self.left(cell=cell)
            second = self.right(cell=cell)
        else:
            first = self.right(cell=cell)
            second = self.left(cell=cell)

        # for normal gravity 
        if self.down(cell=cell) and self.down(cell=cell).state == 0:
            self.swap(cell, self.down(cell=cell))
            self.down(cell=cell).update = False # potentially breaking
        elif cell.update and first and first.state == 0:
            self.swap(cell, first)
            first.update = False
        elif cell.update and second and second.state == 0:
            self.swap(cell, second)
            second.update = False

        # plan to add better behaviour:
        # find to which side, left or right, does more empty cells exist
        # then move to that side

    def handle_acid(self, cell):
        if random.randint(0,1):
            first = self.left(cell=cell)
            second = self.right(cell=cell)
        else:
            first = self.right(cell=cell)
            second = self.left(cell=cell)

        # for acid dissoulution
            # for sand
        if self.down(cell) and self.down(cell).state == 1:
            cell.state = 0
            self.down(cell).state = 0
        elif self.up(cell) and self.up(cell).state == 1:
            cell.state = 0
            self.up(cell).state = 0
        elif first and first.state == 1:
            cell.state = 0
            first.state = 0
        elif second and second.state == 1:
            cell.state = 0
            second.state = 0
            # for water
        elif self.down(cell) and self.down(cell).state == 2:
            cell.state = 0
            self.down(cell).state = 5
        elif self.up(cell) and self.up(cell).state == 2:
            cell.state = 0
            self.up(cell).state = 5
        elif first and first.state == 2:
            cell.state = 0
            first.state = 5
        elif second and second.state == 2:
            cell.state = 0
            second.state = 5

        # for normal gravity 
        if self.down(cell=cell) and self.down(cell=cell).state == 0:
            self.swap(cell, self.down(cell=cell))
            self.down(cell=cell).update = False # potentially breaking
        elif cell.update and first and first.state == 0:
            self.swap(cell, first)
            first.update = False
        elif cell.update and second and second.state == 0:
            self.swap(cell, second)
            second.update = False

    def handle_steam(self, cell):
        if random.randint(0,1):
            first = self.left(cell=cell)
            second = self.right(cell=cell)
        else:
            first = self.right(cell=cell)
            second = self.left(cell=cell)

        # condensation
        if (self.up(cell) is None) or (self.up(cell) and self.up(cell).state == 3):
            if random.random() < 0.01:
                cell.state = 2
                return

        # normal gravity
        if self.up(cell=cell) and cell.update and self.up(cell=cell).state in (0, 1, 2, 4):
            self.swap(cell, self.up(cell=cell))
            self.up(cell=cell).update = False # potentially breaking
        elif cell.update and self.up(cell=cell) and first and self.up(cell=first).state in (0, 1, 2, 4):
            self.swap(cell, self.up(cell=first))
            self.up(cell=first).update = False
        elif cell.update and self.up(cell=cell) and second and self.up(cell=second).state in (0, 1, 2, 4):
            self.swap(cell, self.up(cell=second))
            self.up(cell=second).update = False
        elif cell.update and first and first.state == 0:
            self.swap(cell, first)
            first.update = False
        elif cell.update and second and second.state == 0:
            self.swap(cell, second)
            second.update = False

    def handle_pointer(self, key):
        if key == "w":
            self.pointer_y = (self.pointer_y - 1) % self.height
        if key == "s":
            self.pointer_y = (self.pointer_y + 1) % self.height
        if key == "a":
            self.pointer_x = (self.pointer_x - 1) % self.length
        if key == "d":
            self.pointer_x = (self.pointer_x + 1) % self.length

        # to add: pointer jumping

    def handle_action(self, key):
        brush_size = self.brush_size - 1
        if key != " " or brush_size < 0:
            return

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
            raise NotImplementedError

    def handle_brush_attributes(self, key, elements, shapes):
        # Type
        if key == "q":
            self.brush_type = (self.brush_type - 1) % len(elements)
        if key == "e":
            self.brush_type = (self.brush_type + 1) % len(elements)

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
            self.matrix = [[Cell(row=row, col=col) for col in range(self.length)]
                       for row in range(self.height)]

    def handle_paused(self, key):
        global PAUSED
        if key == "\\":
            PAUSED = not PAUSED

        if PAUSED:
            if key == "]":
                self.record_undo()
                self.update()
            elif key == "[" and UNDO_LIST:
                self.matrix = UNDO_LIST.pop()
                if not PAUSED and UNDO_LIST:
                    self.matrix = UNDO_LIST.pop()

    def record_undo(self):
        global UNDO_LIST, MAX_UNDO
        snapshot = [[Cell(row=c.row, col=c.col, state=c.state, sand_color=c.sand_color) for c in row]for row in self.matrix]
        UNDO_LIST.append(snapshot)
        if len(UNDO_LIST) > MAX_UNDO:
            UNDO_LIST.pop(0)

    def color_depth_variance(self, cell, hsv: tuple):
        global DYNAMIC_LIGHTING 
        if not DYNAMIC_LIGHTING:
            return hsv
        
        h, s, v = hsv

        for i in range(1, 16):
            if self.up(cell, i, True):

                if self.up(cell, i, True).state in (2, 4):
                    v -= 5
                elif self.up(cell, i, True).state in (1, 3):
                    v -= 7

        return (h, s, max(20 , v))
    
    def show(self, extra=0):
        global HUE
        grid = ""

        for rownum, row in enumerate(self.matrix):
            for element in row:

                on_pointer = (element.row == self.pointer_y and element.col == self.pointer_x)
                if on_pointer and self.show_pointer:
                    if element.state == 0:
                        grid += color("⊹", hsv=(HUE, 100, 100))
                        # grid += "◌"⊹
                    elif element.state in (1, 5):
                        grid += color("◇", hsv=(HUE, 100, 100))
                        # grid += "○"◇
                    elif element.state in (2, 4):
                        grid += color("◈", hsv=(HUE, 100, 100))
                        # grid += "●"◈
                    elif element.state == 3:
                        grid += color("◆", hsv=(HUE, 100, 100))
                        # grid += "◉"◆
                else:
                    if element.state == 0:
                        grid += color("∙", rgb=(15, 15, 15))
                        # grid += "∙"
                    elif element.state == 1:
                        grid += color("▩", hsv=self.color_depth_variance(element, (element.get_sand_hue(self.height, self.length), 36, 80 + element.sand_color)))
                        # grid += "▩"
                    elif element.state == 2:
                        grid += color("■", hsv=self.color_depth_variance(element, (215, 78, 100)))
                        # grid += "■"
                    elif element.state == 3:
                        grid += color("◙", hsv=self.color_depth_variance(element, (0, 0, 54)))
                        # grid += "◙"
                    elif element.state == 4:
                        grid += color("■", hsv=self.color_depth_variance(element, (80, 100, 100)))
                        # grid += "■"
                    elif element.state == 5:
                        grid += color("▩", hsv=self.color_depth_variance(element, (80, 2, 40 + 1.5*(element.sand_color))))
                        # grid += "▩"
                grid += " "
            if extra and rownum != 0 and rownum < len(extra) + 1:
                grid += "               │   " + extra[rownum-1]
            grid += "\n"
        sys.stdout.write("\033[H")
        sys.stdout.write(grid)
        sys.stdout.write("═"*2*self.length + "\n")
        sys.stdout.flush()


def average(*args):
    s = 0
    for num in args:
        s += num
    return s / len(args)

def handle_RBS(key):
    global RAINBOW_SAND, RBS_COUNTER
    code = "689689689"

    if key is None:
        return
    
    if key in code:
        if code[RBS_COUNTER] == key:
            RBS_COUNTER += 1
        else:
            RBS_COUNTER = 0
    else:
        RBS_COUNTER = 0

    if RBS_COUNTER == len(code):
        RAINBOW_SAND = not RAINBOW_SAND
        RBS_COUNTER = 0

def handle_framerate(key): 
    global FRAMERATE, PAUSED

    if not PAUSED:
        if key == "]":
            FRAMERATE = min(100, FRAMERATE + 1)
        elif key == "[":
            FRAMERATE = max(1, FRAMERATE - 1)

def color(str: str, hsv: tuple = None, rgb: tuple = None):
    '''Provide a str, and a RGB or HSV tuple to add that color to the str. 
    RGB: 0-255 values for R, G & B color channels.
    HSV: hue (0-360), saturation & value (0-100).'''
    if rgb:
        r, g, b = rgb
    else:
        h, s, v = hsv
        r, g, b = hsv_to_rgb(h/360, s/100, v/100)
        r = round(r*255)
        g = round(g*255)
        b = round(b*255)
    return f"\033[38;2;{r};{g};{b}m{str}\033[0m"

def get_keypress():
    '''Silently checks for input.
    Tab: tab
    Caps Lock: caps lock
    Enter: enter
    Ctrl: ^
    Alt: *'''
    if sys.platform == "win32":
        import msvcrt
        if not msvcrt.kbhit():
            return None         
        
        ch = msvcrt.getch()
        
        # Handle extended keys / Alt combinations (start with \x00 or \xe0)
        if ch in (b'\x00', b'\xe0'):
            ch2 = msvcrt.getch()
            
            # Map standard arrow keys
            arrow_map = {'H': 'UP', 'P': 'DOWN', 'K': 'LEFT', 'M': 'RIGHT'}
            if ch2.decode('utf-8', errors='ignore') in arrow_map:
                return arrow_map.get(ch2.decode('utf-8', errors='ignore'))
            
            # Map Alt + letter scan codes on Windows (e.g., Alt + x is scan code 45)
            alt_scan_codes = {
                30: 'a', 48: 'b', 46: 'c', 32: 'd', 18: 'e', 33: 'f', 34: 'g', 
                35: 'h', 23: 'i', 36: 'j', 37: 'k', 38: 'l', 50: 'm', 49: 'n', 
                24: 'o', 25: 'p', 16: 'q', 19: 'r', 31: 's', 20: 't', 22: 'u', 
                47: 'v', 17: 'w', 45: 'x', 21: 'y', 44: 'z'
            }
            code = ord(ch2)
            if code in alt_scan_codes:
                return f"*{alt_scan_codes[code]}"
            
            return None

        # Handle Enter key
        if ch in (b'\r', b'\n'):
            return 'enter'
        
        # Handle Tab key
        if ch == b'\t':
            return 'tab'

        # Handle Ctrl + key (ASCII values 1 to 26 represent Ctrl+A through Ctrl+Z)
        val = ord(ch)
        if 1 <= val <= 26:
            letter = chr(val + 96)
            return f"^{letter}"

        decoded = ch.decode('utf-8', errors='ignore')
        
        return decoded

def main():
    global FRAMENUM, FRAMERATE, DYNAMIC_LIGHTING, \
        PAUSED, UNDO_LIST, MAX_UNDO, \
        MIN_BRUSH_SIZE, MAX_BRUSH_SIZE, DEFAULT_BRUSH_SIZE, \
        RAINBOW_SAND, HUE, RBS_COUNTER

    L, B = 30, 30 # length and height of the grid [default: 30x30]
    FRAMERATE = 50 # decrease if experiencing stutter [default: 50]
    MIN_BRUSH_SIZE = 0 # [default: 0]
    MAX_BRUSH_SIZE = 7 # [default: 7]
    DEFAULT_BRUSH_SIZE = 1
    HUE = 0
    FRAMENUM = 0
    HUE_CHANGE = 1
    DYNAMIC_LIGHTING = True # [default: True]
    PAUSED = False
    RAINBOW_SAND = False
    RBS_COUNTER = 0
    MAX_UNDO = 1000 # the max cap of undo recordings, set this to low if experience performance issues [default: 1000]
    UNDO_LIST = [Grid(L, B).matrix] * MAX_UNDO

    last_key = None # debug

    elements = {0: "Air", 1: "Sand", 2: "Water", 3: "Steel", 4: "Acid", 5: "Steam"}
    gravity_set = {"up": "↧", "down": "↥", "left": "↦", "right": "↤"}
    pause_set = {False: "▢", True: "▶"}
    shapes_set = {0: "Solid Square", 1: "Hollow Square", 2: "Solid Circle", 3: "Hollow Circle", 4: "Solid Diamond", 5: "Hollow Diamond", 6: "Horizontal Line", 7: "Vertical Line", 8: "Primary Diagonal", 9: "Secondary Diagonal", 10: "Fill Tool"}

    sys.stdout.write("\033[H\033[2J")
    sys.stdout.write("\033[?25l")
    sys.stdout.write("\033[2K")
    grid = Grid(L,B)
    grid.show(extra=[   
    f"Pointer: ({grid.pointer_x}, {grid.pointer_y}) [{elements[grid.matrix[grid.pointer_y][grid.pointer_x].state]}]",
    f"Brush: <{grid.brush_size}px> ({elements[grid.brush_type]}) [{shapes_set[grid.brush_shape]}]                        ", 
    f"Frame Rate: [{(FRAMERATE):.0f}]",
    f"Gravity: [ {gravity_set[grid.orientation]} ]",
    f"Simulation: ( {pause_set[PAUSED]} )"
])

    # main loop 
    while True:
        pressed_key = get_keypress()

        if not PAUSED:
            grid.update()
            grid.record_undo()
        grid.reset_update_flags()
        grid.handle_pointer(pressed_key)
        grid.handle_action(pressed_key)
        grid.handle_brush_attributes(pressed_key, elements, shapes_set)
        grid.handle_orientation(pressed_key)
        grid.handle_clear(pressed_key)
        grid.handle_paused(pressed_key)

        handle_RBS(pressed_key)
        handle_framerate(pressed_key)

        if grid.brush_size == 0:
            grid.show_pointer = 0
        else:
            grid.show_pointer = 1

        if pressed_key == "`":
            HUE_CHANGE = 1 - HUE_CHANGE

        if pressed_key is None: # debug -
            pass
        else:
            last_key = pressed_key # - debug

        grid.show(extra=[   
    f"Pointer: ({grid.pointer_x}, {grid.pointer_y}) [{elements[grid.matrix[grid.pointer_y][grid.pointer_x].state]}]   ",
    f"Brush: <{grid.brush_size}px> ({elements[grid.brush_type]}) [{shapes_set[grid.brush_shape]}]                   ",
    f"Frame Rate: [{FRAMERATE}]   ",
    f"Gravity: [ {gravity_set[grid.orientation]} ]   ",
    f"Simulation: ( {pause_set[PAUSED]} )   ", f"DEBUG: {last_key}               "
])

        HUE += HUE_CHANGE
        FRAMENUM += 1
        sleep(1/FRAMERATE)


if __name__ == "__main__":
    main()
    sys.stdout.write("\033[?25h")
# master