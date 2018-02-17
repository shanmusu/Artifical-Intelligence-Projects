import board
import player
import random_player
import search
import random
import sys;


def mytest(n, k, moves_made):
  players = [player.Player(n,k),random_player.Player(n, k)]
  #random.shuffle(players)
  print(players[0].name() + " vs " + players[1].name())

  b = board.Board(n, k)

  initial_state = list(moves_made);
  initial_state_2D = zip(*[iter(initial_state)]*k)
  
  for rows in range(n):
    for columns in range(k):
      if initial_state_2D[rows][columns] != ".":
        b.make_move_initial(rows,columns);
        players[0].make_move_initial(rows,columns);
        players[1].make_move_initial(rows,columns);
      
  i = 0
  legal_moves = b.generate_moves()
  while not b.last_move_won() and len(legal_moves) > 0:
    print("Board state after ",players[i].name() ," move");
    print(b.__str__());
    move = players[i].get_move()
    #print("whose move ", players[i].name());
    players[0].make_move(move)
    players[1].make_move(move)
    b.make_move(move)
    i^=1
    legal_moves = b.generate_moves()
  if b.last_move_won():
    print("VICTORY FOR PLAYER " + players[i].name())
  else:
    print("DRAW")

n = sys.argv[1];
k = sys.argv[2];
moves_made = sys.argv[3];
mytest(int(n), int(k), moves_made)

