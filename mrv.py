from sudoku import *
from backTracking import *

def getNeighbors(board, row, col):
    neighbors = [(row, i) for i in range(board.BoardSize) if i != col] + \
                [(i, col) for i in range(board.BoardSize) if i != row] + \
                getQuadrant(board, row, col)
    return set(neighbors) - set([(row, col)]) # because getQuadrant has self.

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
    global fuckingNumCheck
    fuckingNumCheck += 1
    #if fuckingNumCheck % 1000 == 0:
    #print fuckingNumCheck
    if iscomplete(board.CurrentGameboard):
        print "Yes, you did it!"
        print fuckingNumCheck
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
fuckingNumCheck = 0
PVB = []
def tryMRVSearch(size, filename):
    # print size, filename
    global fuckingNumCheck
    global PVB
    fuckingNumCheck = 0
    board_1 = SudokuBoard(size ,parse_file(filename))
    PVB = updatePVB(board_1)
    # print board_1.CurrentGameboard
    PVB = updatePVB(board_1)
    solution = MRVSearch(board_1)
    if solution != False:
        pass #print solution.CurrentGameboard
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

def findMRV_MCV(board, PVB):
    MRV = board.BoardSize + 1
    MRVPos = [-1, -1]
    MRV_list = []
    MCV = 0
    for i in range(board.BoardSize):
        for j in range(board.BoardSize):
            if PVB[i][j] == 0:
                continue
            elif (len(PVB[i][j]) < MRV) or ((len(PVB[i][j]) == MRV) and (getMCV(board, i, j) >  MCV)):
                MRVPos = [i, j]
                MRV_list = PVB[i][j]
                MRV = len(PVB[i][j])
                MCV = getMCV(board,i,j)
    #print [MRVPos, MRV_list]
    return [MRVPos, MRV_list]

def getMCV(board, row, col):
    return len([n for n in getNeighbors(board, row, col) if board.CurrentGameboard[n[0]][n[1]] == 0])

def MRV_MCV_Search(board):
    global PVB
    global fuckingNumCheck
    fuckingNumCheck += 1
    if fuckingNumCheck % 1000 == 0:
        print fuckingNumCheck
        #printBoard(board)
    if iscomplete(board.CurrentGameboard):
        print "Yes, you did it!"
        print fuckingNumCheck
        return board # this prints the board
    else:
        MRV_list = findMRV_MCV(board,PVB)[1]
        MRVPos = findMRV_MCV(board,PVB)[0]
        # print "MRV list is " + str(MRV_list) + str(findMRV(board,PVB))
        if len(MRV_list) <= 0:
            return False
        r = MRVPos[0]
        c = MRVPos[1]
        #print MRVPos, MRV_list
        for i in MRV_list:
            board.set_value(r, c, i)
            #print "fill in " + str(r) + "," +str(c) + "," + str(i)
            increUpdatePVB(board,r,c,i)
            tryMove = MRV_MCV_Search(board)
            if tryMove == False:
                board.set_value(r, c, 0)
                backUpdatePVB(board, r, c, i)
                continue
            else: return tryMove
        else: return False


fuckingNumCheck = 0
PVB = []
def tryMRV_MCV_Search(size, filename):
    #print size, filename
    global fuckingNumCheck
    global PVB
    fuckingNumCheck = 0
    board_1 = SudokuBoard(size ,parse_file(filename))
    PVB = updatePVB(board_1)
    #print board_1.CurrentGameboard
    PVB = updatePVB(board_1)
    solution = MRV_MCV_Search(board_1)
    if solution != False:
        pass # print solution.CurrentGameboard
    else:
        print "Shit!"        


def findMRV_MCV_LCV(board, PVB):
    MRV = board.BoardSize + 1
    MRVPos = [-1, -1]
    MRV_list = []
    MCV = 0
    for i in range(board.BoardSize):
        for j in range(board.BoardSize):
            if PVB[i][j] == 0:
                continue
            elif (len(PVB[i][j]) < MRV) or ((len(PVB[i][j]) == MRV) and (getMCV(board, i, j) > MCV)):
                MRVPos = [i, j]
                MRV_list = PVB[i][j]
                MRV = len(PVB[i][j])
                MCV = getMCV(board,i,j)
    #print MRV_list
    #print getLCV(board, MRVPos, MRV_list)
    return getLCV(board, MRVPos, MRV_list)

def getMCV(board, row, col):
    return len([n for n in getNeighbors(board, row, col) if board.CurrentGameboard[n[0]][n[1]] == 0])

def getLCV(board, MRVPos, MRV_list):
    row = MRVPos[0]
    col = MRVPos[1]
    return [MRVPos, [x[0] for x in  sorted([[v, getConstraintNum(board, MRVPos, v)] for v in MRV_list], key = (lambda x: x[1]))]] #sort by how many neighbors it would constraint

def getConstraintNum(board, MRVPos, v):
    row = MRVPos[0]
    col = MRVPos[1]
    # print [n for n in list(getNeighbors(board, row, col)) if  PVB[n[0]][n[1]] != 0 and v in PVB[n[0]][n[1]]]
    # for x in [n for n in list(getNeighbors(board, row, col)) if  PVB[n[0]][n[1]] != 0 and v in PVB[n[0]][n[1]]]:
    #     print PVB[x[0]][x[1]]
    return len([n for n in list(getNeighbors(board, row, col)) if  PVB[n[0]][n[1]] != 0 and v in PVB[n[0]][n[1]]])
    
def MRV_MCV_LCV_Search(board):
    global PVB
    global fuckingNumCheck
    fuckingNumCheck += 1
    if fuckingNumCheck % 1000 == 0:
        print fuckingNumCheck
        #printBoard(board)
    if iscomplete(board.CurrentGameboard):
        print "Yes, you did it!"
        print fuckingNumCheck
        return board # this prints the board
    else:
        MRV_list = findMRV_MCV_LCV(board,PVB)[1]
        MRVPos = findMRV_MCV_LCV(board,PVB)[0]
        # print "MRV list is " + str(MRV_list) + str(findMRV(board,PVB))
        if len(MRV_list) <= 0:
            return False
        r = MRVPos[0]
        c = MRVPos[1]
        # print MRVPos, MRV_list
        for i in MRV_list:
            board.set_value(r, c, i)
            #print "fill in " + str(r) + "," +str(c) + "," + str(i)
            increUpdatePVB(board,r,c,i)
            tryMove = MRV_MCV_LCV_Search(board)
            if tryMove == False:
                board.set_value(r, c, 0)
                backUpdatePVB(board, r, c, i)
                continue
            else: return tryMove
        else: return False


fuckingNumCheck = 0
PVB = []
def tryMRV_MCV_LCV_Search(size, filename):
    # print size, filename
    global fuckingNumCheck
    global PVB
    fuckingNumCheck = 0
    board_1 = SudokuBoard(size ,parse_file(filename))
    PVB = updatePVB(board_1)
    #print board_1.CurrentGameboard
    PVB = updatePVB(board_1)
    solution = MRV_MCV_LCV_Search(board_1)
    if solution != False:
        print solution
    else:
        print "Shit!"






board_1 = SudokuBoard(9 ,parse_file("c:/Users/crazydonkey200/Documents/GitHub/SudokuSolver/Puzzles/9_9.sudoku"))

PVB = updatePVB(board_1)
def printBoard(board):
    for row in board.CurrentGameboard:
        print row
    print "\n"


def test_on_puzzles(size):
    for i in range(1, 21):
        print "Number %d:" % i
        tryMRV_MCV_LCV_Search(size, "c:/Users/crazydonkey200/Documents/GitHub/SudokuSolver/Puzzles/" + str(size) + "x" + str(size) + "." + str(i) + ".sudoku")
        tryMRV_MCV_Search(size, "c:/Users/crazydonkey200/Documents/GitHub/SudokuSolver/Puzzles/" + str(size) + "x" + str(size) + "." + str(i) + ".sudoku")
        tryMRVSearch(size, "c:/Users/crazydonkey200/Documents/GitHub/SudokuSolver/Puzzles/" + str(size) + "x" + str(size) + "." + str(i) + ".sudoku")
        print "\n \n \n"

def test_on_this_puzzle(size, i):
    print "Number %d:" % i
    tryMRV_MCV_LCV_Search(size, "c:/Users/crazydonkey200/Documents/GitHub/SudokuSolver/Puzzles/" + str(size) + "x" + str(size) + "." + str(i) + ".sudoku")
    tryMRV_MCV_Search(size, "c:/Users/crazydonkey200/Documents/GitHub/SudokuSolver/Puzzles/" + str(size) + "x" + str(size) + "." + str(i) + ".sudoku")
    tryMRVSearch(size, "c:/Users/crazydonkey200/Documents/GitHub/SudokuSolver/Puzzles/" + str(size) + "x" + str(size) + "." + str(i) + ".sudoku")
    print "\n \n \n"                

def test_on_puzzles_MRV(size):
    for i in range(1, 21):
        tryMRV_MCV_Search(size, "c:/Users/crazydonkey200/Documents/GitHub/SudokuSolver/Puzzles/" + str(size) + "x" + str(size) + "." + str(i) + ".sudoku")
