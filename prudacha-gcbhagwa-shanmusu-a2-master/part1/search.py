import board
import random


def perft(board, depth):
  total_nodes_visited = 0;

  #gets the next possible moves allowed to take.
  available_moves = board.generate_moves();

  should_end = (depth == 0) or (len(available_moves) == 0);
  if should_end: 
    return 1;
  else:
    for available_moves_temp in available_moves:
      board.make_move(available_moves_temp);
      #check if the last made move was a win so that it indicates the end of the tree.
      if board.last_move_won():
        total_nodes_visited += 1;
      else:
        #recurse for the next depth
        total_nodes_visited += perft(board, depth-1);
      board.unmake_last_move();
  return total_nodes_visited;

def alpha_beta_pruning(board, depth, alpha ,beta, player_temp):
  if depth == 0:
    if board.last_move_won(): 
      if board.player == player_temp:
        return 1;
      else:
        return -1;
    else:
      return 0;
  else:
    #gets the next possible moves allowed to take.
    total_nodes_visited = board.generate_moves();
    for total_nodes_visited_temp in total_nodes_visited:
      board.make_move(total_nodes_visited_temp);
      
      #prune and set the alpha beta values based on the depth leaves.
      result = alpha_beta_pruning(board, depth-1, alpha, beta, player_temp);
      if board.player == player_temp:
        if alpha < result:
          alpha = result;
      else:
        if beta > result:
          beta = result;
      board.unmake_last_move();
      if beta <= alpha:
        break;

    if board.player == 0:
      return alpha;
    else:
      return beta;

def find_win(board, depth):
  total_nodes_visited = board.generate_moves();
  results = [];
  final_result = None;

  player_temp = 0 if board.player == 1 else 1;

  for total_nodes_visited_temp in total_nodes_visited:
    board.make_move(total_nodes_visited_temp);
    #print(board);
    #prune and set the alpha beta values based on the depth leaves.
    result = alpha_beta_pruning(board, depth-1, -2, 2, player_temp);
   
    if final_result is None and result == 1:
      final_result = "WIN BY PLAYING "+str(total_nodes_visited_temp);

    results.append(result);
    board.unmake_last_move();
    
  if final_result is not None:
    return final_result;
  if max(results) == 0:
    return "NO FORCED WIN IN %d MOVES" % depth;
  else:
    return "ALL MOVES LOSE";

