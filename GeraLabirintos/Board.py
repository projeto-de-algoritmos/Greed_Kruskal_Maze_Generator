from pygame import draw, Surface
from colors import BLACK, WALL
from random import randint

class Board():
    def __init__(self, width: int, height: int, horizontal: int, vertical: int, margin: int, standard_color: tuple) -> None:
        self.width = width
        self.height = height
        self.vertical = vertical
        self.horizontal = horizontal
        self.margin = margin
        self.color = standard_color
        # directions to walk
        self.dx = [ -1, 1, 0,  0]
        self.dy = [  0, 0, 1, -1]
        self.grid = [[standard_color for i in range(vertical)] for j in range(horizontal)]

    def out_of_range(self, x: int, y: int) -> bool:
        """tells if x or y access self.grid invalid position

                Parameters:
                        x (int): x position in grid
                        y (int): y position in grid

                Returns:
                        True (bool):  is out of range
                        False (bool): is in range
        """
        return (x < 0 or y < 0 or x >= self.horizontal or y >= self.vertical)

    def draw_grid(self, screen: Surface) -> None:
        """draw grid to specific screen

                Parameters:
                        screen (Surface): game screen

                Returns:
                        None
        """
        for row in range(self.horizontal):
            for column in range(self.vertical):
                draw.rect(screen,
                  self.grid[row][column],
                  [(self.margin + self.width) * (column) + self.margin,
                  (self.margin + self.height) * (row) + self.margin,
                  self.width,
                  self.height])

    def maze_prim(self, x: int, y: int, screen: Surface) -> None:
        """draw maze in the screen based on prim's algorithm

                Parameters:
                        x (int): x screen coordinates
                        y (int): y screen coordinates
                        screen (Surface): game screen

                Returns:
                        None
        """
        check = [[False for i in range(self.vertical)] for j in range(self.horizontal)]
        vetX = []
        vetY = []
        # neighbors
        vetNX = []
        vetNY = []

        vetX.append(x)
        vetY.append(y)
        vetNX.append(0)
        vetNY.append(0)

        while vetX:

                n = randint(0, len(vetX) - 1)

                if self.out_of_range(vetX[n], vetY[n]) or check[vetX[n]][vetY[n]] == True:
                    vetX.pop(n)
                    vetY.pop(n)
                    vetNX.pop(n)
                    vetNY.pop(n)
                    continue

                posX = (self.margin + self.width) * (vetY[n]) + self.margin
                posY = (self.margin + self.height) * (vetX[n]) + self.margin
                draw.rect(screen, WALL, (posX, posY, 13, 13))

                posX = (self.margin + self.width) * (vetY[n] + vetNY[n]/2) + self.margin
                posY = (self.margin + self.height) * (vetX[n] + vetNX[n]/2) + self.margin
                draw.rect(screen, WALL, (posX, posY, 13, 13))

                check[vetX[n]][vetY[n]] = True
                
                for i in range(0, 4):
                    newX = vetX[n]+self.dx[i]
                    newY = vetY[n]+self.dy[i]
                    if not (self.out_of_range(newX, newY) or check[newX][newY] == True):
                        vetX.append(newX)
                        vetY.append(newY)
                        vetNX.append(self.dx[i])
                        vetNY.append(self.dy[i])

    def maze_kruskal(self, screen: Surface) -> None:
        """draw maze in the screen based on kruskal's algorithm

                Parameters:
                        screen (Surface): game screen

                Returns:
                        None
        """
        # x1 and y1 are the main coordinates
        # x2 and y2 are their edge neighboors
        x1 = []
        y1 = []
        x2 = []
        y2 = []

        for x in range(0, self.horizontal):
            for y in range(0, self.vertical):
                for i in range(0, 4):
                    newX = x+self.dx[i]
                    newY = y+self.dy[i]
                    if not (self.out_of_range(newX, newY)):
                        x1.append(x)
                        y1.append(y)
                        x2.append(newX)
                        y2.append(newY)

        check =  [[0 for i in range(self.vertical)] for j in range(self.horizontal)]
        
        while x1:
            n = randint(0, len(x1) - 1)
            sx1 = x1[n]
            sx2 = x2[n]
            sy1 = y1[n]
            sy2 = y2[n]

            if (check[sx1][sy1] + check[sx2][sy2]) == 0:
                key = randint(1, 9000000)
                check[sx1][sy1] = key
                check[sx2][sy2] = key
                self.draw_neighbor(screen, sx1, sx2, sy1, sy2)
                self.pop4(x1, x2, y1, y2, n)
                continue

            if check[sx1][sy1] == check[sx2][sy2]:
                self.pop4(x1, x2, y1, y2, n)
                continue

            if check[sx1][sy1] == 0:
                check[sx1][sy1] = check[sx2][sy2]
                self.draw_neighbor(screen, sx1, sx2, sy1, sy2)
                self.pop4(x1, x2, y1, y2, n)
                continue

            if check[sx2][sy2] == 0:
                check[sx2][sy2] = check[sx1][sy1]
                self.draw_neighbor(screen, sx1, sx2, sy1, sy2)
                self.pop4(x1, x2, y1, y2, n)
                continue

            target = check[sx1][sy1]
            for x in range(0, self.horizontal):
                for y in range(0, self.vertical):
                    if check[x][y] == target:
                        check[x][y] = check[sx2][sy2]
            self.draw_neighbor(screen, sx1, sx2, sy1, sy2)
            self.pop4(x1, x2, y1, y2, n)

    def draw_neighbor (self, screen, sx1, sx2, sy1, sy2) -> None:
        """draw wall between neighbors in the screen

                Parameters:
                        screen (Surface): game screen
                        sx1 (Integer): main coordinates
                        sx2 (Integer): main coordinates
                        sy1 (Integer): neighbors coordinates
                        sy2 (Integer): neighbors coordinates

                Returns:
                        None
        """
        posX = (self.margin + self.width) * (sy2) + self.margin
        posY = (self.margin + self.height) * (sx2) + self.margin
        draw.rect(screen, WALL, (posX, posY, 13, 13))

        posX = (self.margin + self.width) * (sy2 + (sy1 - sy2)/2) + self.margin
        posY = (self.margin + self.height) * (sx2 + (sx1 - sx2)/2) + self.margin
        draw.rect(screen, WALL, (posX, posY, 13, 13))
    
    def pop4(self, x1, x2, y1, y2, n) -> None:
        """pop all coordinates

                Parameters:
                        sx1 (Integer): main coordinates
                        sx2 (Integer): main coordinates
                        sy1 (Integer): neighbors coordinates
                        sy2 (Integer): neighbors coordinates

                Returns:
                        None
        """
        x1.pop(n)
        y1.pop(n)
        x2.pop(n)
        y2.pop(n)

