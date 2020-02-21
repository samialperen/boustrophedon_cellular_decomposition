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
    out_list = []
    added = set()
    for val in in_list:
        if not val in added:
            out_list.append(val)
            added.add(val)
    return out_list


def bcd(erode_img: np.ndarray) -> Tuple[np.ndarray, int]:
    """
    Boustrophedon Cellular Decomposition

    Args:
        erode_img: [H, W], eroded map. The pixel value 0 represents obstacles and 1 for free space.

    Returns:
        [H, W], separated map. The pixel value 0 represents obstacles and others for its' cell number.
    """
    assert len(erode_img.shape) == 2, 'Map should be single channel.'
    last_connectivity = 0
    last_connectivity_parts = []
    current_cell = 1
    current_cells = []
    separate_img = np.copy(erode_img)
    cells_boundaries = {}
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
            cells_boundaries.setdefault(cell_index,[])
            cells_boundaries[cell_index].append(connective_parts)
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
                cells_boundaries.setdefault(cell_index,[])
                cells_boundaries[cell_index].append(connective_parts[i])
    
    # Create adjacency (neighborhood matrix) for the cells based on
    # cell number
    # Cell 1 is the left most cell and cell n is the right most cell
    # where n is the total cell number
    n = len(cells_boundaries.keys())
    all_cell_numbers = cells_boundaries.keys()

    non_neighboor_cells = remove_duplicates(non_neighboor_cells)
   
    #non_neighboor_cells = list(dict.fromkeys(non_neighboor_cells))
    print(non_neighboor_cells)

    # Debug
    #print("Keys: ",cells_boundaries.keys())
    #key1 = list(cells_boundaries.keys())[0]
    #print("Key1: ", key1)
    #print("Key2 value: ", cells_boundaries.get(key1))
    #
    #key2 = list(cells_boundaries.keys())[1]
    #print("Key2: ", key2)
    #print("Key2 value: ", cells_boundaries.get(key2))
    #
    #key3 = list(cells_boundaries.keys())[2]
    #print("Key3: ", key3)
    #print("Key3 value: ", cells_boundaries.get(key3))
    #
    #key4 = list(cells_boundaries.keys())[3]
    #print("Key4: ", key4)
    #print("Key4 value: ", cells_boundaries.get(key4))
    #
    #key5 = list(cells_boundaries.keys())[4]
    #print("Key5: ", key5)
    #print("Key5 value: ", cells_boundaries.get(key5))
    #
    #key6 = list(cells_boundaries.keys())[5]
    #print("Key6: ", key6)
    #print("Key6 value: ", cells_boundaries.get(key6))
    #
    #key7 = list(cells_boundaries.keys())[6]
    #print("Key7: ", key7)
    #print("Key7 value: ", cells_boundaries.get(key7))

    return separate_img, current_cell


def display_separate_map(separate_map, cells):
    display_img = np.empty([*separate_map.shape, 3], dtype=np.uint8)
    random_colors = np.random.randint(0, 255, [cells, 3])
    for cell_id in range(1, cells):
        display_img[separate_map == cell_id, :] = random_colors[cell_id, :]
    fig_new = plt.figure()
    plt.imshow(display_img)


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
    bcd_out_im, bcd_out_cells = bcd(binary_map)
    print('Total cells: {}'.format(bcd_out_cells))
    # Show the decomposed cells on top of original map
    display_separate_map(bcd_out_im, bcd_out_cells)



    # Just for convenience
    plt.show(block=False)
    plt.waitforbuttonpress(1)
    input("Please press any key to close all figures.")
    plt.close("all")
