import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
import json
from AffichageGraphe import afficher_graphe

def lire_donnees(fichier):
    """
    Lit les données du graphe à partir d'un fichier JSON.

    :param fichier: Nom du fichier JSON
    :return: Graphe pondéré avec contraintes
    """
    with open(fichier, 'r') as f:
        donnees = json.load(f)

    n = donnees['nombre_de_villes']
    matrice_cout = np.array(donnees['matrice_cout'])

    G = nx.Graph()
    G.add_nodes_from(range(n))

    for u in range(n):
        for v in range(u + 1, n):
            if matrice_cout[u][v] != float('inf'):
                G.add_edge(u, v, weight=matrice_cout[u][v])

    return G

def calculer_cout(G, tour):
    """
    Calcule le coût total d'une tournée.

    :param G: Graphe
    :param tour: Liste des nœuds dans l'ordre de la tournée
    :return: Coût total de la tournée
    """
    cost = 0
    for i in range(len(tour) - 1):
        u, v = tour[i], tour[i + 1]
        if G.has_edge(u, v):
            cost += G[u][v]['weight']
        else:
            return float('inf')  # Si une arête est interdite, le coût est infini
    return cost

def algorithme_genetique(G, population_size=50, generations=100, mutation_rate=0.01):
    """
    Algorithme génétique pour optimiser la tournée de livraison.

    :param G: Graphe
    :param population_size: Taille de la population
    :param generations: Nombre de générations
    :param mutation_rate: Taux de mutation
    :return: Liste des nœuds dans l'ordre de la tournée optimisée
    """
    def generate_initial_population(size):
        population = []
        nodes = list(G.nodes)
        for _ in range(size):
            random.shuffle(nodes)
            population.append(nodes[:])
        return population

    def crossover(parent1, parent2):
        start, end = sorted(random.sample(range(len(parent1)), 2))
        child = [None] * len(parent1)
        child[start:end] = parent1[start:end]
        index = end
        for city in parent2:
            if city not in child:
                child[index % len(parent1)] = city
                index += 1
        return child

    def mutate(tour):
        if random.random() < mutation_rate:
            i, j = random.sample(range(len(tour)), 2)
            tour[i], tour[j] = tour[j], tour[i]
        return tour

    def select(population):
        costs = [calculer_cout(G, tour) for tour in population]
        min_cost = min(costs)
        selected = [population[i] for i in range(len(population)) if costs[i] == min_cost]
        return random.choice(selected)

    population = generate_initial_population(population_size)
    best_tour = None
    best_cost = float('inf')

    for generation in range(generations):
        new_population = []
        for _ in range(population_size // 2):
            parent1 = select(population)
            parent2 = select(population)
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            new_population.extend([mutate(child1), mutate(child2)])
        population = new_population
        current_best_tour = select(population)
        current_best_cost = calculer_cout(G, current_best_tour)
        if current_best_cost < best_cost:
            best_cost = current_best_cost
            best_tour = current_best_tour

    return best_tour

# Lire les données depuis le fichier JSON et optimiser la tournée
graphe_from_json = lire_donnees('donnees_tournee.json')
tour_optimise = algorithme_genetique(graphe_from_json)
print("Tournée optimisée :", tour_optimise)
afficher_graphe(graphe_from_json, tour_optimise)