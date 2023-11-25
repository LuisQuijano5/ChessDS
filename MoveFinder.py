import random
import ChessEngine as ce
import Tree as t


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
    def __init__(self, isWhite):
        # evaluation
        self.eval = 0
        self.depth = 2
        self.gs = ce.GameState()
        self.currentNode = None
        self.stalemate = 0
        self.value = 1 if isWhite else -1
        self.checkmateValue = self.value * 1000

    def select(self):
        pass

    def getUBTC(self):
        pass

    def expand(self):
        moves = []
        for i in self.gs.getValidMoves():
            moves.append(t.Node(i))
        pass



    def rollout(self):
        for i in range(self.depth):
            self.gs.makeInGameMove(randomMove(self.gs.getValidMoves()))
            if self.gs.checkMate or self.gs.staleMate:
                break
        eval = self.evalPosition()

    def backProp(self):
        pass


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

    def kingSafety(self):
        eval = 0
        reference = (0,0)
        eval = self.value * self.pawnStructure()
        return eval

    def movesAvailable(self):
        pass


