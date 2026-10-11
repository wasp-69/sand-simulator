import sys
import random
from time import sleep
from colorsys import hsv_to_rgb

class Cell:

    def __init__(self, row, col, state=0):
        self.state = state
        self.row = row
        self.col = col
        self.update = True
        self.sand_color = random.randint(-10, 20)

class Grid:
    
    def __init__(self, length, height, min_brush_size=-1, max_brush_size=5, default_brush_size=1):
        self.length = length
        self.height = height
        self.show_pointer = 1
        self.pointer_x = 0
        self.pointer_y = 0
        self.min_brush_size = min_brush_size
        self.max_brush_size = max_brush_size
        self.brush_size = default_brush_size
        self.brush_type = 1
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

    def up(self, cell, n: int = 1):
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

    def down(self, cell, n: int = 1):
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

    def left(self, cell, n: int = 1):
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

    def right(self, cell, n: int = 1):
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

                cell = self.matrix[y][x] # scans left to right, bottom to top

                if cell.state == 1:
                    self.handle_sand(cell)
                elif cell.state == 2:
                    self.handle_water(cell)
                
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
            
    def handle_pointer(self, key):
        if key == "w":
            self.pointer_y = (self.pointer_y - 1) % self.height
        if key == "s":
            self.pointer_y = (self.pointer_y + 1) % self.height
        if key == "a":
            self.pointer_x = (self.pointer_x - 1) % self.length
        if key == "d":
            self.pointer_x = (self.pointer_x + 1) % self.length

    def handle_action(self, key):
        new_brush_size = self.brush_size - 1
        if key == " ":
            if new_brush_size < 0:
                return
            for x in range(self.pointer_x - new_brush_size, self.pointer_x + new_brush_size+1):
                for y in range(self.pointer_y - new_brush_size, self.pointer_y + new_brush_size+1):
                    if y >= 0 and y <= self.height - 1:
                        if x >= 0 and x <= self.length - 1:
                            self.matrix[y][x].state = self.brush_type

    def handle_brush_size(self, key):
        if key == "-":
            self.brush_size = max(self.min_brush_size, self.brush_size - 1)
        if key == "=":
            self.brush_size = min(self.brush_size + 1, self.max_brush_size)

    def handle_brush_type(self, key, elements):
        if key == "q":
            self.brush_type = (self.brush_type - 1) % len(elements)
        if key == "e":
            self.brush_type = (self.brush_type + 1) % len(elements)

    def handle_orientation(self, key):
        if key == "UP":
            self.orientation = "down"
        elif key == "DOWN":
            self.orientation = "up"
        elif key == "LEFT":
            self.orientation = "right"
        elif key == "RIGHT":
            self.orientation = "left"
    
    def show(self, hue, extra=0):
        grid = ""

        for row in self.matrix:
            for element in row:

                on_pointer = (element.row == self.pointer_y and element.col == self.pointer_x)
                if on_pointer and self.show_pointer:
                    if element.state == 0:
                        grid += color("◌", hsv=(hue, 100, 100))
                        # grid += "◌"
                    elif element.state == 1:
                        grid += color("○", hsv=(hue, 100, 100))
                        # grid += "○"
                    elif element.state == 2:
                        grid += color("●", hsv=(hue, 100, 100))
                        # grid += "●"
                    elif element.state == 3:
                        grid += color("◉", hsv=(hue, 100, 100))
                        # grid += "◉"
                else:
                    if element.state == 0:
                        grid += color("∙", rgb=(10, 10, 10))
                        # grid += "∙"
                    elif element.state == 1:
                        grid += color("▩", hsv=(38, 36, 80 + element.sand_color))
                        # grid += "▩"
                    elif element.state == 2:
                        grid += color("■", rgb=(52, 128, 235))
                        # grid += "■"
                    elif element.state == 3:
                        grid += color("◙", rgb=(66, 35, 10))
                        # grid += "◙"
                grid += " "
            grid += "\n"
        print("\033[2J\033[H", end="", flush=True)
        print(grid, end="", flush=True)
        print("= "*self.length, flush=True)
        if extra:
            print(extra, flush=True)


def handle_framerate(key, framerate): 
    if key == ".":
        return min(100, framerate + 1)
    elif key == ",":
        return max(1, framerate - 1)
    else:
        return framerate

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
    if sys.platform == "win32":
        import msvcrt
        if not msvcrt.kbhit():
            return None          
        ch = msvcrt.getch()
        if ch in (b'\x00', b'\xe0'):
            ch2 = msvcrt.getch()
            return {'H': 'UP', 'P': 'DOWN', 'K': 'LEFT', 'M': 'RIGHT'}.get(
                ch2.decode('utf-8', errors='ignore'))
        return ch.decode('utf-8', errors='ignore')

def main():

    L, B = 30, 30 # length and height of the grid [default: 30x30]
    FRAMERATE = 50 # decrease if experiencing stutter [default: 50]
    MIN_BRUSH_SIZE = 0
    MAX_BRUSH_SIZE = 5
    DEFAULT_BRUSH_SIZE = 1
    HUE = 0
    FRAMENUM = 0
    HUE_CHANGE = 1

    elements = {0: "Air", 1: "Sand", 2: "Water", 3: "Sandstone"}
    gravity_set = {"up": "↧", "down": "↥", "left": "↦", "right": "↤"}

    grid = Grid(L,B, max_brush_size=MAX_BRUSH_SIZE, min_brush_size=MIN_BRUSH_SIZE, default_brush_size=DEFAULT_BRUSH_SIZE)
    grid.show(hue=HUE, extra=f"""Pointer: ({grid.pointer_x}, {grid.pointer_y}) [{elements[grid.matrix[grid.pointer_y][grid.pointer_x].state]}] 
Brush: <{grid.brush_size}px> [{elements[grid.brush_type]}] 
Frame Rate: [{(FRAMERATE):.0f}]""")


    while True:
        pressed_key = get_keypress()

        grid.update()
        grid.reset_update_flags()
        grid.handle_pointer(pressed_key)
        grid.handle_action(pressed_key)
        grid.handle_brush_size(pressed_key)
        grid.handle_brush_type(pressed_key, elements)
        grid.handle_orientation(pressed_key)

        FRAMERATE = handle_framerate(pressed_key, FRAMERATE)

        if grid.brush_size == 0:
            grid.show_pointer = 0
        else:
            grid.show_pointer = 1

        if pressed_key == "`":
            HUE_CHANGE = 1 - HUE_CHANGE

        grid.show(hue=HUE, extra=f"""Pointer: ({grid.pointer_x}, {grid.pointer_y}) [{elements[grid.matrix[grid.pointer_y][grid.pointer_x].state]}] 
Brush: <{grid.brush_size}px> [{elements[grid.brush_type]}] 
Frame Rate: [{FRAMERATE}]
Gravity: [ {gravity_set[grid.orientation]} ]""")
        HUE += HUE_CHANGE
        FRAMENUM += 1
        sleep(1/FRAMERATE)


if __name__ == "__main__":
    main()
# master
