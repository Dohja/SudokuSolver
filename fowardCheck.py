import math
import copy
import time
import random
import sudoku

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

class SudokuBoard:
	def __init__(self, size, board):
		self.BoardSize = size #the size of the board
		self.CurrentGameboard = board #the current state of the game board
		self.possibleValues = []
		for row in range(size):
			self.possibleValues.append([])
			for col in range(size):
				self.possibleValues[row].append([])
				for i in range(size):
		 			if isLegalMove(self, row, col, i): 
		 				self.possibleValues[row][col].append(i)
		# 		if self.CurrentGameboard[row][col]==0:
		# 			self.possibleValues[row].append(range(1,size+1))
		# 		else:
		# 			self.possibleValues[row].append([])

		# for row in range(self.BoardSize):
		# 	for col in range(self.BoardSize):
		# 		if self.CurrentGameboard[row][col] != 0:
		# 			value = self.CurrentGameboard[row][col]
		# 			for k in range(self.BoardSize):
		# 				try :
		# 					self.possibleValues[row][k].remove(value)
		# 				except ValueError:
		# 					pass
		# 				try :
		# 					self.possibleValues[k][col].remove(value)
		# 				except ValueError:
		# 					pass
		# 			for i,j in self.getQuadrant(row,col):
		# 				try :
		# 					self.possibleValues[i][j].remove(value)
		# 				except ValueError:
		# 					pass

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

	def iscomplete(self):
	    size = self.BoardSize
	    subsquare = int(math.sqrt(size))
	    #check each cell on the board for a 0, or if the value of the cell
	    #is present elsewhere within the same row, column, or square
	    for row in range(size):
	        for col in range(size):
	            if self.CurrentGameboard[row][col]==0:
	                return False
	            for i in range(size):
	                if ((self.CurrentGameboard[row][i] == self.CurrentGameboard[row][col]) and i != col):
	                    return False
	                if ((self.CurrentGameboard[i][col] == self.CurrentGameboard[row][col]) and i != row):
	                    return False
	            #determine which square the cell is in
	            SquareRow = row // subsquare
	            SquareCol = col // subsquare
	            for i in range(subsquare):
	                for j in range(subsquare):
	                    if((self.CurrentGameboard[SquareRow*subsquare + i][SquareCol*subsquare + j] == self.CurrentGameboard[row][col])
	                       and (SquareRow*subsquare + i != row) and (SquareCol*subsquare + j != col)):
	                        return False
	    return True

	def getQuadrant(self, row, col, size=None):
		if size:
			square = size
		else:
			square = int(math.sqrt(self.BoardSize))
		sq_row = (row // square)
		sq_col = (col // square)
		quadrant = []
		for i in range(square):
			for j in range(square):
				quadrant.append((square * sq_row + i,square * sq_col +j))
		return quadrant

	def set_value(self, row, col, value):
		self.CurrentGameboard[row][col]=value #add the value to the appropriate position on the board
		return SudokuBoard(self.BoardSize, self.CurrentGameboard) #return a new board of the same size with the value added

	def emptyPossibleValues(self):
		for i in range(self.BoardSize):
			for j in range(self.BoardSize):
				if self.possibleValues[i][j] != []:
					return False
		return True

	def forwardCheckSolve(self):
		for i in range(self.BoardSize):
			for j in range(self.BoardSize):
				if self.possibleValues[i][j]==[] and self.CurrentGameboard[i][j]==0:
					return False
		for i in range(self.BoardSize):
			for j in range(self.BoardSize):
				for k in range(0,len(self.possibleValues[i][j])):
					nextMove = self.possibleValues[i][j][k]
					nextState = self.set_value(i,j,nextMove)
					solution = nextState.forwardCheckSolve()
					if solution:
						return solution
					else: self.set_value(i, j, 0)

		if self.iscomplete():
			return self
		else:
			return False

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

def init_board( file_name ):
    board = parse_file(file_name)
    return SudokuBoard(len(board), board)

if __name__ == "__main__" :
	global count
	count = 0
	board = init_board('./Puzzles/4_4.sudoku')
	print board
	print board.forwardCheckSolve()



         