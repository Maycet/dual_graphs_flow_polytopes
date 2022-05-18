def flowgraph_reverse_total_reduction(graph, net_flow_vector, random=False):
    """
    Returns a list with the entire Postnikov-Stanley triangulation of "graph" walking through the inner vertices from the last to the first one.
    
    INPUT:
    
    * "graph" is a sage DiGraph with multiedges that contains a flow graph (or flow network).
    WARNING: It must be a edge labeled graph with polynomials as labels.
    
    * "net_flow_list" is a list which contains the introduced flow for the vertices of "graph". The lenght of "net_flow_list" must be the same number of vertices of "graph".
    WARNING: Sum of "net_flow_list" must be 0 for preserve the graph flow.
    
    * "random" is a optional parameter False by default. If it is True, the set of outgoing edges in every iteration will no have a specific order in the moment of the reduction.
    """
    
    #Initialize the list of the triangulation with "graph" in there for the recursive process
    reduction = [[graph,0]]

    #list the inner vertices for apply the vertex reduction at each of them
    vertices = graph.vertices()[1:-1]
    
    #reverse the list of vertices for apply the "reverse total reduction"
    vertices.reverse()
    
    #Runs over every vertex in the graph for make the corresponding reduction
    for vertex in vertices:
        #the reduction will be applied in the graphs in the current "iteration"
        for G in reduction:
            #to the reduction we append the result of the vertex reduction
            reduction = reduction+flowgraph_vertex_reduction(G[0],vertex,net_flow_vector[vertex],G[1],random)
            #and we delete the first one, that is the initial graph
            reduction.pop(0)
    
    #after the reduction in every vertex returns a list with the simplex graphs
    return reduction