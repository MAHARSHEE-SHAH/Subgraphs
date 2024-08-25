import itertools
import math

# Define vertices and edges
vertices = range(4)
edges = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
v = len(vertices)
e = len(edges)

def edgeExists(tup1):
    # Check if an edge exists between two vertices in the given graph
    return tup1 in edges or (tup1[1], tup1[0]) in edges

def display_combination(combination, edge_subset, line_counter):
    # Display a combination with isolated vertices marked by *
    subgraph_representation = []
    for vertex in vertices:
        if vertex in combination:
            subgraph_representation.append(str(vertex))
        else:
            subgraph_representation.append(f"*{vertex}")
    
    edge_list = [f"({a},{b})" for a, b in edge_subset]
    
    print(f"Vertices: {' '.join(subgraph_representation)} | Edges: {', '.join(edge_list)}")


def generate_subgraphs():
    all_subgraphs = []
    line_counter = 1  # Initialize line counter
    # Iterate over all possible subsets of vertices (excluding the empty set)
    for n in range(1, v + 1):
        combinations = list(itertools.combinations(vertices, n))
        for combination in combinations:
            # Generate all possible subsets of edges within the current combination of vertices
            possible_edges = list(itertools.combinations(combination, 2))
            valid_edges = [edge for edge in possible_edges if edgeExists(edge)]
            for edge_subset in itertools.chain.from_iterable(itertools.combinations(valid_edges, r) for r in range(len(valid_edges)+1)):
                display_combination(combination, edge_subset, line_counter)
                all_subgraphs.append((combination, edge_subset))
                line_counter += 1  # Increment line counter
    
    return all_subgraphs

# Generate and display all subgraphs
subgraphs = generate_subgraphs()

# Print the total number of subgraphs
print("Total number of subgraphs:", len(subgraphs))
