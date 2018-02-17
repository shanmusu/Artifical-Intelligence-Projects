import random

class Player:
  def __init__(self,n ,k):
    # counts stores how many tiles are in each column (initalised to 0)
    self.counts = [0] * int(k)
    #print(self.counts);
    self.board = [];
    self.rows = int(n);
    self.columns = int(k);
    self.whose_move = "userone";
    self.last_whose_move = [];
    self.last_which_row = [];
    self.last_which_column = [];
    self.player = 0;
    
    for rows_count in range(self.rows):
      rows_temp = [];
      for columns_count in range(self.columns):
        rows_temp.append(0);
      self.board.append(rows_temp);


  def name(self):
    return 'RANDOM'

  def make_move_initial(self, row, column):
    if self.whose_move == "userone":
      self.board[row][column] = 1;
      self.whose_move = "usertwo";
      self.player = 1;
      self.last_whose_move.append("userone");
      self.last_which_row.append(row);
      self.last_which_column.append(column);
          
    elif self.whose_move == "usertwo":
      self.board[row][column] = 2;
      self.whose_move = "userone";
      self.player = 0;
      self.last_whose_move.append("usertwo");
      self.last_which_row.append(row);
      self.last_which_column.append(column);

  def make_move(self, move):
    # every time a move is made the number of tiles in that column increases by one
    self.counts[move]+=1
    move_added = False;
    for rows_count in range(self.rows-1, -1, -1):
      if self.board[rows_count][move] == 0:
        if self.whose_move == "userone":
          self.board[rows_count][move] = 1;
          self.whose_move = "usertwo";
          self.player = 1;
          self.last_whose_move.append("userone");
          self.last_which_row.append(rows_count);
          self.last_which_column.append(move);
          
        elif self.whose_move == "usertwo":
          self.board[rows_count][move] = 2;
          self.whose_move = "userone";
          self.player = 0;
          self.last_whose_move.append("usertwo");
          self.last_which_row.append(rows_count);
          self.last_which_column.append(move);
          
        move_added = True;
        break;

  def get_move(self):
    # first we generate the moves, which is any column that isn't full (has less than 6 tiles)
    moves = []
    for i in range(0, self.columns):
      if self.counts[i] < self.columns:
        moves.append(i)
    # return a random legal move
    return random.choice(moves)
