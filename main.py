import time
import sys

L, B = 10, 10

class Cell:

    def __init__(self, row, col, state=0):
        self.state = state
        self.row = row
        self.col = col

class Grid:
    
    def __init__(self, length, height):
        self.length = length
        self.height = height
        self.matrix = [[Cell(row=row, col=col) for col in range(length)]
                       for row in range(height)]

    def set_state(self, cell_x, cell_y, value):
        self.matrix[cell_y][cell_x].state = value

    def update(self):
        new_matrix = [[Cell(row=row, col=col) for col in range(self.length)]
                    for row in range(self.height)]

        for row in self.matrix:
            for current_cell in row:
                if current_cell.state == 0:
                    continue

                down = current_cell.row + 1
                left = current_cell.col - 1
                right = current_cell.col + 1

                if down > self.height - 1:
                    new_matrix[current_cell.row][current_cell.col].state = 1
                    continue

                can_right = right <= self.length - 1
                can_left = left >= 0

                if self.matrix[down][current_cell.col].state == new_matrix[down][current_cell.col].state == 0:
                    new_matrix[down][current_cell.col].state = 1
                elif can_right and self.matrix[down][right].state == new_matrix[down][right].state == 0:
                    new_matrix[down][right].state = 1
                elif can_left and self.matrix[down][left].state == new_matrix[down][left].state == 0:
                    new_matrix[down][left].state = 1
                else:
                    new_matrix[current_cell.row][current_cell.col].state = 1

        self.matrix = new_matrix

    def show(self, extra=0):
        grid = ""
        for row in self.matrix:
            for element in row:
                if element.state == 0:
                    grid += "∙"
                elif element.state == 1:
                    grid += "▩"
                elif element.state == 2:
                    grid += "▢"
                grid += " "
            grid += "\n"
        print("\033[2J\033[H", end="", flush=True)
        print(grid, end="", flush=True)
        print("_ "*self.length, flush=True)
        if extra:
            print(extra)

def place_grains():
    ... # work on this

def main():
    # grains = place_grains()

    grid = Grid(L,B)
    # for i, j in grains:
    #     grid.set_state(i,j,1)
    grid.set_state(5,0,1)
    grid.set_state(4,0,1)
    grid.set_state(6,0,1)
    grid.set_state(3,1,1)
    grid.set_state(7,1,1)
    grid.set_state(0,3,1)
    grid.set_state(0,4,1)
    grid.set_state(0,5,1)
    grid.set_state(0,6,1)

    while True:
        grid.update()
        grid.show()

        time.sleep(0.1)



if __name__ == "__main__":
    main()