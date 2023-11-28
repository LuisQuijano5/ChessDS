#Issue when undoing against machine

import Hash

class GameState():
    def __init__(self):
        # self.board = [
        #     ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        #     ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        #     ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        # ]
        self.board = [
            ["--", "--", "--", "--", "bK", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "wR"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wR", "wN", "wB", "wR", "wK", "wR", "wN", "--"]
        ]
        self.moveFunction = {"P": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
                             "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingPos = (7, 4)
        self.blackKingPos = (0, 4)
        self.checks = 0
        self.checkMate = False
        self.staleMate = False

        #special moves
        self.specialMoveFunction = {"c": self.castle, "C": self.castle, "P": self.promotion,
                                    "E": self.enPassant}
        self.lastMove = None
        self.specialMoves = {}
        self.wKMoves = 0
        self.bKMoves = 0
        self.wRMoves = [0, 0]
        self.bRMoves = [0, 0]

        #hash
        self.hash = Hash.Table(self.board)

        #stalemate
        self.pieceValues = {"P": 10, "R": 7, "N": 3, "B": 4, "Q": 10, '-': 0, 'K': 0}
        self.wValue = 118
        self.counter = 0
        self.bValue = 118
        self.forceStop = False

        #evaluation
        self.evalPieceValues = {"P": 1, "R": 5, "N": 3, "B": 3.5, "Q": 10, '-': 0, 'K': 0}
        self.evalOnQuantity = 0

    """
    This methods "in game" help to keep all the hashing in the engine and not the main
    it distinguishes simulation check moves and real moves and simul from ai 
    """
    def makeInGameMove(self, move, real=True, review=False):
        if move is None:
            #print("Checkmate")
            self.forceStop = True
            self.checkMate = True
            return
        self.makeMove(move, real)

        if self.whiteToMove:
            if move.special == 'E':
                self.bValue -= self.pieceValues["P"]
                self.evalOnQuantity -= self.evalPieceValues["P"]
            else:
                self.bValue -= self.pieceValues[move.pieceCaptured[1]]
                self.evalOnQuantity -= self.evalPieceValues[move.pieceCaptured[1]]
            if move.special == "P":
                self.evalOnQuantity -= 9
        else:
            if move.special == 'E':
                self.wValue -= self.pieceValues["P"]
                self.evalOnQuantity += self.evalPieceValues["P"]
            else:
                self.wValue -= self.pieceValues[move.pieceCaptured[1]]
                self.evalOnQuantity += self.evalPieceValues[move.pieceCaptured[1]]
            if move.special == "P":
                self.evalOnQuantity += 9
        if not review:
            return

        self.hash.getMoveHash(move, True)
        for k, v in self.hash.table.items():
            print(k, v)
        #50move rule
        if self.hash.table[self.hash.hash] >= 3:
            #print("StaleMate by repetition of positions")
            self.forceStop = True
            self.staleMate = True
        if move.pieceCaptured != "--" or move.pieceMoved[1] == "P":
            self.counter = 0
        if self.counter >= 50:
            #print("StaleMate by 50 move rule")
            self.forceStop = True
            self.staleMate = True
        #insufficient material
        if self.wValue < 7 and self.bValue < 7:
            #print("StaleMate by insufficient material")
            self.forceStop = True
            self.staleMate = True
        self.counter += 1#counter of moves w/pawn or capture

    def undoInGameMove(self, real=True, review=False):
        if len(self.moveLog) != 0:
            aux = self.undoMove(real)
            if self.forceStop: self.forceStop = False
            if self.staleMate: self.staleMate = False
            if self.checkMate: self.checkMate = False

            if aux.moveID[0] == "b":
                if aux.special == 'E':
                    self.bValue += self.pieceValues["P"]
                    self.evalOnQuantity += self.evalPieceValues["P"]
                else:
                    self.bValue += self.pieceValues[aux.pieceCaptured[1]]
                    self.evalOnQuantity += self.evalPieceValues[aux.pieceCaptured[1]]
            else:
                if aux.special == 'E':
                    self.wValue += self.pieceValues["P"]
                    self.evalOnQuantity -= self.evalPieceValues["P"]
                else:
                    self.wValue += self.pieceValues[aux.pieceCaptured[1]]
                    self.evalOnQuantity -= self.evalPieceValues[aux.pieceCaptured[1]]

            if not review:
                return
            self.hash.getMoveHash(aux, False)
            self.counter -= 1

    # for simul of checks
    def makeMove(self, move, real=True):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        if move.pieceMoved == "wK":
            self.whiteKingPos = (move.endRow, move.endCol)
            self.wKMoves += 1
        elif move.pieceMoved == "bK":
            self.blackKingPos = (move.endRow, move.endCol)
            self.bKMoves += 1
        if move.moveID[1] == "R": self.checkRMoves(move, 1)
        if move.special != "":
            self.specialMoveFunction[move.special](True, move)
        if real:
            self.whiteToMove = not self.whiteToMove


    def undoMove(self, real=True):
        if len(self.moveLog) != 0:
            moveToUndo = self.moveLog.pop()
            self.board[moveToUndo.startRow][moveToUndo.startCol] = moveToUndo.pieceMoved
            self.board[moveToUndo.endRow][moveToUndo.endCol] = moveToUndo.pieceCaptured
            if moveToUndo.pieceMoved == "wK":
                self.whiteKingPos = (moveToUndo.startRow, moveToUndo.startCol)
                self.wKMoves -= 1
            elif moveToUndo.pieceMoved == "bK":
                self.blackKingPos = (moveToUndo.startRow, moveToUndo.startCol)
                self.bKMoves -= 1
            if moveToUndo.moveID[1] == "R": self.checkRMoves(moveToUndo, -1)
            if moveToUndo.special != "":
                self.specialMoveFunction[moveToUndo.special](False, moveToUndo)
            if real:
                self.whiteToMove = not self.whiteToMove
            return moveToUndo

    """only legal moves"""
    def getValidMoves(self):
        #special movements
        if len(self.moveLog) > 0:
            self.lastMove = self.moveLog[-1]
            self.lastMove = self.lastMove.moveID

        self.specialMoves = {}
        possibleMoves = self.getAllPossibleMoves()
        legalMoves = []
        for move in possibleMoves:
            if move.special.lower() == "c":
                if not self.checkCheck():
                    continue
            self.makeMove(move)
            self.whiteToMove = not self.whiteToMove
            if self.checkCheck():
                legalMoves.append(move)
            self.undoMove()
            self.whiteToMove = not self.whiteToMove
        self.checkCheck()
        if len(legalMoves) == 0 and self.checks > 0:
            #print("CheckMate black wins" if self.whiteToMove else "CheckMate white wins")
            self.forceStop = True
            self.checkMate = True
        elif len(legalMoves) == 0:
            #print("Stalemate")
            self.forceStop = True
            self.staleMate = True
        return legalMoves

    def checkCheck(self):
        self.checks = 0
        noInterest = []
        kP = self.whiteKingPos if self.whiteToMove else self.blackKingPos #king pos
        for i in ["P", "Q", "K", "R", "N", "B"]:
            self.moveFunction[i](kP[0], kP[1], noInterest)
            if self.checks != 0:
                return False
        return True

    """all possible moves """
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]  # w or b
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunction[piece](r, c, moves)
        return moves

    """
    Getting all the possible move of the piece selected
    """
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if r <= 0:
                return
            if self.board[r - 1][c] == "--":
                if r == 1:
                    move = Move((r, c), (r - 1, c), self.board, "P")
                    moves.append(move)
                    self.specialMoves[move.moveID] = [move]
                else:
                    moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0 and self.board[r - 1][c - 1][0] == "b":
                if r == 1:
                    move = Move((r, c), (r - 1, c - 1), self.board, "P")
                    moves.append(move)
                    self.specialMoves[move.moveID] = [move]
                else:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                if self.board[r - 1][c - 1] == "bP":
                    self.checks += 1
            if c + 1 <= 7 and self.board[r - 1][c + 1][0] == "b":
                if r == 1:
                    move = Move((r, c), (r - 1, c + 1), self.board, "P")
                    moves.append(move)
                    self.specialMoves[move.moveID] = [move]
                else:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                if self.board[r - 1][c + 1] == "bP":
                    self.checks += 1
            if r == 3 and self.lastMove is not None and self.lastMove[1:3] == "P1" and self.lastMove[-2] == "3":#en passnt
                aux = int(self.lastMove[-1])
                if abs(c - aux) > 1 or c == aux:
                    pass
                elif c > aux:
                    move = Move((r, c), (r - 1, c - 1), self.board, "E")
                    moves.append(move)
                    self.specialMoves[move.moveID] = [move]
                else:
                    move = Move((r, c), (r - 1, c + 1), self.board, "E")
                    moves.append(move)
                    self.specialMoves[move.moveID] = [move]
        #black pawns
        else:
            if r >= 7:
                return
            if self.board[r + 1][c] == "--":
                if r == 6:
                    move = Move((r, c), (r + 1, c), self.board, "P")
                    moves.append(move)
                    self.specialMoves[move.moveID] = [move]
                else:
                    moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
                elif r == 6:
                    moves.append(Move((r, c), (r + 1, c), self.board, "P"))
            if c - 1 >= 0 and self.board[r + 1][c - 1][0] == "w":
                if r == 6:
                    move = Move((r, c), (r + 1, c - 1), self.board, "P")
                    moves.append(move)
                    self.specialMoves[move.moveID] = [move]
                else:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                if self.board[r + 1][c - 1] == "wP":
                    self.checks += 1
            if c + 1 <= 7 and self.board[r + 1][c + 1][0] == "w":
                if r == 6:
                    move = Move((r, c), (r + 1, c + 1), self.board, "P")
                    moves.append(move)
                    self.specialMoves[move.moveID] = [move]
                else:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                if self.board[r + 1][c + 1] == "wP":
                    self.checks += 1
            if r == 4 and self.lastMove[1:3] == "P6" and self.lastMove[-2] == "4":
                aux = int(self.lastMove[-1])
                if abs(c - aux) > 1 or c == aux:
                    pass
                elif c > aux:
                    move = Move((r, c), (r + 1, c - 1), self.board, "E")
                    moves.append(move)
                    self.specialMoves[move.moveID] = [move]
                else:
                    move = Move((r, c), (r + 1, c + 1), self.board, "E")
                    moves.append(move)
                    self.specialMoves[move.moveID] = [move]

    def getRookMoves(self, r, c, moves):
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endColumn = c + d[1] * i
                if not (0 <= endRow < 8 and 0 <= endColumn < 8):
                    break
                endPiece = self.board[endRow][endColumn]
                if endPiece == "--":
                    moves.append(Move((r, c), (endRow, endColumn), self.board))
                elif endPiece[0] == enemyColor:
                    moves.append(Move((r, c), (endRow, endColumn), self.board))
                    if endPiece[1] == "R" or endPiece[1] == "Q":
                        self.checks += 1
                    break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        directions = [(2,-1), (2,1), (-2,-1), (-2,1), (-1,2), (1,2), (-1,-2), (1,-2)]
        allyColor = "w" if self.whiteToMove else "b"
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if not (0 <= endRow < 8 and 0 <= endCol < 8):
                continue
            endPiece = self.board[endRow][endCol]
            if endPiece[0] != allyColor:
                moves.append(Move((r, c), (endRow, endCol), self.board))
                if endPiece[1] == "N":
                    self.checks += 1

    def getBishopMoves(self, r, c, moves):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if not (0 <= endRow < 8 and 0 <= endCol < 8):
                    break
                endPiece = self.board[endRow][endCol]
                if endPiece == "--":
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                elif endPiece[0] == enemyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                    if endPiece[1] == "B" or endPiece[1] == "Q":
                        self.checks += 1
                    break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + directions[i][0]
            endCol = c + directions[i][1]
            if not (0 <= endRow < 8 and 0 <= endCol < 8):
                continue
            endPiece = self.board[endRow][endCol]
            if endPiece[0] != allyColor:
                moves.append(Move((r, c), (endRow, endCol), self.board))
                if endPiece[1] == "K":
                    self.checks += 1
        #Castling
        if self.wKMoves == 0 and self.whiteToMove:
            if self.wRMoves[1] == 0 and self.board[7][5] == "--" and self.board[7][6] == "--" \
                    and self.board[7][7] == "wR":
                move = Move((r,c), (r, 6), self.board, "c")
                moves.append(move)
                self.specialMoves[move.moveID] = move
            if self.wRMoves[0] == 0 and self.board[7][3] == "--" and self.board[7][2] == "--" \
                    and self.board[7][1] == "--" and self.board[7][0] == "wR":
                move = Move((r,c), (r, 2), self.board, "C")
                moves.append(move)
                self.specialMoves[move.moveID] = move
        elif self.bKMoves == 0 and not self.whiteToMove:
            if self.wRMoves[1] == 0 and self.board[0][5] == "--" and self.board[0][6] == "--" \
                    and self.board[0][7] == "bR":
                move = Move((r, c), (r, 6), self.board, "c")
                moves.append(move)
                self.specialMoves[move.moveID] = move
            if self.wRMoves[0] == 0 and self.board[0][3] == "--" and self.board[0][2] == "--" \
                    and self.board[7][1] == "--" and self.board[0][0] == "bR":
                move = Move((r,c), (r, 2), self.board, "C")
                moves.append(move)
                self.specialMoves[move.moveID] = move

    def castle(self, do, move):
        r = 7 if move.pieceMoved[0] == "w" else 0
        piece = "wR" if move.pieceMoved[0] == "w" else "bR"
        c1 = 0 if move.special == "C" else 7
        c2 = 3 if move.special == "C" else 5
        if do:
            self.board[r][c1] = "--"
            self.board[r][c2] = piece
        else:
            self.board[r][c1] = piece
            self.board[r][c2] = "--"

    def promotion(self, do, move):
        if do:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0]+"Q"
        else:
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.board[move.startRow][move.startCol] = move.pieceMoved

    def enPassant(self, do, move):
        if do:
            if move.pieceMoved[0] == "b":
                self.board[move.endRow - 1][move.endCol] = "--"  # black movement
            else:
                self.board[move.endRow + 1][move.endCol] = "--"  # white movement
        else:
            if move.pieceMoved[0] == "b":
                self.board[move.endRow - 1][move.endCol] = "wP"  # black movement
            else:
                self.board[move.endRow + 1][move.endCol] = "bP"  # white movement

    def checkRMoves(self, move, num):
        if move.pieceMoved[0] == "w" and move.startRow == "7":
            if move.startCol == "0":
                self.wRMoves[0] += num
            elif move.startCol == "7":
                self.wRMoves[1] += num
        elif move.startRow == "0":
            if move.startCol == "0":
                self.bRMoves[0] += num
            else:
                self.bRMoves[1] += num

    def printBoard(self):
        aux = ""
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                aux += self.board[i][j] + " "
            aux += "\n"
        return aux


class Move():
    rankToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRank = {v: k for k, v in rankToRows.items()}
    fileToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFile = {v: k for k, v in fileToCols.items()}

    def __init__(self, startSq, endSq, board, special=""):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.pieceMoved+str(self.startRow)+str(self.startCol)+str(self.endRow)+str(self.endCol)
        self.special = special
        if self.pieceMoved[1] == 'K':
            if self.special == 'E' or self.special == 'P':
                self.special = ''

    """Overriding == method"""
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFile[c] + self.rowsToRank[r]

