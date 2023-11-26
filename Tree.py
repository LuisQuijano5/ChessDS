import math
import random


def randomMove(moves):
    return moves[random.randint(0, len(moves) - 1)]


class Node:
    def __init__(self, gamestate, isWhite, move = None, parent=None):
        self.parent = parent
        self.gs = gamestate
        self.eval = 0
        self.n = 0
        self.children = []
        self.validMoves = self.gs.getValidMoves()
        self.depth = 10
        self.move = move
        self.color = 1 if isWhite else -1

    def makeNodeRoot(self):
        self.parent = None
        self.move = None

    def updateGs(self):
        if self.move is not None:
            self.gs.makeInGameMove(self.move)

    def isLeaf(self):
        return len(self.children) == 0

    def allChildren(self):
        return len(self.validMoves) == len(self.children)

    def select(self):
        max = -1
        goTo = None
        for i in self.children:
            if i.n == 0 and i.eval == 0:
                goTo = i
                break
            aux = i.getUCB1()
            if aux > max:
                goTo = i
                max = aux
        goTo.updateGs()
        return goTo

    def getUCB1(self):
        return self.color * self.eval + 2 * math.sqrt(math.log(self.parent.n)/self.n)

    def expand(self):
        for i in self.validMoves:
            self.children.append(Node(self.gs, not self.color == 1, i, self))

    def rollout(self):
        self.n += 1
        c = 0
        for i in range(self.depth):
            self.gs.makeInGameMove(randomMove(self.validMoves))
            c += 1
            if self.gs.checkMate or self.gs.staleMate:
                break
        self.eval = self.evalPosition()
        self.undoMoves(c)
        self.backProp()

    def undoMoves(self, c):
        for i in range(c):
            self.gs.undoInGameMove()

    def backProp(self):
        aux = self
        while aux.parent is not None:
            aux.parent.eval += aux.eval
            aux.parent.n += 1
            aux.gs.undoInGameMove()
            aux = aux.parent


    """
    This method will be the ones in charge of everything
    realted to the eval of the position when move finder requires it
    """
    def evalPosition(self):
        eval = 0
        eval += self.value * self.kingSafety()
        eval += self.value * self.movesAvailable()#start of the game
        eval += self.value * self.passedPawns() #endgame
        return eval