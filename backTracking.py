from sudoku import *

numChecks = 0

def backTrack(board, size = 0):
    global numChecks
    if size == 0: size = board.BoardSize
    if iscomplete(board.CurrentGameboard):
        print "\n this took us " + str(numChecks) + " consistency checks"
        numChecks = 0 ## just to reset the global
        return board # this prints the board
    else:
        for r in range(size):
            for c in range(size):
                if board.CurrentGameboard[r][c] != 0: continue
                else:
                    for i in range(1, size+1):
                        numChecks += 1
                        if isLegalMove(board, r, c, i):
                            board.set_value(r, c, i)
                            tryMove = backTrack(board, size)
                            if tryMove == False:
                                board.set_value(r, c, 0)
                                continue
                            else: return tryMove
                        else:
                            continue
                    return False ## if we can't put anything in an open spot, we can stop right now.
    numChecks = 0 ## just to reset the global
    return False
                            
