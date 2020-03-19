# Fix OpenCv2 configuration error with ROS
import sys
sys.path.remove("/opt/ros/kinetic/lib/python2.7/dist-packages")

import bcd  #The Boustrophedon Cellular decomposition
import dfs  #The Depth-first Search Algorithm
import bfs  #The Breadth First Search Algorithm
import distance_optim #Distance based optimization of TSP --> genetic, hill climbing etc.

import move_boustrophedon # Uses output of bcd cells in order to move the robot
import exceptions

import timeit


if __name__ == '__main__':
    
    # Read the original data
    original_map = bcd.cv2.imread("../data/real_ex2.png")
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
        _,binary_map = bcd.cv2.threshold(single_channel_map,127,1,bcd.cv2.THRESH_BINARY)

    # Call The Boustrophedon Cellular Decomposition function
    bcd_out_im, bcd_out_cells, cell_numbers, cell_boundaries, non_neighboor_cell_numbers = bcd.bcd(binary_map)
    # Show the decomposed cells on top of original map
    bcd.display_separate_map(bcd_out_im, bcd_out_cells)
    move_boustrophedon.plt.show(block=False)

    #cell_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,14,15,16,17,18,19,20,21,22,23,24]

    #print("Total cell number: ", len(cell_numbers))
    #print("Cells: ", cell_numbers)
    #print("Non-neighboor cells: ", non_neighboor_cell_numbers)
    #print("Cell boundaries: ", cell_boundaries)

    # Calculate optimum path using the depth first search
    # In the future, this graph1 should be calculated automatically using bcd outputs
    graph1 = { #graph1 is for real_ex1.png
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

    graph2 = { #graph2  is for real_ex2.png
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
        13: [11,12,14,15],
        14: [13,16],
        15: [13,16],
        16: [14,15,18,19],
        17: [16,19],
        18: [16,19],
        19: [17,18,20,21],
        20: [19,22],
        21: [19,22],
        22: [20,21,23,24],
        23: [22,25],
        24: [22,25],
        25: [23,24]
    }

    ########### DFS
    cleaned_DFS = [] #Keeps cleaned cell numbers in order
    iter_number = 1000
    #starting_cell_number = move_boustrophedon.randint(1,len(cell_numbers))
    starting_cell_number = 15
    print("Starting cell number: ", starting_cell_number)
    exec_time_dfs = timeit.timeit('dfs.dfs(cleaned_DFS, graph2, starting_cell_number)', \
        'from __main__ import dfs, cleaned_DFS, graph2, starting_cell_number',number = iter_number)
    exec_time_dfs = exec_time_dfs/iter_number
    print("DFS Cleaned cells in order", cleaned_DFS)
    print("Execution time of dfs in seconds: ", exec_time_dfs)

    # Check the output of the DFS --> All cells should be visited!
    #if (len(cell_numbers) != len(cleaned_DFS)):
    #    print("Total cell number: ", len(cell_numbers))
    #    print("Visited total cell number: ", len(cleaned_DFS))
    #    raise exceptions.DfsError("DFS couldn't find a path to visit all cells!")
    


    ######### BFS
    cleaned_BFS = [] #Keeps cleaned cell numbers in order
    iter_number = 1000
    #starting_cell_number = move_boustrophedon.randint(1,len(cell_numbers))
    print("Starting cell number: ", starting_cell_number)
    exec_time_bfs = timeit.timeit('bfs.bfs(cleaned_BFS, graph2, starting_cell_number)', \
        'from __main__ import bfs, cleaned_BFS, graph2, starting_cell_number',number = iter_number)
    exec_time_bfs = exec_time_bfs/iter_number
    print("BFS Cleaned cells in order", cleaned_BFS)
    print("Execution time of bfs in seconds: ", exec_time_bfs)

    ### Check the output of the BFS --> All cells should be visited!
    #if (len(cell_numbers) != len(cleaned_BFS)):
    #    print("Total cell number: ", len(cell_numbers))
    #    print("Visited total cell number: ", len(cleaned_BFS))
    #    raise exceptions.BfsError("BFS couldn't find a path to visit all cells!")
    
    ########### Add cost using distance between center of mass of cells
    # Small function to calculate mean --> no need to use numpy or statistics module
    def mean(input_list):
        output_mean = sum(input_list)/len(input_list)
        return output_mean

    def mean_double_list(input_double_list):
        length = len(input_double_list)
        total = 0 
        for i in range(length):
            total += mean(input_double_list[i])
        
        output_mean = total/length
        return output_mean

    def mean_d_double_list(input_double_list):
        length = len(input_double_list)
        total = 0 
        for i in range(length):
            total += mean(input_double_list[i][0])
        
        output_mean = total/length
        return output_mean
    
    x_length = original_map.shape[1]
    y_length = original_map.shape[0]

    x_coordinates = move_boustrophedon.calculate_x_coordinates(x_length, y_length, \
                    cell_numbers,cell_boundaries,non_neighboor_cell_numbers)
    y_coordinates = cell_boundaries

    mean_x_coordinates = {}
    mean_y_coordinates = {}
    for i in range(len(x_coordinates)):
        cell_idx = i+1 #i starts from zero, but cell numbers start from 1
        mean_x_coordinates[cell_idx] = mean(x_coordinates[cell_idx])
        if type(y_coordinates[cell_idx][0]) is list:
            mean_y_coordinates[cell_idx] = mean_d_double_list(y_coordinates[cell_idx])
        else:
            mean_y_coordinates[cell_idx] = mean_double_list(y_coordinates[cell_idx])
    
    

    # Create a common optimization problem for the mlrose library
    optim_problem = distance_optim.distance_optim(mean_x_coordinates,mean_y_coordinates)

    ####### Genetic algorithm
    iter_number = 10
    starting_cell_number = 15
    print("Starting cell number (not used in ga): ", starting_cell_number)
    exec_time_ga = timeit.timeit('distance_optim.genetic_algorithm(optim_problem,200,0.2,10)', \
        'from __main__ import distance_optim, optim_problem', number = iter_number)
    exec_time_ga = exec_time_ga/iter_number
    print("Execution time of genetic algorithm in seconds: ", exec_time_ga)
    cleaned_genetic = distance_optim.genetic_algorithm(optim_problem,200,0.2,10)
    print("Genetic output:", cleaned_genetic)

    ####### Hill climbing
    iter_number = 10
    print("Starting cell number: ", starting_cell_number)
    exec_time_hc = timeit.timeit('distance_optim.hill_climbing(optim_problem,starting_cell_number)', \
        'from __main__ import distance_optim, optim_problem, starting_cell_number', number = iter_number)
    exec_time_hc = exec_time_hc/iter_number
    print("Execution time of hill climbing in seconds: ", exec_time_hc)
    cleaned_hc = distance_optim.hill_climbing(optim_problem,starting_cell_number)
    print("Hill climbing output:", cleaned_hc)

    ####### Simulated Annealing
    iter_number = 10
    print("Starting cell number: ", starting_cell_number)
    exec_time_sa = timeit.timeit('distance_optim.simulated_annealing(optim_problem,starting_cell_number)', \
        'from __main__ import distance_optim, optim_problem, starting_cell_number', number = iter_number)
    exec_time_sa = exec_time_sa/iter_number
    print("Execution time of simulated annealing in seconds: ", exec_time_sa)
    cleaned_sa = distance_optim.simulated_annealing(optim_problem,starting_cell_number)
    print("Simulated annealing output:", cleaned_sa)

    ####### MIMIC
    iter_number = 10
    print("Starting cell number: ", starting_cell_number)
    exec_time_mimic = timeit.timeit('distance_optim.mimic(optim_problem)', \
        'from __main__ import distance_optim, optim_problem', number = iter_number)
    exec_time_mimic = exec_time_mimic/iter_number
    print("Execution time of mimic in seconds: ", exec_time_mimic)
    cleaned_mimic = distance_optim.mimic(optim_problem)
    print("MIMIC output:", cleaned_mimic)
    

    
    ########## Path Tracking
    # DFS
    iter_number = 1
    dfs_path = [15, 13, 11, 10, 8, 7, 5, 4, 2, 1, 3, 6, 9, 12, 14, 16, 18, 19, 17, 20, 22, 21, 23, 25, 24]
    path_time_dfs = timeit.timeit('move_boustrophedon.track_paths(original_map,dfs_path,cell_boundaries,non_neighboor_cell_numbers)', \
                                   'from __main__ import move_boustrophedon, \
                                   dfs_path, original_map, cell_boundaries,non_neighboor_cell_numbers',number = iter_number)
    path_time_dfs = path_time_dfs/iter_number
    print("Total path tracking time of dfs in seconds: ", path_time_dfs)
    

    ### BFS
    #iter_number = 1
    #bfs_path = [5, 4, 7, 2, 3, 6, 8, 9, 1, 10, 11, 12, 13]
    #path_time_bfs = timeit.timeit('move_boustrophedon.track_paths(original_map,bfs_path,cell_boundaries,non_neighboor_cell_numbers)', \
    #                               'from __main__ import move_boustrophedon, \
    #                               bfs_path, original_map, cell_boundaries,non_neighboor_cell_numbers',number = iter_number)
    #path_time_bfs = path_time_bfs/iter_number
    #print("Total path tracking time of bfs in seconds: ", path_time_bfs)

    ### Genetic algorithm
    #iter_number = 1
    #ga_path = [5, 1, 11, 6, 4, 2, 10, 8, 12, 3, 7, 13, 9]
    #path_time_ga = timeit.timeit('move_boustrophedon.track_paths(original_map,ga_path,cell_boundaries,non_neighboor_cell_numbers)', \
    #                               'from __main__ import move_boustrophedon, \
    #                               ga_path, original_map, cell_boundaries,non_neighboor_cell_numbers',number = iter_number)
    #path_time_ga = path_time_ga/iter_number
    #print("Total path tracking time of ga in seconds: ", path_time_ga)
    #

    ## Simulated Annealing
    #iter_number = 1
    #sa_path = [5, 7, 10, 3, 8, 2, 6, 4, 11, 13, 9, 12, 1]
    #path_time_sa = timeit.timeit('move_boustrophedon.track_paths(original_map,sa_path,cell_boundaries,non_neighboor_cell_numbers)', \
    #                               'from __main__ import move_boustrophedon, \
    #                               sa_path, original_map, cell_boundaries,non_neighboor_cell_numbers',number = iter_number)
    #path_time_sa = path_time_sa/iter_number
    #print("Total path tracking time of sa in seconds: ", path_time_sa)
    
    
    ## MIMIC
    #iter_number = 1
    #mimic_path = [5, 10, 2, 3, 13, 12, 9, 7, 4, 8, 11, 1, 6]
    #path_time_mimic = timeit.timeit('move_boustrophedon.track_paths(original_map,mimic_path,cell_boundaries,non_neighboor_cell_numbers)', \
    #                               'from __main__ import move_boustrophedon, \
    #                               mimic_path, original_map, cell_boundaries,non_neighboor_cell_numbers',number = iter_number)
    #path_time_mimic = path_time_mimic/iter_number
    #print("Total path tracking time of mimic in seconds: ", path_time_mimic)

 








    # Doesn't work --> Look at later, right now assume we have the graph1 
    #calculate_neighboor_matrix(cell_numbers,cell_boundaries,non_neighboor_cell_numbers)




    # Just for convenience, show each plot at the same time at different plots
    move_boustrophedon.plt.waitforbuttonpress(1)
    input("Please press any key to close all figures.")
    move_boustrophedon.plt.close("all")
