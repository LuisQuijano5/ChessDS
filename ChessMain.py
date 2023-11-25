import pygame as p
import ChessEngine
import MoveFinder
import time

p.init() #initialize pygame
WIDTH = HEIGHT = 512
DIMENSIONS = 8 #8x8 of the board
SQUARE_SIZE = WIDTH // DIMENSIONS
MAX_FPS = 15
IMAGES = {}
peña = p.image.load("Res/peña2.png")
pacheco = p.image.load("Res/pachecoidiota.png")

"""
Initialize global dic of images. In a function to do it just once
"""
def loadImages():
    pieces=["wP", "bP", "wR", "bR", "wB", "bB", "wN", "bN", "wQ", "bQ", "wK", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("ChessPieces/" + piece + ".png"),(SQUARE_SIZE, SQUARE_SIZE))

"""
 main, it will handle input and updating graphics
"""
def main():
    aux = True
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flg var for when a move is made
    loadImages() #only once
    running = True
    sqSelected = () #last click of the user
    playerClicks = []

    #players
    bot = MoveFinder
    wPlayer = True
    bPlayer = False
    while(running):
        playerTurn = (wPlayer and gs.whiteToMove) or (bPlayer and not gs.whiteToMove)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse clicks
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gs.forceStop and playerTurn:
                    location = p.mouse.get_pos()
                    col = location[0] // SQUARE_SIZE
                    row = location[1] // SQUARE_SIZE
                    if sqSelected == (row, col): #click on the same sq
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2: #second click
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        if move in validMoves:
                            aux = gs.specialMoves.get(move.moveID, move)
                            if type(aux) == list: aux = aux.pop()
                            gs.makeInGameMove(aux)
                            print(aux.getChessNotation())
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                        else:
                            playerClicks = [sqSelected]
                    #key presses
            elif e.type == p.KEYDOWN and playerTurn:
                if e.key == p.K_z:
                    gs.undoInGameMove()
                    moveMade = True
                if e.key == p.K_p:
                    p.transform.scale(peña, (HEIGHT, WIDTH))
                    screen.fill((255, 255, 255))
                    screen.blit(peña, (0,0))
                    p.display.flip()
                    aux = False
                if e.key == p.K_x:
                    p.transform.scale(pacheco, (HEIGHT, WIDTH))
                    screen.fill((255, 255, 255))
                    screen.blit(pacheco, (0, 0))
                    p.display.flip()
                    aux = False
                if e.key == p.K_o:
                    aux = True
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False

        #move finder
        if not gs.forceStop and not playerTurn:
            time.sleep(0.5)
            move = bot.greedyMove(validMoves)
            aux = gs.specialMoves.get(move.moveID, move)
            if type(aux) == list: aux = aux.pop()
            gs.makeInGameMove(aux)
            #print(aux.getChessNotation())
            moveMade = True
            sqSelected = ()
            playerClicks = []

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        if(aux):
            drawGameState(screen,gs)
            clock.tick(MAX_FPS)
            p.display.flip()

"""
it draws all the graphics within the CURRENT game state
"""
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

"""
Draws board
"""
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("dark gray")] #light squares are even
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

"""
Draws pieces on the board
"""
def drawPieces(screen, board):
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            piece = board[r][c]
            if piece != "--": #not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

if __name__ == "__main__":
    main()