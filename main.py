import time

class Cell:

    def __init__(self, state=0):
        self.state = state

    def update(self, x_pos, y_pos, grid):
        if self.state == 0:
            return
        
        if y_pos < grid.height - 1 and grid.matrix[y_pos+1][x_pos].state == 0: # down movement logic
            grid.matrix[y_pos][x_pos].state = 0
            grid.matrix[y_pos+1][x_pos].state = 1
        else:

            if x_pos > 0 and y_pos < grid.height - 1 and grid.matrix[y_pos+1][x_pos-1].state == 0: # diagonal left movement logic
                grid.matrix[y_pos][x_pos].state = 0
                grid.matrix[y_pos+1][x_pos-1].state = 1
            elif x_pos < grid.length - 1 and y_pos < grid.height - 1 and grid.matrix[y_pos+1][x_pos+1].state == 0: # diagonal right movement logic
                grid.matrix[y_pos][x_pos].state = 0
                grid.matrix[y_pos+1][x_pos+1].state = 1
            else:

                if x_pos > 0 and y_pos < grid.height - 1 and grid.matrix[y_pos][x_pos-1].state == 0: # left movement logic
                    grid.matrix[y_pos][x_pos].state = 0
                    grid.matrix[y_pos][x_pos-1].state = 1
                elif x_pos < grid.length - 1 and grid.matrix[y_pos][x_pos+1].state == 0: # right movement logic
                    grid.matrix[y_pos][x_pos].state = 0
                    grid.matrix[y_pos][x_pos+1].state = 1



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
                grid += "▩" if element.state else "∙"
                grid += " "
            grid += "\n"
        print("\033[2J\033[H", end="", flush=True)
        print(grid, end="", flush=True)
        print("_ "*self.length, flush=True)



def main():
    grid = Grid(10,10)
    grid.show()
    grid.set_state(5,0,1)
    grid.set_state(4,0,1)
    grid.set_state(6,0,1)
    grid.set_state(3,1,1)
    grid.set_state(7,1,1)

    while True:
        for x_pos in range(grid.length -1, -1, -1):
            for y_pos in range(grid.height - 1, -1, -1):
                grid.matrix[y_pos][x_pos].update(x_pos, y_pos, grid)

        grid.show()

        time.sleep(0.2)

if __name__ == "__main__":
    main()

