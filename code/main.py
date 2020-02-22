# Fix OpenCv2 configuration error with ROS
import sys
sys.path.remove("/opt/ros/kinetic/lib/python2.7/dist-packages")

import bcd  #The Boustrophedon Cellular decomposition
import dfs  #The Depth-first Search Algorithm
import move_boustrophedon # Uses output of bcd cells in order to move the robot

import cv2
from matplotlib import pyplot as plt
import timeit

if __name__ == '__main__':
    
    # Read the original data
    original_map = cv2.imread("../data/example2.png")
    #original_map = cv2.imread("../data/example2.png")[:,0:350]
    
    # Show the original data
    fig1 = plt.figure()
    plt.imshow(original_map)
    plt.title("Original Map Image")
    
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

    # DFS
    cleaned = [] #Keeps cleaned cell numbers
    iter_number = 1000
    exec_time_dfs = timeit.timeit('dfs.dfs(cleaned, graph, 1)', 'from __main__ import dfs, cleaned, graph',number = iter_number)
    exec_time_dfs = exec_time_dfs/iter_number
    print("Cleaned cells in order ", cleaned)
    print("Execution time of dfs in seconds: ", exec_time_dfs)

    # Check the output of the DFS --> All cells should be visited!
    if (len(cell_numbers) != len(cleaned)):
        print("DFS couldn't find a path to visit all cells!")
        print("Total cell number: ", len(cell_numbers))
        print("Visited total cell number: ", len(cleaned))
        #break # TODO: Write something to raise error!

    move_boustrophedon.track_paths(original_map,cleaned,cell_boundaries,non_neighboor_cell_numbers)


    # BFS


    # Add cost using distance between center of mass of cells



    # Doesn't work --> Look at later, right now assume we have the graph 
    #calculate_neighboor_matrix(cell_numbers,cell_boundaries,non_neighboor_cell_numbers)

    # Just for convenience
    plt.show(block=False)
    plt.waitforbuttonpress(1)
    input("Please press any key to close all figures.")
    plt.close("all")
