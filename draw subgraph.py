import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from tqdm import tqdm
import time

def parse_subgraph(data):
    """Parse a line of subgraph data into vertices and edges."""
    vertices = set()
    edges = []
    parts = data.split('|')
    vertex_part = parts[0].strip()
    edge_part = parts[1].strip() if len(parts) > 1 else ''

    # Parse vertices
    for vertex in vertex_part.replace('Vertices:', '').strip().split():
        if vertex.startswith('*'):
            continue
        vertices.add(int(vertex))

    # Parse edges
    if edge_part:
        edge_part = edge_part.replace('Edges:', '').strip()
        if edge_part:
            edge_strings = edge_part.split('), (')
            edge_strings[0] = edge_strings[0].lstrip('(')
            edge_strings[-1] = edge_strings[-1].rstrip(')')
            for edge in edge_strings:
                try:
                    edges.append(tuple(map(int, edge.split(','))))
                except ValueError:
                    print(f"Skipping malformed edge: {edge}")

    return vertices, edges

def pentagonal_layout(G):
    """Return pentagonal positions for the vertices in a graph."""
    pos = {}
    nodes = list(G.nodes())
    num_nodes = len(nodes)
    
    if num_nodes == 5:
        angle = 2 * np.pi / num_nodes
        radius = 1
        for i, node in enumerate(nodes):
            pos[node] = (radius * np.cos(i * angle), radius * np.sin(i * angle))
    else:
        pos = circular_layout(G)  # Fallback to circular layout for other cases

    return pos

def square_layout(G):
    """Return square positions for the vertices in a graph."""
    pos = {}
    nodes = list(G.nodes())
    num_nodes = len(nodes)
    
    # Define a square layout for 4 nodes
    if num_nodes == 4:
        positions = [
            (0, 0), (1, 0),
            (0, 1), (1, 1)
        ]
        for i, node in enumerate(nodes):
            pos[node] = positions[i]
    else:
        pos = circular_layout(G)  # Fallback to circular layout for other cases

    return pos

def circular_layout(G):
    """Return circular positions for the vertices in a graph."""
    pos = {}
    nodes = list(G.nodes())
    num_nodes = len(nodes)
    
    # Define a circular layout for nodes
    if num_nodes > 1:
        angle = 2 * np.pi / num_nodes
        radius = 1
        for i, node in enumerate(nodes):
            pos[node] = (radius * np.cos(i * angle), radius * np.sin(i * angle))
    else:
        pos[nodes[0]] = (0, 0)
        
    return pos

def plot_subgraph(vertices, edges, subgraph_number, ax):
    """Plot a subgraph on the provided axis."""
    G = nx.Graph()
    G.add_nodes_from(vertices)
    G.add_edges_from(edges)

    # Use specific layouts based on the number of vertices
    num_vertices = len(vertices)
    if num_vertices == 3:
        pos = circular_layout(G)
    elif num_vertices == 4:
        pos = square_layout(G)
    elif num_vertices == 5:
        pos = pentagonal_layout(G)
    else:
        pos = triangular_layout(G)  # Use triangular layout for other cases

    nx.draw(
        G, pos,
        with_labels=True,
        node_color='skyblue',
        node_size=200,  # Smaller node size
        edge_color='black',  # Darker edge color
        font_size=8,
        font_weight='bold',
        ax=ax,
        edgecolors='black',  # Darker edge color
        width=2,  # Darker and thicker edge lines
        alpha=0.8  # Slight transparency for edges
    )

    # Adjust axis limits based on node positions
    x_vals, y_vals = zip(*pos.values())
    x_margin = 0.5
    y_margin = 0.5
    ax.set_xlim(min(x_vals) - x_margin, max(x_vals) + x_margin)
    ax.set_ylim(min(y_vals) - y_margin, max(y_vals) + y_margin)

    ax.set_title(f'Subgraph {subgraph_number}', fontsize=10)
    ax.axis('off')  # Hide axes for a cleaner look

def triangular_layout(G):
    """Return triangular positions for the vertices in a graph."""
    pos = {}
    nodes = list(G.nodes())
    num_nodes = len(nodes)
    
    # Define a triangular grid layout
    if num_nodes == 1:
        pos[nodes[0]] = (0, 0)
    elif num_nodes <= 3:
        for i, node in enumerate(nodes):
            pos[node] = (i, 0)
    elif num_nodes <= 6:
        positions = [
            (0, 0), (1, 0), (2, 0),
            (0.5, 1), (1.5, 1),
            (1, 2)
        ]
        for i, node in enumerate(nodes):
            pos[node] = positions[i]
    else:
        # For more than 6 nodes, use a default grid layout
        for i, node in enumerate(nodes):
            pos[node] = (i % 3, i // 3)

    return pos

def read_graph_data(file_path):
    """Read the graph data from a file."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def main():
    # File path to the text file with subgraph data
    file_path = r"C:\Users\ASUS\Desktop\maharshee\Python\Python Codes\graph_data.txt"
    
    # Read data from the file
    data_lines = read_graph_data(file_path)

    num_subgraphs = len(data_lines)
    num_cols = 5  # Number of columns per page
    num_rows = 8  # Number of rows per page
    subgraphs_per_page = num_cols * num_rows

    # Create a PDF file to save the plots
    with PdfPages('final_112_final.pdf') as pdf:
        for page_start in tqdm(range(0, num_subgraphs, subgraphs_per_page), desc="Processing Pages"):
            # Create a new figure for each page
            fig, axes = plt.subplots(num_rows, num_cols, figsize=(8.3, 11.7))  # A4 size in inches
            axes = axes.flatten()

            # Track time for progress estimation
            start_time = time.time()

            # Plot subgraphs for the current page
            for i in range(page_start, min(page_start + subgraphs_per_page, num_subgraphs)):
                vertices, edges = parse_subgraph(data_lines[i])
                plot_subgraph(vertices, edges, i + 1, axes[i - page_start])
           
            # Hide any unused subplots
            for j in range(min(page_start + subgraphs_per_page, num_subgraphs) - page_start, len(axes)):
                axes[j].axis('off')

            plt.tight_layout()
            pdf.savefig(fig)
            plt.close()

            # Estimate time taken for this page
            elapsed_time = time.time() - start_time
            print(f"Time taken for page {page_start // subgraphs_per_page + 1}: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
