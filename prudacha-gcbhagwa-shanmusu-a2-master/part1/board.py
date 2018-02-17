# makke changes to the value n and k
class Board:
  def __init__(self, n ,k):
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

  def generate_moves(self):
    possible_moves = [];
    possible_moves_column = [];
    
    for columns_count in range(0, self.columns , 1):
      for rows_count in range(0, self.rows, 1):
        if self.board[rows_count][columns_count] == 0:
          possible_moves.append(str(rows_count) + str(columns_count));
          possible_moves_column.append(columns_count);
        
    return possible_moves_column;
  
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
      
  def unmake_last_move(self):
    if len(self.last_whose_move) > 0 and len(self.last_which_row) > 0 and len(self.last_which_column) > 0:
      self.board[self.last_which_row[len(self.last_which_row) - 1]][self.last_which_column[len(self.last_which_column) - 1]] = 0;
      self.whose_move = self.last_whose_move[len(self.last_whose_move) - 1];
      self.last_whose_move.pop();
      if self.player == 0:
        self.player = 1;
      else:
        self.player = 0;
      self.last_which_row.pop();
      self.last_which_column.pop();
      #print("Move undo done");
    
  def last_move_won(self):
    #print(len(self.last_which_row) -1);
    if len(self.last_whose_move) > 0:
      last_rowmove_made = self.last_which_row[len(self.last_which_row) - 1];
      last_columnmove_made = self.last_which_column[len(self.last_which_column) - 1];
      last_whosemove_made = self.last_whose_move[len(self.last_whose_move) - 1];
      last_whosemove_made_number = -1;

      if last_whosemove_made == "userone":
        last_whosemove_made_number = 1;
      elif last_whosemove_made == "usertwo":
        last_whosemove_made_number = 2;

      #check the verticals if there is a possibility for a win.
      vertical_streak = 0;
      for rows_count in range(last_rowmove_made + (self.rows -1), last_rowmove_made - self.rows , -1):
        if rows_count >= 0 and rows_count <= (self.rows-1):
          if self.board[rows_count][last_columnmove_made] == last_whosemove_made_number:
            vertical_streak += 1;
            if vertical_streak == self.rows:
              break;
          else:
            vertical_streak = 0;

      if vertical_streak == self.rows:
        return True;

      #check the horizontal streak if there is a possibility for a win.
      horizontal_streak = 0;
      for columns_count in range(last_columnmove_made - (self.rows-1), last_columnmove_made + self.rows, 1):
        if columns_count >= 0 and columns_count <= (self.columns-1):
          if self.board[last_rowmove_made][columns_count] == last_whosemove_made_number:
            horizontal_streak += 1;
            if horizontal_streak == self.rows:
              break;
          else:
            horizontal_streak = 0;
      
      if horizontal_streak == self.rows:
        return True;

      #check the diagonal streak if there is a possibility for a win. - diagonal left to right
      diagonal_left_to_right_streak = 0;
      columns_count = last_columnmove_made - (self.rows-1);
      
      for rows_count in range(last_rowmove_made + (self.rows-1), last_rowmove_made - self.rows, -1):
        if rows_count >=0 and rows_count <= (self.rows-1) and columns_count >=0 and columns_count <= (self.columns-1):
          if self.board[rows_count][columns_count] == last_whosemove_made_number:
            diagonal_left_to_right_streak += 1;
            if diagonal_left_to_right_streak == self.rows:
              break;
          else:
            diagonal_left_to_right_streak = 0;
        columns_count += 1;

      if diagonal_left_to_right_streak == self.rows:
        return True;

      #check the diagonal streak if there is a posssibility for a win - diagonal right to left.
      diagonal_right_to_left_streak = 0;
      columns_count = last_columnmove_made - (self.rows-1);

      for rows_count in range(last_rowmove_made - (self.rows-1), last_rowmove_made + self.rows, 1):
        if rows_count >=0 and rows_count <= (self.rows-1) and columns_count >=0 and columns_count <= (self.columns-1):
          if self.board[rows_count][columns_count] == last_whosemove_made_number:
            diagonal_right_to_left_streak += 1;
            if diagonal_right_to_left_streak == self.rows:
              break;
          else:
            diagonal_right_to_left_streak = 0;
        columns_count += 1;

      if diagonal_right_to_left_streak ==  self.rows:
        return True;
      else:
        return False;
    else:
      return False;
  
  def __str__(self):
    print_string = "";
    for rows in range(self.rows):
      column_string = "";
      for columns in range(self.columns):
        if self.board[rows][columns] == 0:
          column_string = column_string + ".";
        elif self.board[rows][columns] == 1:
          column_string = column_string + "w";
        elif self.board[rows][columns] == 2:
          column_string = column_string + "b";
      print_string = print_string + column_string;
      
    return str(print_string);





