import random

pieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 1000
STATEMATE = 0
DEPTH = 2

def findRandomMove(validmoves):
    return validmoves[random.randint(0, len(validmoves) - 1)]

def findBestMove(gs, validMoves):
    random.shuffle(validMoves)
    maxScore = -CHECKMATE
    bestMove = None
    for move in validMoves:
        tempGs = gs.clone()
        tempGs.makeMove(move, True)
        nextMoves = tempGs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(tempGs, nextMoves, DEPTH - 1, -CHECKMATE, CHECKMATE, 1 if tempGs.whiteToMove else -1)
        if score > maxScore:
            maxScore = score
            bestMove = move
    return bestMove

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move, True)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        maxScore = max(maxScore, score)
        alpha = max(alpha, score)
        gs.undoMove()
        if alpha >= beta:
            break
    return maxScore

def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.stalemate:
        return STATEMATE
    score = 0
    for row in range(8):
        for col in range(8):
            square = gs.board[row][col]
            if square[0] == 'w':
                score += pieceScore[square[1]]
                if square[1] in ['p', 'N'] and col in [3, 4] and row in [2, 3]:
                    score += 0.5
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
                if square[1] in ['p', 'N'] and col in [3, 4] and row in [4, 5]:
                    score -= 0.5
    return score