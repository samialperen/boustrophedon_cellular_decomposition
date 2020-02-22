def dfs(cleaned, graph, node):
    if node not in cleaned:
        #print("Path: ", node)
        cleaned.append(node)
        for neighbour in graph[node]:
            dfs(cleaned, graph, neighbour)
            #print("Back at: ", node)
