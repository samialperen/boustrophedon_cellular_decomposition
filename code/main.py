# Fix OpenCv2 configuration error with ROS
import sys
sys.path.remove("/opt/ros/kinetic/lib/python2.7/dist-packages")

# Import necessary libraries
import numpy as np
import cv2
from PIL import Image
from matplotlib import pyplot as plt
import matplotlib
from typing import Tuple, List
import random
import itertools


Slice = List[Tuple[int, int]]


def calc_connectivity(slice: np.ndarray) -> Tuple[int, Slice]:
    """
    Calculates the connectivity of a slice and returns the connected area of ​​the slice.

    Args:
        slice: rows. A slice of map.

    Returns:
        The connectivity number and connectivity parts.
        connectivity --> total number of connected parts

    Examples:
        >>> data = np.array([0,0,0,0,1,1,1,0,1,0,0,0,1,1,0,1,1,0])
        >>> print(calc_connectivity(data))
        (4, [(4, 7), (8, 9), (12, 14), (15, 17)])
        (4,7) --> 4 is the point where connectivity is started
              --> 7 is the point where it finished
    """
    connectivity = 0
    last_data = 0
    open_part = False
    connective_parts = []
    for i, data in enumerate(slice):
        if last_data == 0 and data == 1:
            open_part = True
            start_point = i
        elif last_data == 1 and data == 0 and open_part:
            open_part = False
            connectivity += 1
            end_point = i
            connective_parts.append((start_point, end_point))

        last_data = data
    return connectivity, connective_parts


def get_adjacency_matrix(parts_left: Slice, parts_right: Slice) -> np.ndarray:
    """
    Get adjacency matrix of 2 neighborhood slices.

    Args:
        slice_left: left slice
        slice_right: right slice

    Returns:
        [L, R] Adjacency matrix.
    """
    adjacency_matrix = np.zeros([len(parts_left), len(parts_right)])
    for l, lparts in enumerate(parts_left):
        for r, rparts in enumerate(parts_right):
            if min(lparts[1], rparts[1]) - max(lparts[0], rparts[0]) > 0:
                adjacency_matrix[l, r] = 1

    return adjacency_matrix

def remove_duplicates(in_list):
    """
        This function removes duplicates in the input list, where
        input list is composed of unhashable elements
        Example:
            in_list = [[1,2],[1,2],[2,3]]
            output = remove_duplicates(in_list)
            output --> [[1,2].[2,3]]
    """
    out_list = []
    in_list.sort()
    out_list = list(in_list for in_list,_ in itertools.groupby(in_list))
    #print("input_list: ", in_list)
    #print("output list: ",out_list)
    return out_list

def bcd(erode_img: np.ndarray) -> Tuple[np.ndarray, int]:
    """
    Boustrophedon Cellular Decomposition

    Args:
        erode_img: [H, W], eroded map. The pixel value 0 represents obstacles and 1 for free space.

    Returns:
        [H, W], separated map. The pixel value 0 represents obstacles and others for its' cell number.
        current_cell and seperate_img is for display purposes --> which is used to show
        decomposed cells into a separate figure
        all_cell_numbers --> contains all cell index numbers
        cell_boundaries --> contains all cell boundary coordinates (only y coordinate)
        non_neighboor_cells --> contains cell index numbers of non_neighboor_cells, i.e.
        cells which are separated by the objects
    """
    
    assert len(erode_img.shape) == 2, 'Map should be single channel.'
    last_connectivity = 0
    last_connectivity_parts = []
    current_cell = 1
    current_cells = []
    separate_img = np.copy(erode_img)
    cell_boundaries = {}
    non_neighboor_cells = []

    for col in range(erode_img.shape[1]):
        current_slice = erode_img[:, col]
        connectivity, connective_parts = calc_connectivity(current_slice)
        
        if last_connectivity == 0:
            current_cells = []
            for i in range(connectivity): #slice intersects with the object for the first time
                current_cells.append(current_cell)
                current_cell += 1 # we are creating different cells on the same column
                                  # which are seperated by the objects
        elif connectivity == 0:
            current_cells = []
            continue
        else:
            adj_matrix = get_adjacency_matrix(last_connectivity_parts, connective_parts)
            new_cells = [0] * len(connective_parts)

            for i in range(adj_matrix.shape[0]):
                if np.sum(adj_matrix[i, :]) == 1:
                    new_cells[np.argwhere(adj_matrix[i, :])[0][0]] = current_cells[i]
                # If a previous part is connected to multiple parts this time, it means that IN has occurred.
                elif np.sum(adj_matrix[i, :]) > 1: #left slice is connected to more than one part of right slice
                    for idx in np.argwhere(adj_matrix[i, :]):
                        new_cells[idx[0]] = current_cell
                        current_cell = current_cell + 1

            for i in range(adj_matrix.shape[1]):
                # If a part of this time is connected to the last multiple parts, it means that OUT has occurred.
                if np.sum(adj_matrix[:, i]) > 1: #right slice is connected to more than one part of left slice
                    new_cells[i] = current_cell
                    current_cell = current_cell + 1
                # If this part of the part does not communicate with any part of the last time, it means that it happened in
                elif np.sum(adj_matrix[:, i]) == 0:
                    new_cells[i] = current_cell
                    current_cell = current_cell + 1
            current_cells = new_cells

        # Draw the partition information on the map.
        for cell, slice in zip(current_cells, connective_parts):
            #print("Debug")
            #print(current_cells, connective_parts)
            separate_img[slice[0]:slice[1], col] = cell
        
            # print('Slice {}: connectivity from {} to {}'.format(col, last_connectivity, connectivity))
        last_connectivity = connectivity
        last_connectivity_parts = connective_parts

        #print("Debug")
        #print(current_cells,connective_parts)
        
        #print("Current cell: ", current_cell)
        if len(current_cells) == 1: #no object in this cell
            cell_index = current_cell -1  # cell index starts from 1
            cell_boundaries.setdefault(cell_index,[])
            cell_boundaries[cell_index].append(connective_parts)
        elif len(current_cells) > 1: #cells separated by the object
            # cells separated by the objects are not neighbor to each other
            non_neighboor_cells.append(current_cells)
            # non_neighboor_cells will contain many duplicate values, but we 
            # will get rid of duplicates at the end

            # in this logic, all other cells must be neighboor to each other
            # if their cell number are adjacent to each other
            # like cell1 is neighboor to cell2

            for i in range(len(current_cells)):
                # current cells list doesn't need cell -1 operation 
                # it is already in the proper form
                cell_index = current_cells[i]
                # connective_parts and current_cells contain more than one
                # cell info which are separated by the object ,so we are iterating
                # with the for loop to reach all the cells
                cell_boundaries.setdefault(cell_index,[])
                cell_boundaries[cell_index].append(connective_parts[i])
     
    # Cell 1 is the left most cell and cell n is the right most cell
    # where n is the total cell number
    all_cell_numbers = cell_boundaries.keys()
    non_neighboor_cells = remove_duplicates(non_neighboor_cells)
   
    """
    # Debug
    print("Keys: ",cell_boundaries.keys())
    key1 = list(cell_boundaries.keys())[0]
    print("Key1: ", key1)
    print("Key2 value: ", cell_boundaries.get(key1))
    
    key2 = list(cell_boundaries.keys())[1]
    print("Key2: ", key2)
    print("Key2 value: ", cell_boundaries.get(key2))
    
    key3 = list(cell_boundaries.keys())[2]
    print("Key3: ", key3)
    print("Key3 value: ", cell_boundaries.get(key3))
    
    key4 = list(cell_boundaries.keys())[3]
    print("Key4: ", key4)
    print("Key4 value: ", cell_boundaries.get(key4))
    
    key5 = list(cell_boundaries.keys())[4]
    print("Key5: ", key5)
    print("Key5 value: ", cell_boundaries.get(key5))
    
    key6 = list(cell_boundaries.keys())[5]
    print("Key6: ", key6)
    print("Key6 value: ", cell_boundaries.get(key6))
    
    key7 = list(cell_boundaries.keys())[6]
    print("Key7: ", key7)
    print("Key7 value: ", cell_boundaries.get(key7))
    """
    
    return separate_img, current_cell, all_cell_numbers, cell_boundaries, non_neighboor_cells


def display_separate_map(separate_map, cells):
    display_img = np.empty([*separate_map.shape, 3], dtype=np.uint8)
    random_colors = np.random.randint(0, 255, [cells, 3])
    for cell_id in range(1, cells):
        display_img[separate_map == cell_id, :] = random_colors[cell_id, :]
    fig_new = plt.figure()
    plt.imshow(display_img)

def calculate_neighboor_matrix(cells,boundaries,nonneighboor_cells):
    """
        This function creates adjacency matrix for the decomposed cell
        Output: Matrix composed of zeros and ones
                output.shape --> total_cell_number x total_cell_number
        Assumption: One cell is not neighboor with itself, so diagonal elements
                    are always zero!        
        Example: let's say we have 3 cells: cell1 and cell2 are only neighboors
                adjacency_matrix = [ [0 1 0] #cell1 is neighboor with cell2 
                                     [1 0 0] #cell2 is neighboor with cell1
                                     [0 0 0]  ]
    """
    total_cell_number = len(cells)
    #print("Debug")
    #print("Total cell number: ", total_cell_number)
    #print("Cells: ", cells)
    #print("Boundaries: ", boundaries)
    #print("Non-neighboor cells: ", nonneighboor_cells)


if __name__ == '__main__':
    
    # Read the original data
    #original_map = cv2.imread("../data/example2.png")
    original_map = cv2.imread("../data/example2.png")[:,0:350]

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
    bcd_out_im, bcd_out_cells, cell_numbers, cell_boundaries, non_neighboor_cell_numbers = bcd(binary_map)
    # Show the decomposed cells on top of original map
    display_separate_map(bcd_out_im, bcd_out_cells)

    calculate_neighboor_matrix(cell_numbers,cell_boundaries,non_neighboor_cell_numbers)

    # Just for convenience
    plt.show(block=False)
    plt.waitforbuttonpress(1)
    input("Please press any key to close all figures.")
    plt.close("all")
