import time
import sys
import random

L, B = 30, 30 # length and height of the grid
tickrate = 0.02 # increase if experiencing stutter

class Cell:

    def __init__(self, row, col, state=0):
        self.state = state
        self.row = row
        self.col = col

    def toggle_state(self):
        self.state = 1 - self.state

class Grid:
    
    def __init__(self, length, height):
        self.length = length
        self.height = height
        self.show_pointer = 1
        self.pointer_x = 0
        self.pointer_y = 0
        self.brush_size = 0
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

                if down > self.height - 1:
                    new_matrix[current_cell.row][current_cell.col].state = 1
                    continue

                can_right = right <= self.length - bias and right >= 0
                can_left = left <= self.length + bias and left >= 0

                if self.matrix[down][current_cell.col].state == new_matrix[down][current_cell.col].state == 0:
                    new_matrix[down][current_cell.col].state = 1
                    change += 1
                elif can_right and self.matrix[down][right].state == new_matrix[down][right].state == 0:
                    new_matrix[down][right].state = 1
                    change += 1
                elif can_left and self.matrix[down][left].state == new_matrix[down][left].state == 0:
                    new_matrix[down][left].state = 1
                    change += 1
                else:
                    new_matrix[current_cell.row][current_cell.col].state = 1

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
        if key == " ":
            if self.brush_size == 0:
                self.matrix[self.pointer_y][self.pointer_x].toggle_state()
            else:
                for x in range(self.pointer_x - self.brush_size, self.pointer_x + self.brush_size+1):
                    for y in range(self.pointer_y - self.brush_size, self.pointer_y + self.brush_size+1):
                        if y >= 0 and y <= self.height - 1:
                            if x >= 0 and x <= self.length - 1:
                                self.matrix[y][x].toggle_state()
                return 1
        return 0

    def handle_brush_size(self, key):
        if key == "-":
            self.brush_size = max(-1, self.brush_size - 1)
            return 1
        if key == "=":
            self.brush_size = min(self.brush_size + 1, 4)
            return 1
        return 0

    def show(self, extra=0):
        grid = ""
        for row in self.matrix:
            for element in row:
                on_pointer = (element.row == self.pointer_y and element.col == self.pointer_x)
                if on_pointer and self.show_pointer:
                    if element.state == 0:
                        grid += "\033[38;2;214;180;252m○\033[0m"
                        # grid += "○"
                    elif element.state == 1:
                        grid += "\033[38;2;214;180;252m●"
                        # grid += "●"
                else:
                    if element.state == 0:
                        grid += "\033[38;5;242m∙\033[0m"
                        # grid += "∙"
                    elif element.state == 1:
                        grid += "\033[38;2;224;195;144m▩\033[0m"
                        # grid += "▩"
                grid += " "
            grid += "\n"
        print("\033[2J\033[H", end="", flush=True)
        print(grid, end="", flush=True)
        print("= "*self.length, flush=True)
        if extra:
            print(extra)


def get_key():
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
    elements = {0: "Air", 1: "Sand", 2: "Water", 3: "Sandstone"}

    grid = Grid(L,B)
    grid.show(extra=f"Pointer: ({grid.pointer_x}, {grid.pointer_y}) [{elements[grid.matrix[grid.pointer_y][grid.pointer_x].state]}] \nBrush Size: {grid.brush_size+1}")

    while True:
        pressed_key = get_key()

        update_count = 0

        update_count += grid.update()
        update_count += grid.handle_pointer(pressed_key)
        update_count += grid.handle_action(pressed_key)
        update_count += grid.handle_brush_size(pressed_key)
        if grid.brush_size == -1:
            grid.show_pointer = False
        else:
            grid.show_pointer = True
        if update_count > 0:
            grid.show(extra=f"Pointer: ({grid.pointer_x}, {grid.pointer_y}) [{elements[grid.matrix[grid.pointer_y][grid.pointer_x].state]}] \nBrush Size: {grid.brush_size+1}")

        time.sleep(tickrate)

if __name__ == "__main__":
    main()

# sandstone: ◙
# sandstone pointer: ◉
# water: ■
# water pointer: ◒
