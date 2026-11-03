





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


print(
    DDA_line(x1 = 0, y1 = 0, x2 = 5, y2 = 0),
    "\n",
    DDA_line(x1 = 2, y1 = 2, x2 = 2, y2 = 7),
    "\n",
    DDA_line(x1 = 1, y1 = 1, x2 = 5, y2 = 5),
    "\n",
    DDA_line(x1 = 0, y1 = 0, x2 = 6, y2 = 2),
    "\n",
    DDA_line(x1 = 0, y1 = 0, x2 = 2, y2 = 6),
    "\n",
    DDA_line(x1 = 0, y1 = 4, x2 = 6, y2 = 1),
    "\n",
    DDA_line(x1 = 5, y1 = 5, x2 = 1, y2 = 3),
    "\n",
    DDA_line(x1 = 3, y1 = 3, x2 = 3, y2 = 3)
)