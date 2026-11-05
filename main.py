import sys
import random
from time import sleep, perf_counter
from colorsys import hsv_to_rgb
import math
from collections import deque

AIR, SAND, WATER, STEEL, ACID, STEAM, DRYWOOD, WETWOOD, FIRE, LAVA, OBSIDIAN, GUNPOWDER, FUSE, URANIUM = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13

class Timer:

    def __init__(self):
        self.starting_time = perf_counter()
        self.current_time = perf_counter()

    def reset(self):
        self.starting_time = perf_counter()

    def diff(self):
        self.current_time = perf_counter()
        return self.current_time - self.starting_time

class Cell:

    def __init__(self, row, col, state=AIR):
        self.state = state
        self.row = row
        self.col = col
        self.update = True
        self.uraniumdecaystage = 0
        self.contaminated = False
        self.light_level = 100

    def get_sand_hue(self, height, length):
        global RAINBOW_SAND, HUE
        theta = math.radians(HUE)
        if not RAINBOW_SAND:
            return 38
        else:
            avg = average(math.sin(theta)*(self.row / height), math.cos(theta)*(self.col / length))
            return (avg * 360 ) + HUE 

    def is_static(self):
        return self.state in (STEEL, WETWOOD, OBSIDIAN, FUSE)

    def is_edge(self, ignore_top = True):
        if ignore_top:
            return (self.col == 0 or self.col == 30 or self.row == 30)
        else:
            return (self.col == 0 or self.col == 30 or self.row == 30 or self.row == 0)

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
        self.edges = self.get_edges()                                      # except the top one
        self.bounds = self.get_edges(True)

    def swap(self, cell1: Cell, cell2: Cell):
        cell1.state, cell2.state = cell2.state, cell1.state
        cell1.uraniumdecaystage, cell2.uraniumdecaystage = cell2.uraniumdecaystage, cell1.uraniumdecaystage

    def reset_update_flags(self):
        for x in range(0, self.length):
            for y in range(0, self.height):
                self.matrix[y][x].update = True

    def reset_radiation_flags(self):
        for x in range(0, self.length):
            for y in range(0, self.height):
                self.matrix[y][x].contaminated = False

    def reset_light_levels(self):
        for x in range(0, self.length):
            for y in range(0, self.height):
                self.matrix[y][x].light_level = 30

    def up(self, cell, n: int = 1, static = False):
        if not cell:
            return False
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
        if not cell:
            return False
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
        if not cell:
            return False
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
        if not cell:
            return False
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
        self.reset_update_flags()
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
        elif self.down(cell) and self.down(cell).state == WATER:
            self.swap(cell, self.down(cell))
        elif cell.update and self.down(cell) and first and self.down(first).state == WATER:
            self.swap(cell, self.down(first))
            self.down(first).update = False
        elif cell.update and self.down(cell) and second and self.down(second).state == WATER:
            self.swap(cell, self.down(second))
            self.down(second).update = False

    def handle_water(self, cell):
        if random.randint(0,1):
            first = self.left(cell)
            second = self.right(cell)
        else:
            first = self.right(cell)
            second = self.left(cell)

        # for normal gravity 
        if self.down(cell) and self.down(cell).state == AIR:
            self.swap(cell, self.down(cell))
            self.down(cell).update = False # potentially breaking
        elif cell.update and first and first.state == AIR:
            self.swap(cell, first)
            first.update = False
        elif cell.update and second and second.state == AIR:
            self.swap(cell, second)
            second.update = False

        # plan to add better behaviour:
        # find to which side, left or right, does more empty cells exist
        # then move to that side

    def handle_acid(self, cell):
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
                return
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
                    

        # for normal gravity 
        if self.down(cell) and self.down(cell).state == AIR:
            self.swap(cell, self.down(cell))
            self.down(cell).update = False # potentially breaking
        elif cell.update and first and first.state == AIR:
            self.swap(cell, first)
            first.update = False
        elif cell.update and second and second.state == AIR:
            self.swap(cell, second)
            second.update = False

    def handle_steam(self, cell: Cell):
        if random.randint(0,1):
            first = self.left(cell)
            second = self.right(cell)
        else:
            first = self.right(cell)
            second = self.left(cell)

        # condensation
        if (self.up(cell) is None) or (self.up(cell).is_static()):
            if random.random() < 0.01:
                cell.state = WATER
                return

        # normal gravity
        if self.up(cell) and cell.update and self.up(cell).state in (AIR, SAND, WATER, ACID, FIRE, GUNPOWDER, URANIUM):
            self.swap(cell, self.up(cell))
            self.up(cell).update = False # potentially breaking
        elif cell.update and self.up(cell) and first and self.up(first).state in (AIR, SAND, WATER, ACID, FIRE, GUNPOWDER, URANIUM):
            self.swap(cell, self.up(first))
            self.up(first).update = False
        elif cell.update and self.up(cell) and second and self.up(second).state in (AIR, SAND, WATER, ACID, FIRE, GUNPOWDER, URANIUM):
            self.swap(cell, self.up(second))
            self.up(second).update = False
        elif cell.update and first and first.state == AIR:
            self.swap(cell, first)
            first.update = False
        elif cell.update and second and second.state == AIR:
            self.swap(cell, second)
            second.update = False

    def handle_drywood(self, cell):
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
        not_flammables = (AIR, WATER, STEEL, SAND, ACID, STEAM, FIRE, LAVA, OBSIDIAN, URANIUM)

        if all(cell.state in not_flammables for cell in n): # fire is surrounded by non-flammable materials
            if random.random() < 0.2:
                cell.state = AIR
                return
            if self.up(cell) and cell.update and self.up(cell).state == AIR:
                self.swap(cell, self.up(cell))
                self.up(cell).update = False

        for current in n: # else,
            if current.state == WATER:
                cell.state = STEAM
                current.state = AIR
            elif current.state in (FUSE, GUNPOWDER) and cell.update:
                current.state = FIRE
                current.update = False
            elif random.random() < 0.01: 
                if current.state == DRYWOOD and cell.update:
                    current.state = FIRE
                    current.update = False
                if current.state == WETWOOD and cell.update:
                    current.state = DRYWOOD
                    cell.state = STEAM
                    current.update = False

    def handle_lava(self, cell):
        global FRAMENUM

        if FRAMENUM%3 == 0:
            if random.random() < 0.05:
                above = self.up(cell)
                if above and above.state == AIR:
                    above.state = FIRE
            n: tuple[Cell] = neighbours(cell, self, 3, True)

            for nearby in n:
                if nearby.state == SAND:
                    nearby.state = AIR
                elif nearby.state == WATER:
                    nearby.state = AIR
                    cell.state = OBSIDIAN
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
            below = self.down(cell)
            if below and below.state == FIRE:
                self.swap(cell, below)
            self.handle_water(cell)

    def handle_obsidian(self, cell):
        w = 0
        for i in range(1, min(16, cell.row + 1)):
            above_cell = self.up(cell, i)
            if not above_cell:
                break
            above = above_cell.state
            if above in (AIR, OBSIDIAN, FIRE, STEAM, STEEL, WETWOOD, FUSE):
                break
            elif above in (SAND, GUNPOWDER):
                w += 2
            elif above == WATER:
                w += 1
            elif above == ACID:
                w += 1
            elif above == DRYWOOD:
                w += 3
            elif above == LAVA:
                w += 3

        if w > 20:
            cell.state = AIR

    def handle_gunpowder(self, cell):
        n: tuple[Cell] = neighbours(cell, self, 5, True)

        for nearby in n:
            if nearby.state == WATER:
                cell.state = DRYWOOD
                nearby.state = AIR
                return
            elif nearby.state == LAVA:
                cell.state = FIRE
                return
        self.handle_sand(cell)
        
    def handle_fuse(self, cell):
        n: tuple[Cell] = neighbours(cell, self, 5, True)

        for nearby in n:
            if nearby.state == WATER:
                cell.state = DRYWOOD
                nearby.state = AIR
            elif nearby.state == LAVA:
                cell.state = FIRE

    def handle_uranium(self, cell: Cell):
        if cell.uraniumdecaystage > 11: # death by over-decay
            cell.state = AIR
            return

        if random.random() < 0.01 + (cell.uraniumdecaystage / 200): # random chance to SHOOT radiation ray

            depth = random.randint(0, min(self.length-1, self.height-1))
            if random.random() < 0.5:
                coords = (random.choice([0, self.length-1]), depth)
            else:
                coords = (depth, random.choice([0, self.height-1]))

            for ray in DDA_line(cell.col, cell.row, coords[0], coords[1]): # traversing that ray for cells
                hit_cell = self.matrix[ray[1]][ray[0]]
                dist = get_dist(cell, hit_cell, True)
                hit_cell.contaminated = True

                if hit_cell.state == OBSIDIAN: # sheilding effect of obsidian
                    break

                if random.random() < 0.2 / (1 + dist / 10): # random chance to have a reaction happen
                    if hit_cell.state == WATER:
                        hit_cell.state = ACID
                        cell.uraniumdecaystage += 1
                    elif hit_cell.state == STEEL:
                        hit_cell.state = SAND
                        cell.uraniumdecaystage += 1
                    elif hit_cell.state == DRYWOOD:
                        hit_cell.state = FIRE
                        cell.uraniumdecaystage += 1
                    elif hit_cell.state == SAND and random.random() < 0.3:
                        hit_cell.state = AIR
                        cell.uraniumdecaystage += 1
                    elif hit_cell.state in (GUNPOWDER, FUSE):
                        hit_cell.state = FIRE
                        cell.uraniumdecaystage += 1
                    # elif

        self.handle_sand(cell)


    def handle_pointer(self, key):
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
           current = self.matrix[self.pointer_y][self.pointer_x]
           target = self.brush_type
           empty = current.state
           self.flood_fill(target, empty, current)

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
                self.restore_undo()

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
        for x in range(0, self.length):
            for y in range(0, self.height):
                this = self.matrix[y][x]
                other = random.choice(random.choice(self.matrix))
                self.swap(this, other)

    def get_edges(self, top=False):
        edges = []


        edges.extend(self.matrix[-1])
        if top:
            edges.extend(self.matrix[0])

        for y in range(1, self.height - 1):
            edges.append(self.matrix[y][0])
            edges.append(self.matrix[y][-1])

        return edges

    def color_depth_variance(self, cell, hsv: tuple): # TO REWORK ENTIRELY
        global DYNAMIC_LIGHTING 
        if not DYNAMIC_LIGHTING or cell.state in (FIRE, LAVA):
            return hsv
        
        h, s, v = hsv

        v *= (cell.light_level * 0.01)
        
        return (h, s, max(15 , v))

    def DO_NOT_shoot_a_light_ray_in_all_directions_and_illuminate_the_cells_that_it_hits(self, cell):
        n: tuple[Cell] = neighbours(cell, self, 7, True)
        for current in n:
            current.light_level += (10 - get_dist(cell, current, True))//1.3

    def dynamic_lights(self):
        global DYNAMIC_LIGHTING, BULB_POS
        if not DYNAMIC_LIGHTING:
            return

        solids = [SAND, STEEL, DRYWOOD, WETWOOD, OBSIDIAN, GUNPOWDER, FUSE, URANIUM]
        fluids = [WATER, ACID, STEAM]
        lights = [FIRE, LAVA]

        bulb = BULB_POS
        max_light = 100

        for edge_cell in self.edges: # for every cell that is on the edge,
            prev_light = max_light
            for current in DDA_line(bulb[0], bulb[1], edge_cell.col, edge_cell.row): # make a ray from bulb to that specific edge cell and traverse it
                x, y = current

                if not (0 <= x < self.length and 0 <= y < self.height):
                    continue

                current_cell = self.matrix[y][x]

                if current_cell.state in solids:
                    prev_light -= 7
                elif current_cell.state in fluids:
                    prev_light -= 4
                elif current_cell.state == AIR:
                    prev_light -= 0.5
                elif current_cell.state in lights and current_cell.light_level < 90:
                    self.DO_NOT_shoot_a_light_ray_in_all_directions_and_illuminate_the_cells_that_it_hits(current_cell)

                current_cell.light_level = max(0, prev_light)           
    
    def display(self, cell: Cell):
        global HUE

        symbol: str = None
        hsv: tuple[int] = None

        s = cell.state
        on_pointer = (cell.row == self.pointer_y and cell.col == self.pointer_x)
        if on_pointer and self.show_pointer:
            if s in (AIR, FIRE):
                symbol = "⊹"
            elif s in (SAND, STEAM, DRYWOOD, GUNPOWDER, URANIUM):
                symbol = "◇"
            elif s in (WATER, ACID, LAVA):
                symbol = "◈"
            elif s in (STEEL, WETWOOD, OBSIDIAN, FUSE):
                symbol = "◆"
            else:
                symbol = "?"

            hsv = (HUE, 100, 100)

        else:
            if s == AIR:
                symbol = "∙"
                hsv = (0, 0, 6)
            elif s in (SAND, STEAM, DRYWOOD, GUNPOWDER, URANIUM):
                symbol = "▩"
                if s == SAND:
                    hsv = (cell.get_sand_hue(self.height, self.length) % 360, 36, 80)
                elif s == STEAM:
                    hsv = (80, 2, 40)
                elif s == DRYWOOD:
                    hsv = (28, 51, 46)
                elif s == GUNPOWDER:
                    hsv = (5, 0 , 5)
                elif s == URANIUM:
                    hsv = (75, 100, 20 + cell.uraniumdecaystage*5)
            elif s in (WATER, ACID, LAVA):
                symbol = "■"
                if s == WATER:
                    hsv = (215, 78, 100)
                elif s == ACID:
                    hsv = (128, 100, 100)
                elif s == LAVA:
                    hsv = (17, 100, 100)
            elif s in (STEEL, WETWOOD, OBSIDIAN, FUSE):
                symbol = "◙"
                if s == STEEL:
                    hsv = (0, 0, 55)
                elif s == WETWOOD:
                    hsv = (25, 80, 25)
                elif s == OBSIDIAN:
                    hsv = (250, 70, 70)
                elif s == FUSE:
                    hsv = (55, 80, 20)
            elif s == FIRE:
                symbol = "●"
                hsv = (35, 100, 100)

            if s != AIR:
                hsv = self.color_depth_variance(cell, hsv)
        if cell.contaminated and self.show_radiation_lines:
            hsv = (0, 0, 100)
        return (symbol, hsv)
                
    def show(self, extra=0):
        global HUE
        self.dynamic_lights()
        grid = "╔" + ("═"*(2*self.length+1)) + "╗" + "\n"
        span = max_len(extra)+6
        padding = "     "

        for rownum, row in enumerate(self.matrix):
            grid += "║ "
            for element in row:

                symbol, clr = self.display(element)
                grid += color(symbol, clr)
                grid += " "

            if rownum == 0:
                grid += f"║{padding}" + "╭" + "─" * span + "╮          " + "\n"
            elif rownum == len(extra) + 1:
                grid += f"║{padding}" + "╰" + "─" * span + "╯          " + "\n"
            elif extra and rownum != 0 and rownum < len(extra) + 1:
                grid += f"║{padding}│   " + extra[rownum-1] + " " * (span-len(extra[rownum-1])-3) + "│          "
                grid += "\n"
            else:
                grid += "║\n"
        reset_terminal_cursor_pos()
        sys.stdout.write(grid)
        sys.stdout.write("╚" + ("═"*(2*self.length+1)) + "╝")
        sys.stdout.write("\n")
        sys.stdout.flush()
        self.reset_radiation_flags()

def DDA_line(x1, y1, x2, y2) -> list[tuple[int]]:
    x = x1
    y = y1

    points = [(x, y)]

    dx = x2 - x1
    dy = y2 - y1

    steps = max( abs(dx), abs(dy) )

    for _ in range(steps):
        x += dx/steps
        y += dy/steps
        points.append((round(x), round(y)))

    return points

def neighbours(cell: Cell, grid: Grid, method, filter=False):
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
        for x in range(cell.col - 5, cell.col + 6):
            for y in range(cell.row - 5, cell.row + 6):
                try:
                    n.append(grid.matrix[y][x])
                except IndexError:
                    continue
    else:
        raise ValueError("Method out of bounds.")

    if not filter:
        return tuple(n)
    else:
        return tuple(i for i in n if i)

def get_dist(cell1: Cell, cell2: Cell, direct=False) -> tuple[int]:
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
            FRAMERATE = min(500, FRAMERATE + 1)
        elif key == "[":
            FRAMERATE = max(1, FRAMERATE - 1)

def color(str: str, hsv: tuple = None, rgb: tuple = None):
    '''Provide a string, and a RGB or HSV tuple to add that color to the string. 
    RGB: 0-255 values for R, G & B color channels.
    HSV: hue (0-360), saturation & value (0-100).'''
    if rgb:
        r, g, b = rgb
    else:
        h, s, v = hsv
        r, g, b = hsv_to_rgb((h % 360) / 360, max(0, min(1, s / 100)), max(0, min(1, v / 100)))
        r, g, b = round(r * 255), round(g * 255), round(b * 255)
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

def main():
    global FRAMENUM, FRAMERATE, DYNAMIC_LIGHTING, BULB_POS, \
        PAUSED, UNDO_LIST, MAX_UNDO, \
        MIN_BRUSH_SIZE, MAX_BRUSH_SIZE, DEFAULT_BRUSH_SIZE, \
        RAINBOW_SAND, HUE, RBS_COUNTER

    L, B = 30, 30 # length and height of the grid [default: 30x30]

    MIN_BRUSH_SIZE = 0 # [default: 0]
    MAX_BRUSH_SIZE = 7 # [default: 7]
    DEFAULT_BRUSH_SIZE = 1

    FRAMERATE = 60 # decrease if experiencing stutter [default: 60]
    FRAMENUM = 0

    HUE = 0
    HUE_CHANGE = 1

    PAUSED = False

    DYNAMIC_LIGHTING = True # [default: True]
    BULB_POS = (L//2, -B)

    RAINBOW_SAND = False
    RBS_COUNTER = 0

    MAX_UNDO = 1000 # the max cap of undo recordings, set this to low if experience performance issues [default: 1000]
    UNDO_LIST = deque(maxlen=MAX_UNDO) 

    elements = {0: "Air", 1: "Sand", 2: "Water", 3: "Steel", 4: "Acid", 5: "Steam", 6: "Dry Wood", 7: "Wet Wood", 8: "Fire", 9: "Lava", 10: "Obsidian", 11: "Gunpowder", 12: "Fuse", 13: "Uranium"}
    gravity_set = {"up": "↧", "down": "↥", "left": "↦", "right": "↤"}
    pause_set = {False: "▢", True: "▶"}
    shapes_set = {0: "Solid Square", 1: "Hollow Square", 2: "Solid Circle", 3: "Hollow Circle", 4: "Solid Diamond", 5: "Hollow Diamond", 6: "Horizontal Line", 7: "Vertical Line", 8: "Primary Diagonal", 9: "Secondary Diagonal", 10: "Fill Tool"}

    wipe_terminal_screen()
    hide_terminal_cursor()
    clear_terminal_line()
    grid = Grid(L,B)
    grid.show(extra=[   
    f"Pointer: ({grid.pointer_x}, {grid.pointer_y}) [{elements[grid.matrix[grid.pointer_y][grid.pointer_x].state]}]",
    f"Brush: <{grid.brush_size}px> ({elements[grid.brush_type]}) [{shapes_set[grid.brush_shape]}]", 
    f"Frame Rate: [{(FRAMERATE):.0f}]",
    f"Gravity: {gravity_set[grid.orientation]} ",
    f"Simulation: {pause_set[PAUSED]} "
])

    timer = Timer()

    # main loop 
    while True:
        pressed_key = get_keypress()
        ticked = False

        if not PAUSED and timer.diff() > (1/FRAMERATE):
            grid.record_undo()
            grid.update()
            timer.reset()
            HUE += HUE_CHANGE
            FRAMENUM += 1
            ticked = True

        grid.handle_pointer(pressed_key)
        grid.handle_action(pressed_key)
        grid.handle_brush_attributes(pressed_key, elements, shapes_set)
        grid.handle_orientation(pressed_key)
        grid.handle_clear(pressed_key)
        grid.handle_paused(pressed_key)
        grid.handle_shuffle(pressed_key)

        handle_RBS(pressed_key)
        handle_framerate(pressed_key)

        if grid.brush_size == 0:
            grid.show_pointer = 0
        else:
            grid.show_pointer = 1

        if pressed_key == "`":
            HUE_CHANGE = 1 - HUE_CHANGE
        if pressed_key == "/":
            grid.show_radiation_lines = not grid.show_radiation_lines

        if ticked or pressed_key is not None:
            grid.show(extra=[   
        f"Pointer: ({grid.pointer_x}, {grid.pointer_y}) [{elements[grid.matrix[grid.pointer_y][grid.pointer_x].state]}] LL:{grid.matrix[grid.pointer_y][grid.pointer_x].light_level}", 
        f"Brush: <{grid.brush_size}px> ({elements[grid.brush_type]}) [{shapes_set[grid.brush_shape]}]",
        f"Frame Rate: [{FRAMERATE}]",
        f"Gravity: {gravity_set[grid.orientation]} ",
        f"Simulation: {pause_set[PAUSED]} "
    ])
        else:
            sleep(0.002)
        # sleep(1/FRAMERATE)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        hide_terminal_cursor()
    finally:
        hide_terminal_cursor()
# master
