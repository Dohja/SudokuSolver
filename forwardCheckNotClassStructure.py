import math
import copy
import time
import random
import sudoku

count = 0

def forwardCheckSolve(board):
    global count
    possibleValues = findPossibleValues(board)
    for i in range(board.BoardSize):
        for j in range(board.BoardSize):
            if possibleValues[i][j]==[] and board.CurrentGameboard[i][j]==0:
                count = 0
                return False
    for i in range(board.BoardSize):
        for j in range(board.BoardSize):
            for k in possibleValues[i][j]:
                count += 1
                nextState = board.set_value(i,j,k)
                solution = forwardCheckSolve(nextState)
                if solution: return solution
                else: board.set_value(i, j, 0)
    if iscomplete(board.CurrentGameboard):
        print "this took us " + str(count) + " consistency checks"
        count = 0
        return board
    else: return False

def getQuadrant(board, row, col):
    square = int(math.sqrt(board.BoardSize))
    sq_row = (row // square)
    sq_col = (col // square)
    quadrant = []
    for i in range(square):
        for j in range(square):
            quadrant.append((square * sq_row + i,square * sq_col +j))
    return quadrant

def isLegalMove(board, row, col, val):
    if board.CurrentGameboard[row][col] != 0: 
        return False
    else:
        for i in range(board.BoardSize):
            if (board.CurrentGameboard[row][i] == val or board.CurrentGameboard[i][col] == val): 
                return False
        for square in getQuadrant(board, row, col):
            r = square[0]
            c = square[1]
            if board.CurrentGameboard[r][c] == val: 
                return False
    return True

def findPossibleValues(board):
    possibleValues = []
    for row in range(board.BoardSize):
        possibleValues.append([])
        for col in range(board.BoardSize):
            possibleValues[row].append([])
            for i in range(1, board.BoardSize+1):
                if isLegalMove(board, row, col, i):
                    possibleValues[row][col].append(i)
    return possibleValues
                    
class SudokuBoard:

    #the constructor for the SudokuBoard
    def __init__(self, size, board):
      self.BoardSize = size #the size of the board
      self.CurrentGameboard= board #the current state of the game board

    #This function will create a new sudoku board object with
    #with the input value placed on the GameBoard row and col are
    #both zero-indexed
    def __repr__(self):
        square = int(math.sqrt(self.BoardSize))
        mainString = ""
        padding = 3
        for i in range(self.BoardSize):
            if (i%square) == 0:
                mainString = mainString + "\n" + ("-".center(padding)*(self.BoardSize+square-1))

            string = str(self.CurrentGameboard[i][0]).center(padding)
            for j in range(1,self.BoardSize):
                if ((j%square)) == 0:
                    string = string + "|".center(padding)
                string = string + str(self.CurrentGameboard[i][j]).center(padding)
            mainString = mainString + "\n" + string
        mainString = "\n" + mainString + "\n" + ("-".center(padding)*(self.BoardSize+square-1))
        return mainString
    
    def __str__(self):
        square = int(math.sqrt(self.BoardSize))
        mainString = ""
        padding = 3
        for i in range(self.BoardSize):
            if (i%square) == 0:
                mainString = mainString + "\n" + ("-".center(padding)*(self.BoardSize+square-1))
            string = str(self.CurrentGameboard[i][0]).center(padding)
            for j in range(1,self.BoardSize):
                if ((j%square)) == 0:
                    string = string + "|".center(padding)
                string = string + str(self.CurrentGameboard[i][j]).center(padding)
            mainString = mainString + "\n" + string
        mainString = "\n" + mainString + "\n" + ("-".center(padding)*(self.BoardSize+square-1))
        return mainString
    
    def set_value(self, row, col, value):
        self.CurrentGameboard[row][col]=value #add the value to the appropriate position on the board
        return SudokuBoard(self.BoardSize, self.CurrentGameboard) #return a new board of the same size with the value added
    


# parse_file
#this function will parse a sudoku text file (like those posted on the website)
#into a BoardSize, and a 2d array [row,col] which holds the value of each cell.
# array elements witha value of 0 are considered to be empty

def parse_file(filename):
    f = open(filename, 'r')
    BoardSize = int( f.readline())
    NumVals = int(f.readline())

    #initialize a blank board
    board= [ [ 0 for i in range(BoardSize) ] for j in range(BoardSize) ]

    #populate the board with initial values
    for i in range(NumVals):
        line = f.readline()
        chars = line.split()
        row = int(chars[0])
        col = int(chars[1])
        val = int(chars[2])
        board[row-1][col-1]=val
    
    return board


#takes in an array representing a sudoku board and tests to
#see if it has been filled in correctly
def iscomplete( BoardArray ):
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    #check each cell on the board for a 0, or if the value of the cell
    #is present elsewhere within the same row, column, or square
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col]==0:
                return False
            for i in range(size):
                if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
                    return False
                if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
                    return False
            #determine which square the cell is in
            SquareRow = row // subsquare
            SquareCol = col // subsquare
            for i in range(subsquare):
                for j in range(subsquare):
                    if((BoardArray[SquareRow*subsquare + i][SquareCol*subsquare + j] == BoardArray[row][col])
                       and (SquareRow*subsquare + i != row) and (SquareCol*subsquare + j != col)):
                        return False
    return True

# creates a SudokuBoard object initialized with values from a text file like those found on the course website
def init_board( file_name ):
    board = parse_file(file_name)
    return SudokuBoard(len(board), board)


########## NEW CODE

def isLegalMove(board, row, col, val):
    if board.CurrentGameboard[row][col] != 0: 
        return False
    else:
        for i in range(board.BoardSize):
            if (board.CurrentGameboard[row][i] == val or board.CurrentGameboard[i][col] == val): 
                return False
        for square in getQuadrant(board, row, col):
            r = square[0]
            c = square[1]
            if board.CurrentGameboard[r][c] == val: 
                return False
    return True

def getQuadrant(board, row, col):
    square = int(math.sqrt(board.BoardSize))
    sq_row = (row // square)
    sq_col = (col // square)
    quadrant = []
    for i in range(square):
        for j in range(square):
            quadrant.append((square * sq_row + i,square * sq_col +j))
    return quadrant

         
