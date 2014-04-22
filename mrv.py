from sudoku import *
from backTracking import *

def getNeighbors(board, row, col):
    neighbors = [(row, i) for i in range(board.BoardSize) if i != col] + \
                [(i, col) for i in range(board.BoardSize) if i != row] + \
                getQuadrant(board, row, col)
    return set(neighbors)

def getRemainingValue(board, row, col):
    neighbors = getNeighbors(board, row, col)
    return set(range(1, board.BoardSize + 1)) - set([board.CurrentGameboard[pair[0]][pair[1]] for pair in neighbors])            

def updatePVB(board):
    PVB = []
    for i in range(board.BoardSize):
        PVB.append([[] for x in range(board.BoardSize)])
    for i in range(board.BoardSize):
        for j in range(board.BoardSize):
            if board.CurrentGameboard[i][j] == 0:
                PVB[i][j] = list(getRemainingValue(board, i, j))
            else:
                PVB[i][j] = 0
    return PVB

PVB = []

def increUpdatePVB(board, row, col, val):
    global PVB
    # print list(getNeighbors(board, row, col))
    for neighbor in list(getNeighbors(board, row, col)):
        if PVB[neighbor[0]][neighbor[1]] != 0:
            PVB[neighbor[0]][neighbor[1]] = list(set(PVB[neighbor[0]][neighbor[1]]) - set([val]))
    PVB[row][col] = 0

def backUpdatePVB(board, row, col, val):
    global PVB
    # print list(getNeighbors(board, row, col))
    for neighbor in list(getNeighbors(board, row, col)):
        if board.CurrentGameboard[neighbor[0]][neighbor[1]] == 0:
            PVB[neighbor[0]][neighbor[1]] = list(getRemainingValue(board, neighbor[0], neighbor[1]))
        else:
            PVB[neighbor[0]][neighbor[1]] = 0
    PVB[row][col] = list(getRemainingValue(board, row, col))

def findMRV(board, PVB):
    MRV = board.BoardSize + 1
    MRVPos = [-1, -1]
    MRV_list = []
    for i in range(board.BoardSize):
        for j in range(board.BoardSize):
            if PVB[i][j] == 0:
                continue
            elif len(PVB[i][j]) < MRV:
                MRVPos = [i, j]
                MRV_list = PVB[i][j]
                MRV = len(PVB[i][j])
    return [MRVPos, MRV_list]


def MRVSearch(board):
    global PVB
    global numCheck
    numCheck += 1
    if numCheck % 1000 == 0:
        print numCheck
    if iscomplete(board.CurrentGameboard):
        print "Yes, you did it!"
        return board # this prints the board
    else:
        MRV_list = findMRV(board,PVB)[1]
        MRVPos = findMRV(board,PVB)[0]
        # print "MRV list is " + str(MRV_list) + str(findMRV(board,PVB))
        if len(MRV_list) <= 0:
            return False
        r = MRVPos[0]
        c = MRVPos[1]
        for i in MRV_list:
            board.set_value(r, c, i)
            increUpdatePVB(board,r,c,i)
            tryMove = MRVSearch(board)
            if tryMove == False:
                board.set_value(r, c, 0)
                backUpdatePVB(board, r, c, i)
                continue
            else: return tryMove
        else: return False

# board_1 = SudokuBoard(4 ,parse_file("c:/Users/crazydonkey200/Documents/GitHub/SudokuSolver/Puzzles/4_4.sudoku"))
numCheck = 0
PVB = []
def tryMRVSearch(size, filename):
    print size, filename
    global numCheck
    global PVB
    numCheck = 0
    board_1 = SudokuBoard(size ,parse_file(filename))
    PVB = updatePVB(board_1)
    print board_1.CurrentGameboard
    PVB = updatePVB(board_1)
    solution = MRVSearch(board_1)
    if solution != False:
        print solution.CurrentGameboard
    else: print "Shit!"

##for i in range(1,21):
##    tryMRVSearch(9, "c:/Users/crazydonkey200/Documents/GitHub/SudokuSolver/Puzzles/9x9." + str(i) + ".sudoku")
##
##
##for i in range(1,21):
##    tryMRVSearch(16, "c:/Users/crazydonkey200/Documents/GitHub/SudokuSolver/Puzzles/16x16." + str(i) + ".sudoku")
##
##
#solution_backtrack = backTrack(board_1)
#if solution_backtrack != False:
#    print solution_backtrack.CurrentGameboard
#else: print "Shit!"
