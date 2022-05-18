def flowgraph_dual(graph, net_flow_vector, ring, random=False):
    """
    Returns the PS dual graph of the given "graph" and net flow vector, i.e. graph associated to the adjacency relations of the polytope obtained by Postnikov-Stanley triangulation of "graph".
    
    INPUT:
    
    * "graph" is a sage DiGraph with multiedges that contains a net_flow_list graph (or net_flow_list network).
    WARNING: It must be a edge labeled graph with polynomials as labels.
    
    * "net_flow_list" is a list which contains the introduced flow for the vertices of "graph".
    The lenght of "net_flow_list" must be the same number of vertices of "graph".
    WARNING: Sum of "net_flow_list" must be 0 for preserve the graph flow.
    
    * "ring" is a polynomial ring on which take values the labels of the edges of "graph".

    * "random" is a optional parameter False by default. If it is True, the the Postnikov-Stanley triangulation will have not a stablished order.
    """
    
    #Calculate the dimension of the flow polytope associated to "graph"
    dimension = flowgraph_polytope(graph,net_flow_vector,ring).dim()

    #list of flow graphs after apply the total reduction of "graph"
    graphs = flowgraph_reverse_total_reduction(graph,net_flow_vector,random)
    
    #initialize the lists of the full dimensional polytopes ans their graphs
    full_dimensional_graphs, full_dimensional_polytopes, volume = [], [], 0
    for G in graphs:
        polytope = flowgraph_polytope(G[0],net_flow_vector,ring)
        if polytope.dim() == dimension:
            #save in the lists of the polytopes and graphs if it have the same dimension of the initial one
            full_dimensional_graphs.append(G)
            full_dimensional_polytopes.append(polytope)
            volume = volume+1
    
    #initialize the PS dual graph as a simple undirected graph
    ps_dual_graph = Graph()
    
    #runs over all the polytopes twice for verify if them are adjacent
    for polytope1 in range(volume):
        for polytope2 in range(volume):
            if polytope1 != polytope2:
                #the polytopes are adjacent if their intersection have
                #the dimension of the original less 1
                if full_dimensional_polytopes[polytope1].intersection(full_dimensional_polytopes[polytope2]).dim()==dimension-1:
                    #and if them are adjacent, create the edge
                    ps_dual_graph.add_edge(full_dimensional_graphs[polytope1][1],full_dimensional_graphs[polytope2][1])
    
    #The function returns the PS dual graph of the triangulation
    return ps_dual_graph