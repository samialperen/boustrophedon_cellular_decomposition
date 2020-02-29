# Fix OpenCv2 configuration error with ROS
import sys
sys.path.remove("/opt/ros/kinetic/lib/python2.7/dist-packages")

import bcd  #The Boustrophedon Cellular decomposition
import dfs  #The Depth-first Search Algorithm
import bfs  #The Breadth First Search Algorithm
import move_boustrophedon # Uses output of bcd cells in order to move the robot
import exceptions

import cv2
import timeit


if __name__ == '__main__':
    
    # Read the original data
    original_map = cv2.imread("../data/main_example3.png")
    #original_map = cv2.imread("../data/example2.png")[:,0:350]
    
    # Show the original data
    fig1 = move_boustrophedon.plt.figure()
    move_boustrophedon.plt.imshow(original_map)
    move_boustrophedon.plt.title("Original Map Image")
    
    # We need binary image
    # 1's represents free space while 0's represents objects/walls
    if len(original_map.shape) > 2:
        print("Map image is converted to binary")
        single_channel_map = original_map[:, :, 0]
        _,binary_map = cv2.threshold(single_channel_map,127,1,cv2.THRESH_BINARY)

    # Call The Boustrophedon Cellular Decomposition function
    bcd_out_im, bcd_out_cells, cell_numbers, cell_boundaries, non_neighboor_cell_numbers = bcd.bcd(binary_map)
    # Show the decomposed cells on top of original map
    bcd.display_separate_map(bcd_out_im, bcd_out_cells)
    move_boustrophedon.plt.show(block=False)

    #print("Total cell number: ", len(cell_numbers))
    #print("Cells: ", cell_numbers)
    #print("Non-neighboor cells: ", non_neighboor_cell_numbers)
    #print("Cell boundaries: ", cell_boundaries)

    # Calculate optimum path using the depth first search
    # In the future, this graph should be calculated automatically using bcd outputs
    graph = {
        1: [2,3],
        2: [1,4],
        3: [1,4],
        4: [2,3,5,6],
        5: [4,7],
        6: [4,7],
        7: [5,6,8,9],
        8: [7,10],
        9: [7,10],
        10: [8,9,11,12],
        11: [10,13],
        12: [10,13],
        13: [11,12]
    }

    ############ DFS
    cleaned_DFS = [] #Keeps cleaned cell numbers in order
    iter_number = 1000
    starting_cell_number = move_boustrophedon.randint(1,len(cell_numbers))
    print("Starting cell number: ", starting_cell_number)
    exec_time_dfs = timeit.timeit('dfs.dfs(cleaned_DFS, graph, starting_cell_number)', \
        'from __main__ import dfs, cleaned_DFS, graph, starting_cell_number',number = iter_number)
    exec_time_dfs = exec_time_dfs/iter_number
    print("DFS Cleaned cells in order", cleaned_DFS)
    print("Execution time of dfs in seconds: ", exec_time_dfs)

    # Check the output of the DFS --> All cells should be visited!
    if (len(cell_numbers) != len(cleaned_DFS)):
        print("Total cell number: ", len(cell_numbers))
        print("Visited total cell number: ", len(cleaned_DFS))
        raise exceptions.DfsError("DFS couldn't find a path to visit all cells!")
    


    ######### BFS
    cleaned_BFS = [] #Keeps cleaned cell numbers in order
    iter_number = 1000
    #starting_cell_number = move_boustrophedon.randint(1,len(cell_numbers))
    print("Starting cell number: ", starting_cell_number)
    exec_time_bfs = timeit.timeit('bfs.bfs(cleaned_BFS, graph, starting_cell_number)', \
        'from __main__ import bfs, cleaned_BFS, graph, starting_cell_number',number = iter_number)
    exec_time_bfs = exec_time_bfs/iter_number
    print("BFS Cleaned cells in order", cleaned_BFS)
    print("Execution time of bfs in seconds: ", exec_time_bfs)

    # Check the output of the BFS --> All cells should be visited!
    if (len(cell_numbers) != len(cleaned_BFS)):
        print("Total cell number: ", len(cell_numbers))
        print("Visited total cell number: ", len(cleaned_BFS))
        raise exceptions.BfsError("BFS couldn't find a path to visit all cells!")
    
    ########## Add cost using distance between center of mass of cells

    
    
    ########## Path Tracking
    ### DFS
    iter_number = 1
    path_time_dfs = timeit.timeit('move_boustrophedon.track_paths(original_map,cleaned_DFS,cell_boundaries,non_neighboor_cell_numbers)', \
                                   'from __main__ import move_boustrophedon, \
                                   cleaned_DFS, original_map, cell_boundaries,non_neighboor_cell_numbers',number = iter_number)
    path_time_dfs = path_time_dfs/iter_number
    print("Total path tracking time of dfs in seconds: ", path_time_dfs)
    
    ### BFS
    iter_number = 1
    path_time_dfs = timeit.timeit('move_boustrophedon.track_paths(original_map,cleaned_BFS,cell_boundaries,non_neighboor_cell_numbers)', \
                                   'from __main__ import move_boustrophedon, \
                                   cleaned_BFS, original_map, cell_boundaries,non_neighboor_cell_numbers',number = iter_number)
    path_time_bfs = path_time_bfs/iter_number
    print("Total path tracking time of bfs in seconds: ", path_time_bfs)


    


 








    # Doesn't work --> Look at later, right now assume we have the graph 
    #calculate_neighboor_matrix(cell_numbers,cell_boundaries,non_neighboor_cell_numbers)




    # Just for convenience, show each plot at the same time at different plots
    move_boustrophedon.plt.waitforbuttonpress(1)
    input("Please press any key to close all figures.")
    move_boustrophedon.plt.close("all")
