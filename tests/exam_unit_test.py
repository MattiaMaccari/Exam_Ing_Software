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


# TEST DELLA PRIMA PROCEDURA GREEDY

from exam.exam import greedy_minimum_opening_time

def test_greedy_minimum_opening_time():
    # Creo 3 nodi con tempi di apertura diversi
    node0 = {
        'id': 0,
        'opening_time': 0,
        'coordinates': (0, 0),
        'distance_vector': np.array([0, 5, 10])
    }
    node1 = {
        'id': 1,
        'opening_time': 5,
        'coordinates': (1, 1),
        'distance_vector': np.array([5, 0, 3])
    }
    node2 = {
        'id': 2,
        'opening_time': 12,
        'coordinates': (2, 2),
        'distance_vector': np.array([10, 3, 0])
    }

    nodes = [node2, node0, node1]  # ordine mescolato
    route = greedy_minimum_opening_time(nodes)

    # Verifico che l'ordine sia corretto (per opening_time)
    assert [n['id'] for n in route] == [0, 1, 2]

    # Verifico che idle e tardiness siano calcolati
    assert route[0]['idle_tardiness'] == (0, 0)
    assert isinstance(route[1]['idle_tardiness'], tuple)
    assert isinstance(route[2]['idle_tardiness'], tuple)


# TESTO IL FUNZIONAMENTO DELLA SECONDA GREEDY
from exam.exam import greedy_minimum_distance_from_zero

def test_greedy_minimum_distance_from_zero():
    # Creo 3 nodi con distanze diverse rispetto al nodo 0
    node0 = {
        'id': 0,
        'opening_time': 0,
        'coordinates': (0, 0),
        'distance_vector': np.array([0, 5, 10])
    }
    node1 = {
        'id': 1,
        'opening_time': 5,
        'coordinates': (1, 1),
        'distance_vector': np.array([5, 0, 3])
    }
    node2 = {
        'id': 2,
        'opening_time': 12,
        'coordinates': (2, 2),
        'distance_vector': np.array([10, 3, 0])
    }

    nodes = [node2, node0, node1]  # ordine mescolato
    route = greedy_minimum_distance_from_zero(nodes)

    # Verifico che l'ordine sia corretto (per distanza da nodo 0)
    assert [n['id'] for n in route] == [0, 1, 2]

    # Verifico che idle e tardiness siano presenti
    assert route[0]['idle_tardiness'] == (0, 0)
    assert isinstance(route[1]['idle_tardiness'], tuple)
    assert isinstance(route[2]['idle_tardiness'], tuple)


# TESTO IL FUNZIONAMENTO DELLA TERZA GREEDY

from exam.exam import nn_greedy

def test_nn_greedy_order_and_idle_tardiness():
    # Definizione dei nodi
    node0 = {
        'id': 0,
        'opening_time': 0,
        'coordinates': (0, 0),
        'distance_vector': np.array([0, 5, 10])
    }
    node1 = {
        'id': 1,
        'opening_time': 5,
        'coordinates': (1, 1),
        'distance_vector': np.array([5, 0, 3])
    }
    node2 = {
        'id': 2,
        'opening_time': 12,
        'coordinates': (2, 2),
        'distance_vector': np.array([10, 3, 0])
    }

    nodes = [node2, node0, node1]  # ordine mescolato
    route = nn_greedy(nodes)

    # Verifica ordine atteso: parte da 0, poi va al più vicino (1), poi 2
    expected_order = [2, 1, 0]
    actual_order = [n['id'] for n in route]
    assert actual_order == expected_order, f"Ordine atteso {expected_order}, ottenuto {actual_order}"

    # Verifica che ogni nodo abbia idle_tardiness
    for node in route:
        assert 'idle_tardiness' in node
        assert isinstance(node['idle_tardiness'], tuple)


# TESTO LA LOCAL SEARCH SWAP ADJACENT
from exam.exam import LS_swap_adjacent

def build_node(id, opening_time, coordinates, distance_vector):
    return {
        'id': id,
        'opening_time': opening_time,
        'coordinates': coordinates,
        'distance_vector': distance_vector,
        'idle_tardiness': (0, 0)
    }

def test_LS_swap_adjacent_improves_solution():
    # Distanze simmetriche tra 5 nodi
    d0 = np.array([0, 4, 8, 6, 9])
    d1 = np.array([4, 0, 5, 7, 6])
    d2 = np.array([8, 5, 0, 3, 4])
    d3 = np.array([6, 7, 3, 0, 2])
    d4 = np.array([9, 6, 4, 2, 0])

    istance = [
        build_node(0, 0, (0, 0), d0),   # base
        build_node(1, 5, (1, 1), d1),
        build_node(2, 10, (2, 2), d2),
        build_node(3, 15, (3, 3), d3),
        build_node(4, 20, (4, 4), d4)
    ]

    # Route iniziale subottimale: base → 4 → 3 → 2 → 1
    route = [istance[0], istance[4], istance[3], istance[2], istance[1]]

    # Calcolo valore obiettivo iniziale
    obj_val = calculate_objective(route, istance)

    # Applico local search
    new_route, new_obj_val, moves, info = LS_swap_adjacent(route, obj_val, istance)

    # Verifiche
    assert new_obj_val is not None
    assert new_obj_val < obj_val
    assert moves >= 1
    assert isinstance(info, list)
    assert [n['id'] for n in new_route][0] == 0  # parte dalla base
    assert sorted([n['id'] for n in new_route]) == [0, 1, 2, 3, 4]  # tutti i nodi presenti

    for node in new_route:
        assert isinstance(node['idle_tardiness'], tuple)
        assert len(node['idle_tardiness']) == 2


# TEST DELLA SECONDA PROCEDURA DI LOCAL SEARCH
from exam.exam import LSH_city_insert

def build_node(id, opening_time, coordinates, distance_vector):
    return {
        'id': id,
        'opening_time': opening_time,
        'coordinates': coordinates,
        'distance_vector': distance_vector,
        'idle_tardiness': (0, 0)
    }

def test_LSH_city_insert_improves_solution():
    print("Test eseguito")
    # Distanze simmetriche tra 5 nodi
    d0 = np.array([0, 4, 8, 6, 9])
    d1 = np.array([4, 0, 5, 7, 6])
    d2 = np.array([8, 5, 0, 3, 4])
    d3 = np.array([6, 7, 3, 0, 2])
    d4 = np.array([9, 6, 4, 2, 0])

    istance = [
        build_node(0, 0, (0, 0), d0),   # base
        build_node(1, 5, (1, 1), d1),
        build_node(2, 10, (2, 2), d2),
        build_node(3, 15, (3, 3), d3),
        build_node(4, 20, (4, 4), d4)
    ]

    # Route iniziale subottimale: base → 4 → 3 → 2 → 1
    route = [istance[0], istance[4], istance[3], istance[2], istance[1]]

    # Calcolo valore obiettivo iniziale
    obj_val = calculate_objective(route, istance)

    # Applico local search con H=2
    new_route, new_obj_val, moves, info = LSH_city_insert(route, obj_val, istance, H=2)

    # Verifiche
    assert new_obj_val is not None
    assert new_obj_val < obj_val
    assert moves >= 1
    assert isinstance(info, list)
    assert [n['id'] for n in new_route][0] == 0  # parte dalla base
    assert sorted([n['id'] for n in new_route]) == [0, 1, 2, 3, 4]  # tutti i nodi presenti

    # Verifica che ogni nodo abbia idle_tardiness aggiornato
    for node in new_route:
        assert isinstance(node['idle_tardiness'], tuple)
        assert len(node['idle_tardiness']) == 2



# TEST DELLA TERZA PROCEDURA DI LOCAL SEARCH

from exam.exam import LSH_city_insertT

def build_node(id, opening_time, coordinates, distance_vector):
    return {
        'id': id,
        'opening_time': opening_time,
        'coordinates': coordinates,
        'distance_vector': distance_vector,
        'idle_tardiness': (0, 0)
    }

def test_LSH_city_insertT_improves_solution():
    # Distanze simmetriche tra 5 nodi
    d0 = np.array([0, 4, 8, 6, 9])
    d1 = np.array([4, 0, 5, 7, 6])
    d2 = np.array([8, 5, 0, 3, 4])
    d3 = np.array([6, 7, 3, 0, 2])
    d4 = np.array([9, 6, 4, 2, 0])

    istance = [
        build_node(0, 0, (0, 0), d0),   # base
        build_node(1, 5, (1, 1), d1),
        build_node(2, 10, (2, 2), d2),
        build_node(3, 15, (3, 3), d3),
        build_node(4, 20, (4, 4), d4)
    ]

    # Route iniziale subottimale: base → 4 → 3 → 2 → 1
    route = [istance[0], istance[4], istance[3], istance[2], istance[1]]

    # Calcolo valore obiettivo iniziale
    obj_val = calculate_objective(route, istance)

    # Applico local search con H=2
    new_route, new_obj_val, moves, info = LSH_city_insertT(route, obj_val, istance, H=2)

    # Verifiche
    assert new_obj_val is not None
    assert new_obj_val < obj_val
    assert moves >= 1
    assert isinstance(info, list)
    assert [n['id'] for n in new_route][0] == 0  # parte dalla base
    assert sorted([n['id'] for n in new_route]) == [0, 1, 2, 3, 4]  # tutti i nodi presenti

    # Verifica che ogni nodo abbia idle_tardiness aggiornato
    for node in new_route:
        assert isinstance(node['idle_tardiness'], tuple)
        assert len(node['idle_tardiness']) == 2


# TESTO LA PRIMA TABU SEARCH
#istance = generate_tsp_instance(n=10, max_coordinate=200, seed_coordinates=3, seed_opening_times=4)
#route = greedy_minimum_opening_time(istance)
from exam.exam import tabu_search_city_insertAR

def build_node(id, opening_time, coordinates, distance_vector):
    return {
        'id': id,
        'opening_time': opening_time,
        'coordinates': coordinates,
        'distance_vector': distance_vector,
        'idle_tardiness': (0, 0)
    }

def test_tabu_search_city_insertAR_improves_solution():
    # Distanze simmetriche tra 5 nodi
    d0 = np.array([0, 4, 8, 6, 9])
    d1 = np.array([4, 0, 5, 7, 6])
    d2 = np.array([8, 5, 0, 3, 4])
    d3 = np.array([6, 7, 3, 0, 2])
    d4 = np.array([9, 6, 4, 2, 0])

    istance = [
        build_node(0, 0, (0, 0), d0),   # base
        build_node(1, 5, (1, 1), d1),
        build_node(2, 10, (2, 2), d2),
        build_node(3, 15, (3, 3), d3),
        build_node(4, 20, (4, 4), d4)
    ]
    # Route iniziale subottimale: base → 4 → 3 → 2 → 1
    route = [istance[0], istance[4], istance[3], istance[2], istance[1]]

    # Calcolo valore obiettivo iniziale
    obj_val = calculate_objective(route, istance)

    # Parametri Tabu
    tabu = 3
    stall = 10

    # Applico Tabu Search
    best_route, best_obj_val, info_current, info_best, best_tabu = tabu_search_city_insertAR(
        route, obj_val, istance, tabu, stall
    )

    # Lista contenente tutti i nodi
    listsorted = list(range(5))

    # Verifiche
    assert best_obj_val is not None
    assert best_obj_val <= obj_val
    assert isinstance(info_current, list)
    assert isinstance(info_best, list)
    assert isinstance(best_tabu, list)
    assert [n['id'] for n in best_route][0] == 0  # parte dalla base
    assert sorted([n['id'] for n in best_route]) == listsorted  # tutti i nodi presenti

    # Verifica che ogni nodo abbia idle_tardiness aggiornato
    for node in best_route:
        assert isinstance(node['idle_tardiness'], tuple)
        assert len(node['idle_tardiness']) == 2


# TEST DELLA SECONDA TABU SEARCH

from exam.exam import information_guided_tabu_searchAR

def build_node(id, opening_time, coordinates, distance_vector):
    return {
        'id': id,
        'opening_time': opening_time,
        'coordinates': coordinates,
        'distance_vector': distance_vector,
        'idle_tardiness': (0, 0)
    }

def test_information_guided_tabu_searchAR_improves_solution():
    # Distanze simmetriche tra 5 nodi
    d0 = np.array([0, 4, 8, 6, 9])
    d1 = np.array([4, 0, 5, 7, 6])
    d2 = np.array([8, 5, 0, 3, 4])
    d3 = np.array([6, 7, 3, 0, 2])
    d4 = np.array([9, 6, 4, 2, 0])

    istance = [
        build_node(0, 0, (0, 0), d0),   # base
        build_node(1, 5, (1, 1), d1),
        build_node(2, 10, (2, 2), d2),
        build_node(3, 15, (3, 3), d3),
        build_node(4, 20, (4, 4), d4)
    ]

    # Route iniziale subottimale: base → 4 → 3 → 2 → 1
    route = [istance[0], istance[4], istance[3], istance[2], istance[1]]

    # Calcolo valore obiettivo iniziale
    obj_val = calculate_objective(route, istance)

    # Parametri Tabu
    tabu = 3
    stall = 10

    # Applico Tabu Search guidata
    best_route, best_obj_val, info_current, info_best, best_tabu = information_guided_tabu_searchAR(
        route, obj_val, istance, tabu, stall
    )

    # Verifiche
    assert best_obj_val is not None
    assert best_obj_val <= obj_val
    assert isinstance(info_current, list)
    assert isinstance(info_best, list)
    assert isinstance(best_tabu, list)
    assert [n['id'] for n in best_route][0] == 0  # parte dalla base
    assert sorted([n['id'] for n in best_route]) == [0, 1, 2, 3, 4]  # tutti i nodi presenti

    # Verifica che ogni nodo abbia idle_tardiness aggiornato
    for node in best_route:
        assert isinstance(node['idle_tardiness'], tuple)
        assert len(node['idle_tardiness']) == 2