class Node:
    def __init__(self, move):
        self.move = move
        self.eval = None
        self.n = 0
        self.childs = []

    def isLeaf(self):
        return len(self.childs) == 0

    def setChilds(self, moves):
        self.childs.append(moves)
        self.childs = self.childs.pop()