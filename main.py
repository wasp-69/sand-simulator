import time

class Cell:

    def __init__(self, state=0):
        self.state = state

    def update(self, x_pos, y_pos, grid):
        if self.state == 0 or y_pos >= grid.height + 1:
            return
        
        if grid.matrix[y_pos+1][x_pos].state == 0:
            grid.matrix[y_pos][x_pos].state = 0
            grid.matrix[y_pos+1][x_pos].state = 1



class Grid:
    
    def __init__(self, length, height):
        self.length = length
        self.height = height
        self.matrix = [[Cell() for _ in range(length)]
                       for _ in range(height)]

    def set_state(self, cell_x, cell_y, value):
        self.matrix[cell_y][cell_x].state = value

    def show(self):
        grid = ""
        for row in self.matrix:
            for element in row:
                grid += str(element.state)
                grid += " "
            grid += "\n"
        print("\033[2J\033[H", end="", flush=True)
        print(grid, end="", flush=True)
        print("_ "*self.length, flush=True)



def main():
    grid = Grid(10,10)
    grid.show()
    grid.set_state(5,0,1)

    while True:
        for y_pos, row in enumerate(grid.matrix.reverse()):
            for x_pos, element in enumerate(row.reverse()):
                element.update(x_pos, y_pos, grid)

        grid.show()

        time.sleep(1)

if __name__ == "__main__":
    main()

