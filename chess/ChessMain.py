import pygame as p
import ChessEngine
import SmartMove


p.init()


WIDTH = HEIGHT = 750
DIMENTION = 8
SQ_SIZE = HEIGHT // DIMENTION
MAX_FPS = 15
IMAGES = {}


def loadImage():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("./assets/imgs-80px/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def drawMenu(screen):
    background = p.image.load("./assets/backgrounds/back3.png")  
    background = p.transform.scale(background, (WIDTH, HEIGHT))  
    screen.blit(background, (0, 0)) 
    
    font = p.font.SysFont("Helvitca", 45, True, False)
    text_start = font.render("Start", True, p.Color('White'))
    text_ai = font.render("Two players", True, p.Color('White'))
    text_exit = font.render("Exit", True, p.Color('White'))
    
    screen.blit(text_start, (WIDTH // 2 - text_start.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(text_ai, (WIDTH // 2 - text_ai.get_width() // 2, HEIGHT // 2))
    screen.blit(text_exit, (WIDTH // 2 - text_exit.get_width() // 2, HEIGHT // 2 + 60))
    p.display.flip()



def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))  
    clock = p.time.Clock()  
    screen.fill(p.Color("white"))  
    gs = ChessEngine.GameState()  
    validMoves = gs.getValidMoves()  
    moveMade = False  
    animate = False  
    loadImage()  
    running = True  
    sqSelected = ()  
    playerClicks = []  
    gameOver = False  
    playerOne = True  
    playerTwo = False  
    showMenu = True  

    while running:
        if showMenu:
            drawMenu(screen)
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()
                    if WIDTH // 2 - 100 <= location[0] <= WIDTH // 2 + 100:
                        if HEIGHT // 2 - 60 <= location[1] <= HEIGHT // 2 - 30:
                            showMenu = False  
                        elif HEIGHT // 2 <= location[1] <= HEIGHT // 2 + 30:
                            showMenu = False  
                            playerTwo = True  
                        elif HEIGHT // 2 + 60 <= location[1] <= HEIGHT // 2 + 90:
                            running = False  
        else:
            humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
            
            for e in p.event.get():
                if e.type == p.QUIT:  
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    showMenu = True
                    playerTwo = False
                
                elif e.type == p.MOUSEBUTTONDOWN:  
                    if not gameOver and humanTurn:
                        location = p.mouse.get_pos()  
                        col = location[0] // SQ_SIZE  
                        row = location[1] // SQ_SIZE  
                        if sqSelected == (row, col):  
                            sqSelected = ()  
                            playerClicks = []  
                        else:
                            sqSelected = (row, col)  
                            playerClicks.append(sqSelected)  
                        if len(playerClicks) == 2:  
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)  
                            print(move.getChessNotation())  
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    gs.makeMove(validMoves[i])  
                                    moveMade = True  
                                    animate = True  
                                    sqSelected = ()  
                                    playerClicks = []  
                            if not moveMade:
                                playerClicks = [sqSelected]  
                
                elif e.type == p.KEYDOWN:  
                    if e.key == p.K_z:  
                        gs.undoMove()
                        moveMade = True
                        animate = False
                    if e.key == p.K_r:  
                        gs = ChessEngine.GameState()
                        validMoves = gs.getValidMoves()
                        sqSelected = ()
                        playerClicks = []
                        moveMade = False
                        animate = False

            if not gameOver and not humanTurn:
                AIMove = SmartMove.findBestMove(gs, validMoves)  
                if AIMove == None:
                    AIMove = SmartMove.findRandomMove(validMoves)  
                gs.makeMove(AIMove)  
                moveMade = True
                animate = True

            if moveMade:  
                if animate:
                    animaMove(gs.moveLog[-1], screen, gs.board, clock)  
                validMoves = gs.getValidMoves()  
                moveMade = False
                animate = False

            drawGameState(screen, gs, validMoves, sqSelected)  

            if gs.checkmate:  
                gameOver = True
                if gs.whiteToMove:
                    drawText(screen, 'Black wins by checkmate')  
                else:
                    drawText(screen, 'White wins by checkmate')  
            elif gs.stalemate:  
                gameOver = True
                drawText(screen, 'Stalemate')  

            clock.tick(MAX_FPS)  
            p.display.flip()  

def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):  
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  
            s.fill(p.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))

def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)  
    highlightSquares(screen, gs, validMoves, sqSelected)  
    drawPieces(screen, gs.board)  

def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]  
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            color = colors[(r + c) % 2]  
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))  

def drawPieces(screen, board):
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            piece = board[r][c]
            if piece != "--":  
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))  

def animaMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow  
    dC = move.endCol - move.startCol  
    framesPerSquare = 10  
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare  
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)  
        drawPieces(screen, board)  

        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)

        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
            
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)  

def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 50, True, False)  
    textObject = font.render(text, 0, p.Color('White'))  
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObject.get_width() / 2, HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)  
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))  

if __name__ == "__main__":
    main()
