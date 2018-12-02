import random

class Maze:
    def __init__(self, size):
        self.maze = [[Node(i, j) for j in range(size)] for i in range(size)]
        self.wumpusAlive = True


    def setMaze(self): #generates node and sets them
        for i, row in enumerate(self.maze):
            for j, element in enumerate(row):
                #set neighbors
                if j+1 <= len(row)-1:
                    element.neighbors.append(self.maze[i][j+1])
                if j-1 >= 0:
                    element.neighbors.append(self.maze[i][j-1])
                if i-1 >= 0:
                    element.neighbors.append(self.maze[i-1][j])
                if i+1 <= len(self.maze)-1:
                    element.neighbors.append(self.maze[i+1][j])

    def setMap(self):
        for row in self.maze:
            for element in row:
                element.stench = None
                element.breeze = None
                element.pit = None
                element.wumpus = None
                element.gold = None
                element.valid = None
                
    def setHazards(self):
        for row in self.maze:
            for element in row:
                if element is not self.maze[0][0]:
                    if self.pit():
                        element.value = 'P'
                        element.pit = True
                        element.setBreeze()
        self.wumpus()
        self.gold()

    def pit(self): #determines if node is pit
        if random.random() < .2:
            return True
        return False

    def wumpus(self): #determines if node is wumpus
        x = random.randint(0, len(self.maze)-1)
        y = random.randint(0, len(self.maze)-1)
        if self.maze[x][y].pit or x is 0 and y is 0: #if node is pit or start, try again
            self.wumpus()
        else:
            self.maze[x][y].value = 'W'
            self.maze[x][y].wumpus = True
            self.maze[x][y].setStench()

    def gold(self): #determines if node has gold
        x = random.randint(0, len(self.maze)-1)
        y = random.randint(0, len(self.maze)-1)
        if self.maze[x][y].pit or x is 0 and y is 0: #if node is pit or start, try again
            self.gold()
        else:
            if self.maze[x][y].value is 'W':
                self.maze[x][y].value = '*' #Both wumpus and gold
            else:
                self.maze[x][y].value = 'G'
            self.maze[x][y].gold = True


    def printMaze(self):
        for row in self.maze:
            for element in row:
                print(element.value, end='')
            print('')
        print()


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.value = '_'
        self.neighbors = []

        self.pit = False
        self.wumpus = False
        self.gold = False
        self.previous = None

        self.stench = False
        self.breeze = False

    def setStench(self): #set neighbor nodes to have a stench
        for neighbor in self.neighbors:
            neighbor.stench = True

    def eliminateStench(self): #set neighbor nodes to get rid of stench if wumpus is killed
        for neighbor in self.neighbors:
            neighbor.stench = False

    def setBreeze(self): #set neighbor nodes to have a breeze
        for neighbor in self.neighbors:
            neighbor.breeze = True
