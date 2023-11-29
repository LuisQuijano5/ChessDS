import math
import random


def randomMove(moves):
    if len(moves) < 1:
        return None
    if len(moves) == 1:
        return moves[0]
    return moves[random.randint(0, len(moves) - 1)]


class NodeMM:
    def __init__(self, gamestate, isWhite, move=None, parent=None):
        self.parent = parent
        self.gs = gamestate
        self.eval = 0
        self.auxEval = 0
        self.n = 0
        self.children = []
        self.depth = 1
        self.move = move
        self.color = 1 if isWhite else -1
        if self.parent is None:
            self.validMoves = self.gs.getValidMoves()
        else:
            self.gs.whiteToMove = not self.color == 1
            self.gs.makeInGameMove(self.move, False)
            self.updateTurn()
            self.validMoves = self.gs.getValidMoves()
            self.gs.undoInGameMove(False)

    def makeNodeRoot(self):
        self.parent = None
        self.updateGs()

    def updateGs(self):
        self.gs.makeInGameMove(self.move, False)

    def isLeaf(self):
        return len(self.children) == 0

    def allChildren(self):
        return len(self.validMoves) == len(self.children)

    def select(self):
        max = -10000
        goTo = None
        if len(self.children) == 0:
            self.expand()
        for i in self.children:
            if i.n == 0:
                goTo = i
                break
            aux = i.getUCB1()
            if aux > max:
                goTo = i
                max = aux
            elif aux == max:
                rand = random.randint(0,1)
                goTo = i if rand == 0 else goTo
                max = aux if rand == 0 else max
        if goTo == None:
            self.eval = self.color * 100
            self.backProp()
            return None
        goTo.updateGs()
        return goTo

    def getUCB1(self):
        return self.color * self.eval + 50 * math.sqrt(math.log(self.parent.n)/self.n)

    def expand(self):
        for i in self.validMoves:
            self.children.append(Node(self.gs, not self.color == 1, i, self))

    def rollout(self):
        self.updateTurn()
        self.n += 1
        c = 0
        for i in range(self.depth):
            validMoves = self.gs.getValidMoves()
            if self.gs.checkMate or self.gs.staleMate:
                break
            self.gs.makeInGameMove(randomMove(validMoves))
            c += 1
        self.eval = self.evalPosition()
        self.undoMoves(c)
        self.backProp()

    def undoMoves(self, c):
        for i in range(c):
            self.gs.undoInGameMove()

    def updateTurn(self):
        self.gs.whiteToMove = not self.color == 1

    def backProp(self):
        aux = self
        aux.auxEval = aux.eval
        while aux.parent is not None:
            aux.parent.auxEval = aux.auxEval
            aux.parent.eval += aux.parent.auxEval
            aux.parent.n += 1
            aux.gs.undoInGameMove()
            #print("BACK",aux.move.moveID, aux.eval, aux.auxEval)
            aux = aux.parent

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.move == other.move

    def evalPosition(self):
        temp = 0
        for i in range(len(self.gs.board)):
            for j in range(len(self.gs.board[i])):
                temp += self.gs.evalPieceValues[self.gs.board[i][j][1]] if self.gs.board[i][j][0] == "w" else -1 * self.gs.evalPieceValues[self.gs.board[i][j][1]]
        #print("evaleval", self.move.moveID,temp)
        eval = temp
        #print("eval",self.move.moveID, eval)
        #print("EVAL",eval)
        # eval += self.value * self.kingSafety()
        # eval += self.value * self.movesAvailable()#start of the game
        # eval += self.value * self.passedPawns() #endgame
        return eval