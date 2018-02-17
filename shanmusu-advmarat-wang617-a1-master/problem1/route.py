#A* is the best algorithm for finding the optimal path given the heuristic function is correct.
#Heuristic function is the straight line distance between the current node and the goal node.
#for our assignment IDS is the fastest algoritm
#DFS is the most efficient algorithm in terms of memory. 
import Assignment_two_final_mapSearch_BFS;
import Assignment_two_final_mapSearch_DFS;
import Assignment_two_final_mapSearch_Astar;
import Assignment_two_final_mapSearch_IDS;
import sys;

if sys . argv [ 4 ].lower() == "bfs":
    Assignment_two_final_mapSearch_BFS.input_function(sys . argv [ 1 ], sys . argv [ 2 ], sys . argv [ 3 ]);

    Assignment_two_final_mapSearch_BFS.file_reading();

    Assignment_two_final_mapSearch_BFS.search_algorithm();

elif sys . argv [ 4 ].lower() == "dfs":
    Assignment_two_final_mapSearch_DFS.input_function(sys . argv [ 1 ], sys . argv [ 2 ], sys . argv [ 3 ]);

    Assignment_two_final_mapSearch_DFS.file_reading();

    Assignment_two_final_mapSearch_DFS.search_algorithm();

elif sys . argv [ 4 ].lower() == "astar":
    Assignment_two_final_mapSearch_Astar.input_function(sys . argv [ 1 ], sys . argv [ 2 ], sys . argv [ 3 ]);

    Assignment_two_final_mapSearch_Astar.file_reading();

    Assignment_two_final_mapSearch_Astar.search_algorithm();

elif sys . argv [ 4 ].lower() == "ids":
    Assignment_two_final_mapSearch_IDS.input_function(sys . argv [ 1 ], sys . argv [ 2 ], sys . argv [ 3 ]);

    Assignment_two_final_mapSearch_IDS.file_reading();

    Assignment_two_final_mapSearch_IDS.search_algorithm();
    
