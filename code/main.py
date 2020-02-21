# Fix OpenCv2 configuration error with ROS
import sys
sys.path.remove("/opt/ros/kinetic/lib/python2.7/dist-packages")

import bcd  #The Boustrophedon Cellular decomposition
import dfs  #THe Depth-first Search Algorithm
import cv2
from matplotlib import pyplot as plt

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
    print("Total cell number: ", len(cell_numbers))
    print("Cells: ", cell_numbers)
    print("Non-neighboor cells: ", non_neighboor_cell_numbers)
    

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
    cleaned = [] #Keeps cleaned cell numbers
    
    dfs.dfs(cleaned, graph, 1)
    
    print("Cleaned cell order ", cleaned)
    # Doesn't work --> Look at later, right now assume we have the graph 
    #calculate_neighboor_matrix(cell_numbers,cell_boundaries,non_neighboor_cell_numbers)

    # Just for convenience
    plt.show(block=False)
    plt.waitforbuttonpress(1)
    input("Please press any key to close all figures.")
    plt.close("all")
