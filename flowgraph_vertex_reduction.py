def flowgraph_vertex_reduction(graph, vertex, net_flow_vertex, polynomial, random=False):
    """
    Returns a list with the result of making a reduction of a flow graph "graph" at "vertex".
    That reduction is the described in the PS algorithm and contains a set of graphs.
    
    INPUT:
    
    * "graph" is a flow graph (also known as directed network or flow network) given as a sage DiGraph with enable multiple edges.
    The edges of the graph must have polynomials as labels, these polynomials completely decribes the assosiated polytope. (The complete flow must be 0 for the balance of the graph)

    * "vertex" is the index of the vertex of "graph" at which the reduction will be applied.

    * "net_flow_vertex" is the net flow to be introduced at "vertex", it surely is in the "vertex"-th entry of a net flow list.
    
    * "polynomial" is a polynomial that is used to distinguish the graph, used practically as label of "graph".
    
    * "random" is an optional argument, if it is True a shuffle (default method) at the list of outgoing edges is applied.
    If it is not given, the list of outgoing edges is ordered according to the polynomial ring order.
    
    EXAMPLES::
    
        sage: car_4 = Caracol_graph(4)
        Defining X1_2, X1_3, X1_4, X2_3, X2_5, X3_4, X3_5, X4_5
        4-Caracol graph with edge labels in a polynomial ring.
        sage: reduction_3 = flowgraph_vertex_reduction(graph=car_4[0], vertex=3, net_flow_vertex=0, random=False)
        sage: reduction_3
        [Multi-digraph on 5 vertices]
    """

    #define an empty list in which the result of the reduction will be stored
    reduction = []
    
    #list of the edges at "vertex" for use in the method
    incoming_edges = graph.incoming_edges(vertex)
    outgoing_edges = graph.outgoing_edges(vertex)
    
    #A flag for check if the set of incoming edges was ordered
    incoming_ordered = 0
    while incoming_ordered == 0:
        incoming_ordered = 1
        for edge in range(len(incoming_edges)-1):
            #insertion sort, reversing the ordering
            if incoming_edges[edge][2][0] < incoming_edges[edge+1][2][0]:
                temp = incoming_edges[edge]
                incoming_edges[edge] = incoming_edges[edge+1]
                incoming_edges[edge+1] = temp
                incoming_ordered = 0
                break
    
    #A flag for check if the set of outgoing edges was ordered
    outgoing_ordered = 0
    while outgoing_ordered == 0:
        outgoing_ordered = 1
        for edge in range(len(outgoing_edges)-1):
            #insertion sort, reversing the ordering
            if outgoing_edges[edge][2][0] < outgoing_edges[edge+1][2][0]:
                temp = outgoing_edges[edge]
                outgoing_edges[edge] = outgoing_edges[edge+1]
                outgoing_edges[edge+1] = temp
                outgoing_ordered = 0
                break
    
    #verify if "random" is setted as True, if it is make a shuffle in the edges
    if random:
        shuffle(outgoing_edges)
    
    #add an edge to keep the net flow at "vertex" for use it in the algorithm
    incoming_edges.append((vertex,vertex,(net_flow_vertex,net_flow_vertex)))
    incoming = len(incoming_edges) #number of incoming edges
    outgoing = len(outgoing_edges) #number of outgoing edges
    
    #It will run over all the integer compositions of the number of outgoing
    #edges less 1 on the number of incoming edges parts
    for composition in list(IntegerVectors(outgoing-1,incoming)):
        #create an auxiliar graph for keepeng the original at every composition
        graph_aux = graph.copy()
        graph_aux.delete_vertex(vertex) #for remove all the edges of "vertex"
        graph_aux.add_vertex(vertex) #and create the same vertex with no edges
        
        #the polynomial label of the new graphs depending of the composition
        new_polynomial = polynomial+sum([incoming_edges[a][2][1]*composition[a] for a in range(incoming)])        
        
        Polynom = 0 #Initialize the polynomial used for the labels of the edges
        pos_out = 0 #The position on the list of outgoing edges
        
        #It will run over all the indices of the entries of the composition
        for pos_in in range(len(composition)):
            #verify if there are only an edge on that vertex in bipartite tree
            if composition[pos_in] == 0:
                #verify if it is the last element of the incoming edges
                if pos_in == len(composition)-1:
                    #make the polynomial and add the new edge to the graph
                    Polynom = outgoing_edges[pos_out][2][1]-Polynom
                    graph_aux.add_edge(incoming_edges[pos_in][0],outgoing_edges[pos_out][1],(incoming_edges[pos_in][2][0]+outgoing_edges[pos_out][2][0],Polynom))
                else:
                    #make the polynomial and add the new edge to the graph
                    graph_aux.add_edge(incoming_edges[pos_in][0],outgoing_edges[pos_out][1],(incoming_edges[pos_in][2][0]+outgoing_edges[pos_out][2][0],incoming_edges[pos_in][2][1]))
                    Polynom = Polynom+incoming_edges[pos_in][2][1]
            else:
                #make the polynomial and add the new edge to the graph
                Polynom = outgoing_edges[pos_out][2][1]-Polynom
                graph_aux.add_edge(incoming_edges[pos_in][0],outgoing_edges[pos_out][1],(incoming_edges[pos_in][2][0]+outgoing_edges[pos_out][2][0],Polynom))
                pos_out = pos_out+1 #pass to the next outgoing edge index
                
                #initialize the number of tree edges at that vertex
                max_tree_edges=1
                while max_tree_edges < composition[pos_in]:
                    #make the polynomial and add the new edge to the graph
                    graph_aux.add_edge(incoming_edges[pos_in][0],outgoing_edges[pos_out][1],(incoming_edges[pos_in][2][0]+outgoing_edges[pos_out][2][0],outgoing_edges[pos_out][2][1]))
                    Polynom = Polynom+outgoing_edges[pos_out][2][1]
                    pos_out = pos_out+1 #pass to the next outgoing edge index
                    max_tree_edges = max_tree_edges+1 #pass to the next edge
                #verify if it is the last element of the incoming edges
                if pos_in == len(composition)-1:
                    #make the polynomial and add the new edge to the graph
                    graph_aux.add_edge(incoming_edges[pos_in][0],outgoing_edges[pos_out][1],(incoming_edges[pos_in][2][0]+outgoing_edges[pos_out][2][0],outgoing_edges[pos_out][2][1]))
                else:
                    Polynom = incoming_edges[pos_in][2][1]-Polynom
                    graph_aux.add_edge(incoming_edges[pos_in][0],outgoing_edges[pos_out][1],(incoming_edges[pos_in][2][0]+outgoing_edges[pos_out][2][0],Polynom))
        
        #save the new graph ant the corresponding label polynomial in a list
        reduction.append([graph_aux,new_polynomial])
    
    #return the list of all the new graphs and its polynomials
    return reduction