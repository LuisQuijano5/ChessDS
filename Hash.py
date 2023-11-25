import random

class Table:
    bound = 1000000000
    table = {}
    def __init__(self, board):
        self.evalHash = {}
        self.emptyBoardHash = 0
        self.pieces = {"bP": random.randint(0, self.bound), "bR": random.randint(0, self.bound),
                       "bN": random.randint(0, self.bound), "bB": random.randint(0, self.bound),
                       "bQ": random.randint(0, self.bound), "bK": random.randint(0, self.bound),
                       "wB": random.randint(0, self.bound), "wN": random.randint(0, self.bound),
                       "wR": random.randint(0, self.bound), "wP": random.randint(0, self.bound),
                       "wQ": random.randint(0, self.bound), "wK": random.randint(0, self.bound),
                       "--": random.randint(0, self.bound)}

        self.sqValues = []
        self.hash = 0
        for i in range(8):
            self.sqValues.append([])
            for j in range(8):
                self.sqValues[i].append(random.randint(0, self.bound))
                self.emptyBoardHash ^= self.getHash('--', i, j)
                self.hash ^= self.getHash(board[i][j], i, j)
        self.table[self.hash] = 1

    def getHash(self, piece, i, j):
        return self.sqValues[i][j] + self.pieces.get(piece)

    def eval(self, value):
        self.evalHash[self.hash] = value

    def getMoveHash(self, move):
        self.hash ^= self.getHash(move.pieceMoved, move.startRow, move.startCol)
        self.hash ^= self.getHash("--", move.startRow, move.startCol)
        self.hash ^= self.getHash(move.pieceCaptured, move.endRow, move.endCol)
        self.hash ^= self.getHash(move.pieceMoved, move.endRow, move.endCol)

        #special moves
        if move.special == "":
            pass
        elif move.special == "E":
            self.hash ^= self.getHash(move.moveID[0] + "P", move.startRow, move.endCol)
            self.hash ^= self.getHash("--", move.startRow, move.endCol)
        elif move.special == "P":
            self.hash ^= self.getHash(move.pieceMoved, move.endRow, move.endCol)
            self.hash ^= self.getHash(move.moveID[0] + "Q", move.endRow, move.endCol)
        elif move.special.lower() == "c":
            r = 7 if move.pieceMoved[0] == "w" else 0
            c1 = 0 if move.special == "C" else 7
            c2 = 3 if move.special == "C" else 5
            self.hash ^= self.getHash(move.moveID[0] + "R", r, c1)
            self.hash ^= self.getHash("--", r, c1)
            self.hash ^= self.getHash("--", r, c2)
            self.hash ^= self.getHash(move.moveID[0] + "R", r, c2)

        if self.hash in self.table:
            self.table[self.hash] += 1
        else:
            self.table[self.hash] = 1
