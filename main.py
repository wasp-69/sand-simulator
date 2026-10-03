import sys
import random
from time import sleep
from dataclasses import dataclass

class Cell:

    def __init__(self, row, col, state=0):
        self.state = state
        self.row = row
        self.col = col
        self.update = True

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
        self.matrix = [[Cell(row=row, col=col) for col in range(length)]
                       for row in range(height)]

    def set_state(self, cell_x, cell_y, value):
        self.matrix[cell_y][cell_x].state = value

    def reset_update_flags(self):
        for x in range(0, self.length):
            for y in range(0, self.height):
                self.matrix[y][x].update = True
    
    def update(self):
        for x in range(0, self.length):
            for y in range(self.height-1, -1, -1):

                cell = self.matrix[y][x] # scans left to right, bottom to top
                up = y - 1
                down = y + 1
                left = x - 1
                right = x + 1
                can_up = 0 <= up < self.height
                can_down = 0 <= down < self.height
                can_left = 0 <= left < self.length
                can_right = 0 <= right < self.length
                if random.choice([0,1]):
                    first_side = left
                    first_check = can_left
                    second_side = right
                    second_check = can_right
                else:
                    first_side = right
                    first_check = can_right
                    second_side = left
                    second_check = can_left

                # this makes things order specific which can be bad but it's the most convenient way
                dirs = (up, down, left, right, first_side, second_side)
                checks = (can_up, can_down, can_left, can_right, first_check, second_check)

                self.handle_sand(x, y, cell, dirs, checks)
                self.handle_water(x, y, cell, dirs, checks)
                
                # sleep(1)

    def handle_sand(self, x, y, cell, dirs, checks):
        up, down, left, right, first_side, second_side = dirs
        can_up, can_down, can_left, can_right, first_check, second_check = checks
        if cell.state == 1:

            # for normal gravity 
            if can_down and self.matrix[down][x].state == 0:
                self.matrix[y][x].state = 0
                self.matrix[down][x].state = 1
            elif cell.update and can_down and first_check and self.matrix[down][first_side].state == 0:
                self.matrix[y][x].state = 0
                self.matrix[down][first_side].state = 1
                self.matrix[down][first_side].update = False
            elif cell.update and can_down and second_check and self.matrix[down][second_side].state == 0:
                self.matrix[y][x].state = 0
                self.matrix[down][second_side].state = 1
                self.matrix[down][second_side].update = False

            # for swapping with water (density swap)
            elif can_down and self.matrix[down][x].state == 2:
                self.matrix[y][x].state = 2
                self.matrix[down][x].state = 1
            elif cell.update and can_down and first_check and self.matrix[down][first_side].state == 2:
                self.matrix[y][x].state = 2
                self.matrix[down][first_side].state = 1
                self.matrix[down][first_side].update = False
            elif cell.update and can_down and second_check and self.matrix[down][second_side].state == 2:
                self.matrix[y][x].state = 2
                self.matrix[down][second_side].state = 1
                self.matrix[down][second_side].update = False

    def handle_water(self, x, y, cell, dirs, checks):
        up, down, left, right, first_side, second_side = dirs
        can_up, can_down, can_left, can_right, first_check, second_check = checks
        if cell.state == 2:

            # for normal gravity 
            if can_down and self.matrix[down][x].state == 0:
                self.matrix[y][x].state = 0
                self.matrix[down][x].state = 2
            elif cell.update and first_check and self.matrix[y][first_side].state == 0:
                self.matrix[y][x].state = 0
                self.matrix[y][first_side].state = 2
                self.matrix[y][first_side].update = False
            elif cell.update and second_check and self.matrix[y][second_side].state == 0:
                self.matrix[y][x].state = 0
                self.matrix[y][second_side].state = 2
                self.matrix[y][second_side].update = False

            # plan to add better behaviour:
            # find to which side, left or right, does more empty cells exist
            # then move to that side
            
    def handle_pointer(self, key):
        if key == "UP":
            self.pointer_y = (self.pointer_y - 1) % self.height
        if key == "DOWN":
            self.pointer_y = (self.pointer_y + 1) % self.height
        if key == "LEFT":
            self.pointer_x = (self.pointer_x - 1) % self.length
        if key == "RIGHT":
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
    
    def show(self, extra=0):
        grid = ""
        for row in self.matrix:
            for element in row:
                on_pointer = (element.row == self.pointer_y and element.col == self.pointer_x)
                if on_pointer and self.show_pointer:
                    if element.state == 0:
                        grid += color("◌", (214, 180, 252))
                        # grid += "◌"
                    elif element.state == 1:
                        grid += color("○", (214, 180, 252))
                        # grid += "○"
                    elif element.state == 2:
                        grid += color("●", (214, 180, 252))
                        # grid += "●"
                    elif element.state == 3:
                        grid += color("◉", (214, 180, 252))
                        # grid += "◉"
                else:
                    if element.state == 0:
                        grid += color("∙", (10, 10, 10))
                        # grid += "∙"
                    elif element.state == 1:
                        grid += color("▩", (224, 195, 144))
                        # grid += "▩"
                    elif element.state == 2:
                        grid += color("■", (52, 128, 235))
                        # grid += "■"
                    elif element.state == 3:
                        grid += color("◙", (66, 35, 10))
                        # grid += "◙"
                grid += " "
            grid += "\n"
        print("\033[2J\033[H", end="", flush=True)
        print(grid, end="", flush=True)
        print("= "*self.length, flush=True)
        if extra:
            print(extra)


def handle_tickrate(key, tickrate):
    if key == ",":
        return min(2, tickrate + 0.01)
    elif key == ".":
        return max(0.01, tickrate - 0.01)
    else:
        return tickrate

def color(str: str, rgb: tuple):
    r, g, b = rgb
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

    L, B = 20, 20 # length and height of the grid [default: 20x20]
    TICKRATE = 0.02 # increase if experiencing stutter [default: 0.02]
    MIN_BRUSH_SIZE = 0
    MAX_BRUSH_SIZE = 5
    DEFAULT_BRUSH_SIZE = 1

    elements = {0: "Air", 1: "Sand", 2: "Water", 3: "Sandstone"}

    grid = Grid(L,B, max_brush_size=MAX_BRUSH_SIZE, min_brush_size=MIN_BRUSH_SIZE, default_brush_size=DEFAULT_BRUSH_SIZE)
    grid.show(extra=f"Pointer: ({grid.pointer_x}, {grid.pointer_y}) [{elements[grid.matrix[grid.pointer_y][grid.pointer_x].state]}] \nBrush: <{grid.brush_size}px> [{elements[grid.brush_type]}] \nFrame Rate: [{(1/TICKRATE):.0f}]")


    while True:
        pressed_key = get_keypress()

        grid.update()
        grid.reset_update_flags()
        grid.handle_pointer(pressed_key)
        grid.handle_action(pressed_key)
        grid.handle_brush_size(pressed_key)
        grid.handle_brush_type(pressed_key, elements)

        TICKRATE = handle_tickrate(pressed_key, TICKRATE)

        if grid.brush_size == 0:
            grid.show_pointer = False
        else:
            grid.show_pointer = True

        grid.show(extra=f"Pointer: ({grid.pointer_x}, {grid.pointer_y}) [{elements[grid.matrix[grid.pointer_y][grid.pointer_x].state]}] \nBrush: <{grid.brush_size}px> [{elements[grid.brush_type]}] \nFrame Rate: [{(1/TICKRATE):.0f}]")

        sleep(TICKRATE)


if __name__ == "__main__":
    main()
# chore/rework-update-logic