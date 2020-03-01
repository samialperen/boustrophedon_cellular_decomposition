import mlrose
import numpy as np

def distance(x_coordinates,y_coordinates,cell1,cell2):
    """
    Input: x_coordinates, y_coordinates --> they hold mean coordinate values of each cell
                                            they are dictionaries
    Output: distance between city1 and city2
    """
    cell1 += 1 # Real cell numbers start from 1, but mlrose requires zero indices
    cell2 += 1 # x_coordinates,y_coordinates have real cell numbers, i.e. starts from one
    a = np.array([x_coordinates[cell1],y_coordinates[cell1]])
    b = np.array([x_coordinates[cell2],y_coordinates[cell2]])
    return np.linalg.norm(a-b)

def distance_optim(x_coordinates,y_coordinates):
    # Create the distance list for cell pairs
    # Unfortunately, cell indices starts from zero for mlrose
    dist_list = [(0, 1, distance(x_coordinates,y_coordinates,0,1)), (0, 2, distance(x_coordinates,y_coordinates,0,2)),\
                 (1, 3, distance(x_coordinates,y_coordinates,1,3)), (2, 3, distance(x_coordinates,y_coordinates,2,3)),\
                 (3, 4, distance(x_coordinates,y_coordinates,3,4)), (3, 5, distance(x_coordinates,y_coordinates,3,5)),\
                 (4, 6, distance(x_coordinates,y_coordinates,4,6)), (5, 6, distance(x_coordinates,y_coordinates,5,6)),\
                 (6, 7, distance(x_coordinates,y_coordinates,6,7)), (6, 8, distance(x_coordinates,y_coordinates,6,8)),\
                 (7, 9, distance(x_coordinates,y_coordinates,7,9)), (8, 9, distance(x_coordinates,y_coordinates,8,9)),\
                 (9, 10, distance(x_coordinates,y_coordinates,9,10)), (9, 11, distance(x_coordinates,y_coordinates,9,11)),\
                 (10, 12, distance(x_coordinates,y_coordinates,10,12)), (11, 12, distance(x_coordinates,y_coordinates,11,12))]

    # Define a fitness function object
    fitness_dists = mlrose.TravellingSales(distances = dist_list)
    # Define a optimization problem object
    problem_fit = mlrose.TSPOpt(length = len(y_coordinates), fitness_fn = fitness_dists, maximize=False)
    return problem_fit

def genetic_algorithm(problem,pop_size,mutation_prob,max_attemp):
    """
    Genetic algorithm implementation to minimize TSP
    Inputs: 
            fitness --> fitness distances required by mlrose
            problem --> optimization problem object required by mlrose
            pop_size --> population_size: genetic algorithm parameter
            mutation_prob --> mutation_probability: genetic algorithm parameter
            max_attemp --> maximum attemps per step: genetic algorithm parameter
    Outputs: 
            optimized_cells --> cells to visit
    """
    optimized_cells, _ = mlrose.genetic_alg(problem, mutation_prob = mutation_prob,\
                                        max_attempts = max_attemp, random_state = 2)
    return optimized_cells