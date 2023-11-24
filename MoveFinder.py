import random
import time
import ChessEngine as ce

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


# class MontecarloFinder:
#     def __init__(self, isWhite):
#         # evaluation
#         self.eval = 0
#
#         self.stalemate = 0
#         self.value = 1 if isWhite else -1
#         self.checkmateValue = self.value * 1000
#
#     """
#     This method will be the ones in charge of everything
#     realted to the eval of the position when move finder requires it
#     """
#     def evalPosition(self, board):
#         self.piecesQuantity(board)
#         return self.eval
#
#     def piecesQuantity(self):