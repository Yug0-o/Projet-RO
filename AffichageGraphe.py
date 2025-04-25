import networkx as nx
import matplotlib.pyplot as plt

def afficher_graphe(G, tour=None):
    """
    Affiche le graphe avec les poids des arêtes.

    :param G: Graphe à afficher
    :param tour: Liste des nœuds dans l'ordre de la tournée
    """
    pos = nx.spring_layout(G, seed=42)
    labels = {(u, v): f"{G[u][v]['weight']:.0f}" if G[u][v]['weight'] != float('inf') else '∞' for u, v in G.edges()}

    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')

    if tour:
        tour_edges = [(tour[i], tour[i + 1]) for i in range(len(tour) - 1)]
        tour_edges.append((tour[-1], tour[0]))
        nx.draw_networkx_edges(G, pos, edgelist=tour_edges, edge_color='r', width=2)

    for edge, label in labels.items():
        u, v = edge
        x = (pos[u][0] + pos[v][0]) / 2
        y = (pos[u][1] + pos[v][1]) / 2
        plt.text(x, y, label, fontsize=8, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

    plt.title("Graphe des villes avec coûts des arêtes")
    plt.show()