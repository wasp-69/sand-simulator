import time
import sys
import random

class Cell:

    def __init__(self, row, col, state=0):
        self.state = state
        self.row = row
        self.col = col

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

    def update(self):
        new_matrix = [[Cell(row=row, col=col) for col in range(self.length)]
                    for row in range(self.height)]

        change = 0

        for row in self.matrix:
            for current_cell in row:
                if current_cell.state == 0:
                    continue
                
                bias = random.choice([1,-1])
                
                down = current_cell.row + 1
                left = current_cell.col - bias
                right = current_cell.col + bias

                can_right = right <= self.length - bias and right >= 0
                can_left = left <= self.length + bias and left >= 0
                can_down = down < self.height

                if current_cell.state == 1: # if the current cell is sand
                    if can_down and self.matrix[down][current_cell.col].state == new_matrix[down][current_cell.col].state == 0:
                        new_matrix[down][current_cell.col].state = 1
                        change += 1
                    elif can_down and can_right and self.matrix[down][right].state == new_matrix[down][right].state == 0:
                        new_matrix[down][right].state = 1
                        change += 1
                    elif can_down and can_left and self.matrix[down][left].state == new_matrix[down][left].state == 0:
                        new_matrix[down][left].state = 1
                        change += 1
                    else:
                        new_matrix[current_cell.row][current_cell.col].state = 1

                elif current_cell.state == 2: # if the current cell is water
                    if can_down and self.matrix[down][current_cell.col].state == new_matrix[down][current_cell.col].state == 0:
                        new_matrix[down][current_cell.col].state = 2
                        change += 1
                    elif can_right and self.matrix[current_cell.row][right].state == new_matrix[current_cell.row][right].state == 0:
                        new_matrix[current_cell.row][right].state = 2
                        change += 1
                    elif can_left and self.matrix[current_cell.row][left].state == new_matrix[current_cell.row][left].state == 0:
                        new_matrix[current_cell.row][left].state = 2
                        change += 1

                    elif current_cell.row > 0 and self.matrix[current_cell.row - 1][current_cell.col].state == 1:
                        new_matrix[current_cell.row - 1][current_cell.col].state = 2
                        new_matrix[current_cell.row][current_cell.col].state = 1
                        change += 1

                    # >>> add diagonal sand swaps

                    else:
                        new_matrix[current_cell.row][current_cell.col].state = 2

        self.matrix = new_matrix
        return change


    def handle_pointer(self, key):
        change = 0
        if key == "UP":
            self.pointer_y = (self.pointer_y - 1) % self.height
            change += 1
        if key == "DOWN":
            self.pointer_y = (self.pointer_y + 1) % self.height
            change += 1
        if key == "LEFT":
            self.pointer_x = (self.pointer_x - 1) % self.length
            change += 1
        if key == "RIGHT":
            self.pointer_x = (self.pointer_x + 1) % self.length
            change += 1
        return change

    def handle_action(self, key):
        new_brush_size = self.brush_size - 1
        if key == " ":
            if new_brush_size == 0:
                self.matrix[self.pointer_y][self.pointer_x].state = self.brush_type
            else:
                for x in range(self.pointer_x - new_brush_size, self.pointer_x + new_brush_size+1):
                    for y in range(self.pointer_y - new_brush_size, self.pointer_y + new_brush_size+1):
                        if y >= 0 and y <= self.height - 1:
                            if x >= 0 and x <= self.length - 1:
                                self.matrix[y][x].state = self.brush_type
                return 1
        return 0

    def handle_brush_size(self, key):
        change = 0
        if key == "-":
            self.brush_size = max(self.min_brush_size, self.brush_size - 1)
            change += 1
        if key == "=":
            self.brush_size = min(self.brush_size + 1, self.max_brush_size)
            change += 1
        return change

    def handle_brush_type(self, key, elements):
        change = 0
        if key == "q":
            self.brush_type = (self.brush_type - 1) % len(elements)
            change += 1
        if key == "e":
            self.brush_type = (self.brush_type + 1) % len(elements)
            change += 1
        return change
    
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
                grid += " "
            grid += "\n"
        print("\033[2J\033[H", end="", flush=True)
        print(grid, end="", flush=True)
        print("= "*self.length, flush=True)
        if extra:
            print(extra)


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

    L, B = 20, 20 # length and height of the grid
    TICKRATE = 0.02 # increase if experiencing stutter
    MIN_BRUSH_SIZE = 0
    MAX_BRUSH_SIZE = 5
    DEFAULT_BRUSH_SIZE = 1

    elements = {0: "Air", 1: "Sand", 2: "Water", 3: "Sandstone"}

    grid = Grid(L,B, max_brush_size=MAX_BRUSH_SIZE, min_brush_size=MIN_BRUSH_SIZE, default_brush_size=DEFAULT_BRUSH_SIZE)
    grid.show(extra=f"Pointer: ({grid.pointer_x}, {grid.pointer_y}) [{elements[grid.matrix[grid.pointer_y][grid.pointer_x].state]}] \nBrush Size: <{grid.brush_size}> [{elements[grid.brush_type]}]")


    while True:
        pressed_key = get_keypress()

        update_count = 0

        update_count += grid.update()
        update_count += grid.handle_pointer(pressed_key)
        update_count += grid.handle_action(pressed_key)
        update_count += grid.handle_brush_size(pressed_key)
        update_count += grid.handle_brush_type(pressed_key, elements)

        if grid.brush_size == 0:
            grid.show_pointer = False
        else:
            grid.show_pointer = True

        if update_count > 0:
            grid.show(extra=f"Pointer: ({grid.pointer_x}, {grid.pointer_y}) [{elements[grid.matrix[grid.pointer_y][grid.pointer_x].state]}] \nBrush Size: <{grid.brush_size}> [{elements[grid.brush_type]}]")

        time.sleep(TICKRATE)


if __name__ == "__main__":
    main()
# chore/rework-update-logic
# aaaah software breaking change here aaaah