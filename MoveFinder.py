import random
import ChessEngine as ce
import Tree as T


def randomMove(moves):
    return moves[random.randint(0, len(moves)-1)]

def greedyMove(moves):
    gs = ce.GameState()
    bestMove = abs(gs.evalOnQuantity)
    move = None
    for i in moves:
        gs.makeInGameMove(i)
        if abs(gs.evalOnQuantity) > bestMove:
            move = i
            bestMove = abs(gs.evalOnQuantity)
        gs.undoInGameMove()
    if move is None:
        return randomMove(moves)
    return move


class MontecarloFinder:
    def __init__(self, isWhite, gamestate):
        self.color = 1 if isWhite else -1
        self.gs = gamestate
        self.rootNode = T.Node(self.gs, self.color == 1)
        self.depth = 20

    def updateRoot(self):
        aux = self.gs.moveLog[-1]
        for i in self.rootNode.children:
            if aux == i.move:
                self.rootNode = i
                self.rootNode.makeNodeRoot()
                print("Correct update of root")
                break

    def search(self):
        self.rootNode.n += 1
        currentNode = self.rootNode
        for _ in range(self.depth):
            if not currentNode.isLeaf():
                currentNode = currentNode.select()
                continue
            if currentNode.n == 0:
                currentNode.rollout() #includes undoing of moves and backprop
                currentNode = self.rootNode
                continue
            currentNode.expand()
            currentNode = currentNode.select()
        return self.bestMove()

    def bestMove(self):
        highest = 0
        maxNode = None
        for i in self.rootNode.children:
            if maxNode is None:
                maxNode = i
                highest = self.color * maxNode.eval
                continue
            if self.color * maxNode.eval > highest:
                maxNode = i
                highest = self.color * maxNode.eval
            elif self.color * maxNode.eval == highest:
                maxNode = i if random.randint(0,1) == 0 else maxNode
                highest = self.color * maxNode.eval
        return maxNode.move