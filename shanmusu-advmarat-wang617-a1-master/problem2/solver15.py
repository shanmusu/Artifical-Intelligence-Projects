#Solves the 15-puzzle
#function cost_to_goal(matrix) : heuristic function based on Manhattan distance. Accepts board as input and calculates total cost to goal state.
#shift_tile(matrix) : accepts a board config as input and gives all possible combinations after moving tiles L , R , U , D
#Solution function uses priority queue to choose positions with lowest cost to goal.
#Using python libraries for using deepcopy() function.
#Using heapq implenentation by python for priority queue.
import sys
import copy
import heapq
file = sys.argv[1] 
file_op = open(file)
matrix2 = file_op.read().split("\n",4)
matrix = [[],[],[],[]]
matrix = [matrix2[i].split() for i in range(0,4)]
matrix = [[int(element) for element in inner_list] for inner_list in matrix]

def cost_to_goal(matrix):
	cost = x = y = 0
	for i in range(0,4):
		for j in range(0,4):
			if matrix[i][j] == (i*4)+j+1 or matrix[i][j] == 0:
				cost += 0
			else:
				x = (matrix[i][j]-1)/4
				y = (matrix[i][j]-1)%4
				cost += (abs(i-x)+abs(j-y))
	return cost

def shift_tile(matrix):
	mat1 = copy.deepcopy(matrix)

	lst = []
	for i in range(0,4):
		for j in range(0,4):
			if matrix[i][j] == 0:
				x = i
				y = j

				mat1[x][y] , mat1[x][y-1] = mat1[x][y-1] , mat1[x][y] #R
				lst.append(mat1)
				mat1 = copy.deepcopy(matrix)
				mat1[x][y] , mat1[x][(y+1)%4] = mat1[x][(y+1)%4] , mat1[x][y] #L
				lst.append(mat1)
				mat1 = copy.deepcopy(matrix)
				mat1[x][y] , mat1[(x+1)%4][y] = mat1[(x+1)%4][y] , mat1[x][y] #U
				lst.append(mat1)
				mat1 = copy.deepcopy(matrix)
				mat1[x][y] , mat1[x-1][y] = mat1[x-1][y] , mat1[x][y]  #D
				lst.append(mat1)

	return lst

def return_move(index):
	if index == 0:
		return "R"
	elif index == 1:
		return "L"
	elif index == 2:
		return "U"
	else:
		return "D"
visited = []
moves = []
def solution(matrix):
	pririty_queue = []
	initial_cost = cost_to_goal(matrix)
	prev_matrix = []
	heapq.heappush(pririty_queue,[initial_cost,matrix,""])
	while len(pririty_queue) > 0:
		ls = []
		lst2 = []
		k = heapq.heappop(pririty_queue)
		if cost_to_goal(k[1]) == 0:
			return k[1]
		else:
			prev_matrix.append(k[1])
			moves.append(k[2])
			lst2 = shift_tile(k[1])
			for x in range(0,len(lst2)):
				ls.append(cost_to_goal(lst2[x]))
			for i in range(0,len(lst2)):
				if lst2[i] not in prev_matrix:
					heapq.heappush(pririty_queue,[ls[i],lst2[i],return_move(i)])
	return False				


print solution(matrix)
print "\n"
del moves[0]
print(" ".join(x for x in moves))