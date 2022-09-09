# dual_graphs_flow_polytopes
### Collection of methods used in my bachelor's thesis for the conjectures that were proved in it.

> **Remark:** Every of the attached scripts are methods written for beign executed with Sagemath not Python itself.

> For the full context of the mathematical structures and processes you can read my bachelor's thesis at https://maycet.github.io/BachelorsThesis.html or its references for the complete documentation.

The correct order to execute the methods on this repository are:

1. `flowgraph_vertex_reduction`: Make a reduction on the specified vertex of a flow graph.
2. `flowgraph_reverse_total_reduction`: Make a reduction recursively on every vertex for every of the graphs generated on the last vertex, walking through the inner vertices from the last to the first one.
3. `flowgraph_polytope`: Translates a given flow graph in the corresponding flow polytope (as a Polyhedron object).
4. `flowgraph_dual`: Creates a graph given by the adjacency relationship on the polytopes associated to the graphs obtained from a reverse total reduction of a flow graph.
5. `caracol_graph`: Creates the Caracol graph of the specified number of vertices. (Not depends of another script).

The complete and specific documentation of that functions are in each of the scripts.
