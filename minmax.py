import random
import ChessEngine as ce
import minmaxnodes as T


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


class MinMax:
    def __init__(self, isWhite, gamestate):
        self.color = 1 if isWhite else -1
        self.gs = gamestate
        self.rootNode = T.Node(self.gs, self.color == 1)
        self.depth = 500

    def updateRoot(self, node):
        aux = self.gs.moveLog.pop()
        if node is not None:
            if not node.allChildren() or len(node.children) == 0:
                node.expand()
            for i in node.children:
                if i.move.moveID == aux.moveID:
                    self.rootNode = i
                    break
            self.rootNode.makeNodeRoot()

    def search(self):
        self.rootNode.n += 1
        counter = 0
        currentNode = self.rootNode
        while True:
            flag = False
            counter += 1
            if not currentNode.isLeaf():
                currentNode = currentNode.select()
                if currentNode is None:
                    currentNode = self.rootNode
                    break
            else:
                if currentNode.n == 0:
                    currentNode.rollout() #includes undoing of moves and backprop
                    currentNode = self.rootNode
                    flag = True
                else:
                    currentNode.expand()
                    currentNode = currentNode.select()
                    if currentNode is None:
                        currentNode = self.rootNode
                        break
            if counter > self.depth and flag:
                break
        maxNode = self.bestMove()
        self.gs.whiteToMove = self.color == -1
        return maxNode

    def bestMove(self):
        highest = 0
        maxNode = None
        for i in self.rootNode.children:
            print(i.move.moveID, i.eval, i.n)
            if maxNode is None:
                maxNode = i
                highest = self.color * maxNode.eval
                continue
            elif i.eval == highest:
                maxNode = i if random.randint(0, 1) == 0 else maxNode
                highest = self.color * maxNode.eval
            else:
                if self.color == -1:
                    if i.eval > highest:
                        maxNode = i
                        highest = self.color * maxNode.eval
                else:
                    if i.eval < highest:
                        maxNode = i
                        highest = self.color * maxNode.eval
        print(maxNode.move.moveID)
        print(highest)
        return maxNode