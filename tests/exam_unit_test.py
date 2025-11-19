# TESTO LA PRIMA FUNZIONE CHE GENERA LE ISTANZE DATI I SEMI.

import numpy as np
from exam.exam import generate_tsp_instance

def test_output_structure():
    nodes = generate_tsp_instance(n=3, seed_coordinates=42, seed_opening_times=99)
    assert isinstance(nodes, list)
    assert len(nodes) == 3
    for i, node in enumerate(nodes):
        assert isinstance(node, dict)
        assert set(node.keys()) == {'id', 'opening_time', 'coordinates', 'distance_vector'}
        assert node['id'] == i
        assert isinstance(node['coordinates'], tuple)
        assert isinstance(node['opening_time'], int)
        assert isinstance(node['distance_vector'], np.ndarray)
        assert node['distance_vector'].shape == (3,)

def test_distance_symmetry_and_diagonal():
    nodes = generate_tsp_instance(n=4, seed_coordinates=123)
    matrix = np.array([node['distance_vector'] for node in nodes])
    assert np.allclose(matrix, matrix.T), "La matrice deve essere simmetrica"
    assert np.all(np.diag(matrix) == 0), "La diagonale deve essere tutta zero"

def test_reproducibility_with_seeds():
    nodes1 = generate_tsp_instance(n=5, seed_coordinates=1, seed_opening_times=2)
    nodes2 = generate_tsp_instance(n=5, seed_coordinates=1, seed_opening_times=2)

    for n1, n2 in zip(nodes1, nodes2):
        assert n1['id'] == n2['id']
        assert n1['opening_time'] == n2['opening_time']
        assert n1['coordinates'] == n2['coordinates']
        assert np.allclose(n1['distance_vector'], n2['distance_vector']), "I vettori di distanza devono essere uguali"

def test_opening_time_first_zero():
    nodes = generate_tsp_instance(n=5, seed_opening_times=42)
    assert nodes[0]['opening_time'] == 0, "Il primo nodo deve avere opening_time = 0"


# TEST DELLA FUNZIONE CHE PRINTA LE ISTANZE

from exam.exam import print_istance

def test_print_istance_output(capsys):
    nodes = [
        {
            'id': 0,
            'opening_time': 5,
            'coordinates': (10, 20),
            'distance_vector': [0, 7, 9]
        },
        {
            'id': 1,
            'opening_time': 3,
            'coordinates': (30, 40),
            'distance_vector': [7, 0, 5]
        }
    ]

    print_istance(nodes)

    captured = capsys.readouterr()
    output = captured.out

    assert "ID: 0" in output
    assert "Opening Time: 5" in output
    assert "Coordinates: (10, 20)" in output
    assert "Distance Vector: [0, 7, 9]" in output
    assert "ID: 1" in output
    assert "Opening Time: 3" in output


# TESTO LA FUNZIONE DI STAMPA DEI NODI DEL TSP
from matplotlib.collections import PathCollection
import matplotlib.pyplot as plt
from exam.exam import plot_tsp_nodes

def test_plot_tsp_nodes():
    nodes = [
        {'id': 0, 'coordinates': (10, 20), 'opening_time': 0, 'distance_vector': [0, 1]},
        {'id': 1, 'coordinates': (30, 40), 'opening_time': 5, 'distance_vector': [1, 0]},
    ]

    # Pulizia figure precedenti
    plt.close('all')

    plot_tsp_nodes(nodes)

    fig = plt.gcf()  # Get current figure
    ax = plt.gca()   # Get current axes

    # Verifica base
    assert fig.get_size_inches()[0] == 6
    assert fig.get_size_inches()[1] == 6
    assert ax.get_title() == "TSP Nodes Visualization"
    assert ax.get_xlabel() == "X Coordinate"
    assert ax.get_ylabel() == "Y Coordinate"

    # Verifica che ci siano 2 scatter plot
    
    scatter_points = [child for child in ax.get_children() if isinstance(child, PathCollection)]
    assert len(scatter_points) >= 2

    # Verifica che ci sia almeno un testo (label del nodo)
    texts = [child for child in ax.get_children() if isinstance(child, plt.Text)]
    assert any("1" in t.get_text() for t in texts)


# TESTO LA FUNZIONE CHE CALCOLA IL VALORE DELLA FUNZIONE OBBIETTIVO

# tests/test_calculate_objective.py
import numpy as np
from exam.exam import calculate_objective

def build_node(id, opening_time, coordinates, distance_vector):
    return {
        'id': id,
        'opening_time': opening_time,
        'coordinates': coordinates,
        'distance_vector': distance_vector
    }

def test_valid_solution():
    # 3 nodi: base + 2 clienti
    d0 = np.array([0, 10, 20])
    d1 = np.array([10, 0, 15])
    d2 = np.array([20, 15, 0])

    istance = [
        build_node(0, 0, (0, 0), d0),
        build_node(1, 5, (1, 1), d1),
        build_node(2, 10, (2, 2), d2)
    ]

    # Route: base → 1 → 2
    route = [istance[0], istance[1], istance[2]]

    value = calculate_objective(route, istance)
    # distanza: 0→1 (10) + 1→2 (15) + 2→0 (20) = 45
    # tardiness: arrivo a 1 = 10, apertura 5 → 5 di ritardo
    #            arrivo a 2 = 25, apertura 10 → 15 di ritardo
    # totale = 45 + 5 + 15 = 65
    assert value == 65

def test_missing_node_in_route():
    istance = [
        build_node(0, 0, (0, 0), np.array([0, 1])),
        build_node(1, 5, (1, 1), np.array([1, 0]))
    ]
    route = [istance[0]]  # manca il nodo 1
    assert calculate_objective(route, istance) is None

def test_wrong_start_node():
    istance = [
        build_node(0, 0, (0, 0), np.array([0, 1])),
        build_node(1, 5, (1, 1), np.array([1, 0]))
    ]
    route = [istance[1], istance[0]]  # parte da nodo 1
    assert calculate_objective(route, istance) is None

def test_node_not_included():
    istance = [
        build_node(0, 0, (0, 0), np.array([0, 1, 2])),
        build_node(1, 5, (1, 1), np.array([1, 0, 3])),
        build_node(2, 10, (2, 2), np.array([2, 3, 0]))
    ]
    route = [istance[0], istance[1], build_node(99, 0, (0, 0), np.array([0, 0, 0]))]
    assert calculate_objective(route, istance) is None