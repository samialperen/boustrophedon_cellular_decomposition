# visits all the nodes of a graph (connected component) using BFS
def bfs(cleaned, graph, start):
    # keep track of nodes to be checked
    queue = [start]
 
    # keep looping until there are nodes still to be checked
    while queue:
        # pop shallowest node (first node) from queue
        node = queue.pop(0)
        if node not in cleaned:
            # add node to list of checked nodes
            cleaned.append(node)
            neighbours = graph[node]
 
            # add neighbours of node to queue
            for neighbour in neighbours:
                queue.append(neighbour)