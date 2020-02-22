def track_paths(original_im,cells_to_visit,cell_boundaries,nonneighbors):
    """
        Input: original_im --> Input map image without any preprocessing
        Input: cells_to_visit --> It contains the order of cells to visit
        Input: cell_boundaries --> It contains y coordinates of each cell
            x coordinates will be calculated in this function based on 
            cell number since first cell starts from the left and moves towards
            right
        Input: Nonneighbors --> This shows cels which are separated by the objects
                ,so these cells should have the same x coordinates!
        Output: draw the executed path on the image
            Path will be boustrophedonial --> zig,zag
        Output: total travel time
    """
    ## TODO: Calculate the margin at the beginning and at the end for x coordinates
            # They don't start at x=0 actually!


    total_cell_number = len(cells_to_visit)

    # Find the total length of the axises
    size_x = original_im.shape[1]
    size_y = original_im.shape[0]
    
    # Calculate x coordinates of each cell
    cells_x_coordinates = {}
    width_accum_prev = 0
    cell_idx = 1
    while cell_idx <= total_cell_number:
        #print("Cell index: ", cell_idx)
        for subneighbor in nonneighbors:
            #print("Subneighbor: ", subneighbor)
            if subneighbor[0] == cell_idx: #current_cell, i.e. cell_idx is divided by the object(s)
                #print("Current cell is problematic")
                separated_cell_number = len(subneighbor) #contains how many cells are in the same vertical line 
                width_current_cell = len(cell_boundaries[cell_idx])
                #print("Width current cell: ", width_current_cell)
                for j in range(separated_cell_number):
                    # All cells separated by the object(s) in this vertical line have same x coordinates 
                    cells_x_coordinates[cell_idx+j] = list(range(width_accum_prev,width_current_cell+width_accum_prev))
                width_accum_prev += width_current_cell
                cell_idx = cell_idx + separated_cell_number 
                break
        
        #current cell is not separated by any object(s)
        #print("Current cell is okay")
        width_current_cell = len(cell_boundaries[cell_idx])
        #print("Width current cell: ", width_current_cell)
        cells_x_coordinates[cell_idx] = list(range(width_accum_prev,width_current_cell+width_accum_prev))
        width_accum_prev += width_current_cell

        cell_idx = cell_idx + 1
        # end of x calculation while loop
    
    
    ## Debug
    #print("##############DEBUG##########")
    #for i in range(total_cell_number):
    #    print("cell index: ", i+1)
    #    print("width: ", len(cell_boundaries[i+1]))
    ## Debug
    #print("##############DEBUG##########")
    #for i in range(total_cell_number):
    #    print("cell index: ", i+1)
    #    print("X coordinates: ", cells_x_coordinates[i+1])

    #for i in range(len(cells_to_visit)):
    #    current_cell = cells_to_visit[i]
    #    boundaries_current_cell = cell_boundaries[current_cell]


