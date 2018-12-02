import world
import random
import sys
from collections import deque

class Wumpus:
    def __init__(self, size):
        self.world = world.Maze(size)
        self.world.setMaze()
        self.world.setHazards()
        self.maze = self.world.maze

        self.world.printMaze()

        self.currentNode = self.maze[0][0] #start at 0,0
        self.m = world.Maze(size) #create maze of the same size to store logic of where to move
        self.m.setMaze() #identify neighbors
        self.m.setMap() #set all agents to None
        self.map = self.m.maze

        self.visited = [] #list of visited nodes
        self.Gold = False 
        self.score = 0

    def bfs(self, currentNode, finish): #bfs is used to go home with gold or to go to new undiscovered 'K' node
       #create queue, visited nodes gets reset
       queue = deque([currentNode])
       visitedNodes = []

       while len(queue) > 0:
          node = queue.pop()
          if node in visitedNodes:
             continue

          visitedNodes.append(node)
          if node is finish:
              self.updateMove(node, currentNode)
              return self.nodeLocation(node)

          for neighbor in node.neighbors:
             if neighbor not in visitedNodes and neighbor.value is 'K':
                neighbor.previous = node
                queue.appendleft(neighbor)
       return False
    
    def updateMove(self, node, finish): #after completing bfs, determine how many moves made then update overall score
        while node is not finish:
            self.score -= 1
            node = node.previous

    def location(self): #return location of node currently
        return self.map[self.currentNode.x][self.currentNode.y]

    def nodeLocation(self, node): #return location of node on map
        return self.maze[node.x][node.y]

    def evaluateNode(self, node, location, map, maze):
        self.visited.append(location)
        location.value = 'K'

        if node.gold: #if node is gold, take gold
            self.Gold = True

        if node.breeze: #if the node has a breeze, mark nodes as a possible pit
            location.breeze = True
            for neighbor in location.neighbors:
                if neighbor not in self.visited and neighbor.pit is not False:
                    neighbor.value = '?'
        else: #no breeze, mark all adjacent nodes as not a pit
            location.breeze = False
            for neighbor in location.neighbors:
                neighbor.pit = False

        if node.stench: #if the node has a stench, mark all other nodes as a possible wumpus
            location.stench = True
            for neighbor in location.neighbors:
                if neighbor not in self.visited and neighbor.wumpus is not False:
                    neighbor.value = '?'
        else: #no stench, mark all adjacent nodes as not wumpus
            location.stench = False
            for neighbor in location.neighbors:
                neighbor.wumpus = False
                
    def guessNode(self, node): #guess a random '?' spot
        guess = node.neighbors[random.randint(0, len(node.neighbors)-1)]

        if guess.value is not '?': #if the guess is not a '?' repeat
            guess = self.guessNode(node)

        return guess

    def determinePit(self, node): #determine where pits are
        validNodes = 0
        invalidNode = ''
        for neighbor in node.neighbors: #if all breeze children are 'K' except one, thats the pit
            if neighbor.value is 'K':
                validNodes += 1
            elif neighbor.value is '?':
                invalidNode = neighbor

        if validNodes == len(node.neighbors)-1:
            if invalidNode is not '':
                invalidNode.pit = True
                invalidNode.value = 'P'

    def evaluateWorld(self, map, maze): #evaluate current map to update nodes
        for row in map:
            for node in row:
                if node.pit is False and node.wumpus is False: #if a node if not a pit and wumpus, automatic 'K'
                    node.value = 'K'
                elif node.value is '?':
                    wumpusCount = 0
                    for neighbor in node.neighbors:
                        if neighbor.breeze is False and neighbor.stench is False: #if a '?' node has a normal node,cannot be a hazard
                            node.pit = False
                            node.wumpus = False
                            node.value = 'K'
                            break

                        if neighbor.stench:
                            wumpusCount += 1

                    if wumpusCount >= 2: #if a '?' has atleast 2 stench children, node is the wumpus
                        node.wumpus = True
                        node.value = 'W'
                    else:
                        node.wumpus = False

            for node in row:
                if node.breeze is True: #determine any pits with updated information
                    self.determinePit(node)


    def determineMove(self, node, location, map, maze): #check neighbors for a 'K' node that has not been visited, if all have, bfs to 'K' unvisited global node, else pick random '?'
        if self.Gold: #have gold, Go back home
            return self.bfs(location, map[0][0])

        for neighbor in location.neighbors: #check local neighbors for any unvisited 'K'
            if neighbor.value is 'K' and neighbor not in self.visited:
                self.score -= 1
                return self.nodeLocation(neighbor)

        for row in map: #check globally for 'K' nodes that aren't visited
            for element in row:
                if element.value is 'K' and element not in self.visited:
                    return self.bfs(location, element)

        #guess
        self.score -= 1
        return self.nodeLocation(self.guessNode(location))

    def gameOver(self): #check to see if current node is at a lethal spot or won
        if self.currentNode.pit: #if node is pit
            print('Yikes! You fell in a pit.')
            self.score -= 1000
            return True
        elif self.currentNode.wumpus: #if node is wumpus
            print('Uh-oh!You ran into the Wumpus!')
            self.score -= 1000
            return True
        elif self.Gold and self.currentNode is self.maze[0][0]: #if node is at the start and has the gold
            print('You made it out of the cave with some gold!')
            self.score += 1000
            return True
        return False
    
    def play(self): #play the damn game
        self.map[0][0].value = 'K'

        while not self.gameOver():
            node = self.location()
            self.evaluateNode(self.currentNode, node, self.map, self.maze)

            #printing current status of maze
            node.value = 'X'
            print('\nHas gold: {}'.format(self.Gold))
            print('Breeze: {} Stench: {}'.format(node.breeze, node.stench))
            self.m.printMaze()
            node.value = 'K'

            self.evaluateWorld(self.map, self.maze)
            self.currentNode = self.determineMove(self.currentNode, node, self.map, self.maze)
        print('Game Over!\nScore: {}'.format(self.score))



if __name__ == '__main__':
    game = Wumpus(int(sys.argv[1]))
    game.play()
