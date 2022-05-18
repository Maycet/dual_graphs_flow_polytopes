def flowgraph_polytope(graph, net_flow_vector=None, ring=None):
    """
    Returns the flow polytope generate by "graph".
    
    INPUT:
    
    * "graph" is a flow graph (also known as directed network or flow network) given as a sage DiGraph with enable multiple edges.
    The edges of the graph must have polynomials as labels, these polynomials completely decribes the assosiated polytope. (The complete flow must be 0 for the balance of the graph)
    
    * "net_flow_vector" is a list which contains the net flow for the vertices of "graph".
    The lenght of "net_flow_vector" must be the same as the number of vertices of "graph".
    If "net_flow_vector" is None, by default will be a list with 1 in the first entry and -1 in the last.
    WARNING: Sum of "net_flow_vector" must be 0 for preserve the graph flow.
    
    * "ring" is a PolynomialRing object on which take values the labels of the edges of "graph".
    If "ring" is not given a PolynomialRing with as many variables as edges in "graph" will be created and every edges will have a variable as label.
    
    EXAMPLES::
    
        sage: Ring = PolynomialRing(QQ,'x',5)
        sage: Ring.inject_variables()
        Defining x0, x1, x2, x3, x4
        sage: G = DiGraph()
        sage: G.add_edges([[1,2,x0],[1,3,x1],[2,3,x2],[2,4,x3],[3,4,x4]])
        sage: net_flow = [1,0,0,-1]
        sage: Polytope = flow_polytope(G,net_flow,Ring)
        sage: Polytope
        A 2-dimensional polyhedron in QQ^5 defined as the convex hull of 3 vertices
    """
    
    #Keep the edges and vertices into lists
    edges = graph.edges()
    vertices = graph.vertices()
    
    #If "ring" is not given, one PolynomialRing is created according to "graph"
    if ring == None:
        ring = PolynomialRing(QQ,['X%i_%i'%(edge[0],edge[1]) for edge in graph.edges()])
        ring.inject_variables()
    
    #If "net_flow_vector" is not given, a 'default' list is created
    if net_flow_vector == None:
        net_flow_vector = [0 for i in range(len(vertices))] #0 for the entries
        net_flow_vector[0] = 1 #1 in the first entry
        net_flow_vector[-1] = -1 #-1 in the last entry
    
    #Use the PolynomialRing variable names for find their coefficients
    variable_names = ring.variable_names()

    #the inequalities that describe the polytope are given as lists of
    #coefficients where the first entry is the constant term (0) and the other
    #are the coefficients of the label (polynomial) of every edge of the graph
    inequalities = [[0]+[edge[2][1].monomial_coefficient(eval(var)) for var in variable_names] for edge in edges]

    #create a empty list for the equations which depends of the edges
    equations = []
    
    #Each vertex have an associated equation depending of its edges
    for vertex in vertices[:-1]:
        #an initial zero polynomial in which save the corresponding to edges
        #remember that the "2" entry of an edge is the label (a polynomial)
        polynomial = 0

        #first adding the polynomials of the incoming edges to vertex "v"
        for incoming in graph.incoming_edges(vertex):
            polynomial = polynomial+incoming[2][1]
        
        #then subtracting the polynomials of the outgoing edges to vertex "v"
        for outgoing in graph.outgoing_edges(vertex):
            polynomial = polynomial-outgoing[2][1]
        
        #save the polynomial only if there are any information
        if polynomial != 0:
            #the net_flow_list at "v" is the constant term of the polynomial
            equations.append([net_flow_vector[vertex]]+[polynomial.monomial_coefficient(eval(var)) for var in variable_names])
    
    #Funtion returns the polytope corresponding to the equalities and equations
    return Polyhedron(eqns=equations, ieqs=inequalities)