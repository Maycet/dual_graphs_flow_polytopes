def caracol_graph(n, labels=None):
    """
    Returns the n-Caracol flow graph with n+1 vertices.
    If labels are given, returns only the graph othercase returns a tuple with the Caracol graph and the polynomial ring in which are defined the labels of the edges.
    
    INPUT:
    
    * "n" is an integer, the index of the Caracol graph, i.e. the number of the vertices less 1.
    
    * "labels" is an optional argument, a list which contains the labels for the graph. If it's not given, the graph will have variables on a polynomial ring as labels.
    WARNING: If the list is given but the length is different to 3*(n+1)-7 (the total number of edges in a Caracol graph) it will works as the edges were not given.
             The labels have to live in some polynomial ring for an easy application of the PS algorithm.
    
    EXAMPLES::
    
        sage: caracol_graph(4)
        Defining X1_2, X1_3, X1_4, X2_3, X2_5, X3_4, X3_5, X4_5
        4-Caracol graph with edge labels in a polynomial ring.
        sage: caracol_graph(3,['a','b','c','d','e'])
        Edge labeled 3-Caracol graph.
        sage: caracol_graph(6,['a','b','c'])
        Defining X1_2, X1_3, X1_4, X1_5, X1_6, X2_3, X2_7, X3_4, X3_7, X4_5, X4_7, X5_6, X5_7, X6_7
        6-Caracol graph with edge labels in a polynomial ring.
    """
    
    #Define the number of vertices and the graph object
    n = n+1
    G = DiGraph(multiedges=True)
    G.add_edge(0,1) #the first edge
    
    #create the edges between inner vertices, edges from source
    #to inner vertices and from inner vertices to sink
    for i in range(1,n-2):
        G.add_edges([[i,i+1],[0,i+1],[i,n-1]])
    G.add_edge(n-2,n-1) #the last edge
    
    #verify if labes are not given or if given ones have the correct size
    if labels == None or len(labels) != 3*n-7:
        #if no valid labels were given, we create the names of the variables
        #the variables/edges are named according to the vertices in every edge
        #name 'X_i_j' correspond to an edge from vertex i to vertex j
        variable_names = ['X%i_%i'%(edge[0]+1,edge[1]+1) for edge in G.edges()]
        reverse_variable_names = copy(variable_names)
        reverse_variable_names.reverse()
        
        #PolynomialRing object in rationals, with variables names in the list
        ring = PolynomialRing(QQ,reverse_variable_names)
        ring.inject_variables() #this create the variables as script objects

        #now polynomial variables are assigned as label to every edge in graph
        for i,j,l in G.edges():
            G.set_edge_label(i,j,(eval(variable_names[G.edges().index((i,j,l))]),eval(variable_names[G.edges().index((i,j,l))])))

        #show a message that the graph object are succesfully created
        print str(n-1)+"-Caracol graph with edge labels in a polynomial ring."
        return G,ring #returns a tuple with the graph and the polynomial ring
    
    #if labels with matching size are given, assing the names to the edges
    for i,j,l in G.edges():
        #the order of the labels are not related with the names of the edges
        G.set_edge_label(i,j,labels[G.edges().index((i,j,l))])

    #show a message that the graph object are succesfully created
    print "Edge labeled "+str(n-1)+"-Caracol graph."
    return G #returns only the graph with the given labels