
from AnimatedTetris import *
from SimpleTetris import *
from kbinput import *
from TetrisGame import *
import time, sys
from copy import deepcopy
from random import randint

# Problem Description - Simple version

# The maximum score achieved was 716, and followed by that was 669. This is still based on the random distribution, so it takes a few re-runs to work as expected.
# The picture proofs are uploaded in the directory for your consideration.
# As per our trails, every once in seven runs, this program produces a score of above 200.

# Somes ideas were taken and reduced to the form that fits the problem from the following link : http://www.ryanheise.com/tetris/tetris_stacking.html
# The initial values and the weighing ideas are taken and modeled to fit the current problem statement : http://bayes.cs.ucla.edu/TRIBUTE/part1-heuristics-linked.pdf

# The height_computation() function computes for each position on the board and if there is a block at that position, it checks whether the 
# height of the current column is zero or not. If zero, the height of each column is calcualted by subtracting the current row from the 
# total length of the board.

# The row_computation() function computes the horizontal version of height_computation() function. For each line, if there is no block in that row,
# the variable lines is incremented.

# The gap_computation() function filters the gaps but removing the states on the board that are filled.

# The weighted_computation() is a function that returns the value of the compute variable and compares it with the original or the initial value. These weights were
# tested for different values and the numbers that produce the best output were used, and they were initialized statically. 

# The intial values were chosen based on the ideas from the links above, and stored in a dictionary. Now, for each position, if there is not block, we check for collision.
# If there is no collison, we compute the current_value and we do as said in the above comment. At the end of each, the rotation factor, or the variable rotate_factor
# is incremented and the piece is rotated by an angle of 90 degrees.

# In the output_moves string, we first find the number of times the piece has to rotate because this cannot be done abruptly after moving the piece left or right.
# Then the piece can be moved to either left or right based on the values in the dictionary. Then the string of total moves is returned.

# The initial compute value was tested with various values, but the values ranging between 8000 to 9000 seem to give a good output. So, it was randomized.  


columns = 10

weights = {'height' : 1.00, 'gap' : 0.31, 'row' : -1.01}

# Function to compute height of each column
def height_computation(board):
    height = [0] * columns
    for r in range(0, len(board)):
        for c in range(0, columns):
            if board[r][c] == 'x':
                if  height[c] == 0:
                    height[c] = len(board) -  r
    return sum(height)

# function to compute the number of complete rows
def row_computation(board):
    lines = 0
    for r in range(0, len(board)):
        lines += 1
        for c in range(0, columns):
            if board[r][c] == ' ':
                lines -= 1
                break
    return lines

# function to complete the gaps 
def gap_computation(board):
    gaps = 0
    for c in range(0, columns):
        filled = 0
        for r in range(0, len(board)):
            if board[r][c] == 'x':
                filled = 1
            elif board[r][c] == ' ' and filled == 1:
                gaps += 1
    return gaps

# Instrad of uniformly weighing them, I weighed them differently but validating values
def weighted_computation((board, score)):
    return (weights['height'] * height_computation(board))  + (weights['gap'] * gap_computation(board)) + (weights['row'] * row_computation(board))

class HumanPlayer:
    def get_moves(self, tetris):
        print "Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\nThen press enter. E.g.: bbbnn\n"
        moves = raw_input()
        return moves

    def control_game(self, tetris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": tetris.left, "n": tetris.rotate, "m": tetris.right, " ": tetris.down }
            commands[c]()

#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#
class ComputerPlayer:
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. tetris is an object that lets you inspect the board, e.g.:
    #   - tetris.col, tetris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - tetris.get_piece() is the current piece, tetris.get_next_piece() is the next piece after that
    #   - tetris.left(), tetris.right(), tetris.down(), and tetris.rotate() can be called to actually
    #     issue game commands
    #   - tetris.get_board() returns the current state of the board, as a list of strings.
    #


    def get_moves(self, tetris):
        # super simple current algorithm: just randomly move left, right, and rotate a few times
        b = deepcopy(tetris)
        board = b.get_board()
   	init_score = 0
        init_dict = {'compute' : randint(8000, 9000), 'row' : 20, 'col' : 20, 'rot' : 0}
       	rotate_factor = 0
        
	while (rotate_factor < 4):
            for r in range(0, len(b.get_board())):
                for c in range(0, columns):
                    if board[r][c] != 'x':
                        if not (TetrisGame.check_collision((board, init_score), b.piece, r, c)):
                    	    current_compute = weighted_computation(TetrisGame.place_piece((board, init_score), b.piece, r, c) )
                            
                            if current_compute <= init_dict['compute']:
                                init_dict['compute'] = current_compute; init_dict['row'] = r; init_dict['col'] = c; init_dict['rot'] = rotate_factor;
	    rotate_factor += 1
            b.piece = TetrisGame.rotate_piece(b.piece, 90)
       
	output_moves = ''
	
	# Adding 'Rotation' factor
        if init_dict['rot'] > 0:
            for i in range(0, init_dict['rot']):
                output_moves += 'n'

	# Adding 'Left' Factor
        if tetris.col - init_dict['col'] <= 0:
            for i in range(0, abs(tetris.col -  init_dict['col'])):
                output_moves += 'm'
        else:
        # Adding right factor
      	    for i in range(0, tetris.col - init_dict['col']):
                output_moves += 'b'

        return output_moves

        # return random.choice("mnb") * random.randint(1, 10)
       
    # This is the version that's used by the animated version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "tetris" object to control the movement. In particular:
    #   - tetris.col, tetris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - tetris.get_piece() is the current piece, tetris.get_next_piece() is the next piece after that
    #   - tetris.left(), tetris.right(), tetris.down(), and tetris.rotate() can be called to actually
    #     issue game commands
    #   - tetris.get_board() returns the current state of the board, as a list of strings.
    #
    def control_game(self, tetris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:
            time.sleep(0.1)

            board = tetris.get_board()
            column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [100,] ) for c in range(0, len(board[0]) ) ]
            index = column_heights.index(max(column_heights))

            if(index < tetris.col):
                tetris.left()
            elif(index > tetris.col):
                tetris.right()
            else:
                tetris.down()


###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print "unknown player!"

    if interface_opt == "simple":
        tetris = SimpleTetris()
    elif interface_opt == "animated":
        tetris = AnimatedTetris()
    else:
        print "unknown interface!"

    tetris.start_game(player)

except EndOfGame as s:
    print "\n\n\n", s

