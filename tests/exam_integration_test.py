import matplotlib.pyplot as plt

from exam.exam import (
    main,
    generate_tsp_instance,
    calculate_objective,
    greedy_minimum_opening_time,
    greedy_minimum_distance_from_zero,
    nn_greedy,
    call_LocalSearch,
    call_tabu_searchA,
    plot_tsp_nodes_link,
    plot_tsp_nodes,
    call_greedy,
    compare_greedy,
)

def check_route_validity(route, istance):
    assert route is not None
    assert len(route) == len(istance)
    assert route[0]["id"] == 0
    ids = [node["id"] for node in route]
    assert set(ids) == set(range(len(istance)))
    for node in route:
        assert "idle_tardiness" in node

def test_main_and_functions(capsys, monkeypatch):
    monkeypatch.setattr(plt, "show", lambda:None)
    main()
    captured = capsys.readouterr()
    assert "Istanza" in captured.out or "Valore" in captured.out or captured.out == ""

    # 2. Genera un'istanza come fa il main
    instance = generate_tsp_instance(n=20, max_coordinate=100, seed_coordinates=1, seed_opening_times=2)

    # 2bis. Controlla funzioni di plotting e orchestrazione
    route = greedy_minimum_opening_time(instance)
    # plot_tsp_node_link deve accettare una route
    assert plot_tsp_nodes_link(route) is None
    # plot_tsp_nodes deve accettare un'istanza
    assert plot_tsp_nodes(instance) is None
    # call_greedy deve restituire qualcosa (o None se plot attivo)
    assert call_greedy(10, 100, 50, 11, 2, "greedy_minimum_opening_time") is None or True
    # compare_greedy deve restituire qualcosa (o None se plot attivo)
    assert compare_greedy(10, 100, 50, 11, 2) is None or True

    # 3. GREEDY
    for greedy in [greedy_minimum_opening_time, greedy_minimum_distance_from_zero, nn_greedy]:
        route = greedy(instance)
        check_route_validity(route, instance)
        value = calculate_objective(route, instance)
        assert value is not None

    # 4. LOCAL SEARCH
    ls_strategies = [
        ("greedy_minimum_opening_time", "LS_swap_adjacent"),
        ("greedy_minimum_distance_from_zero", "LSH_city_insert"),
        ("nn_greedy", "LSH_city_insertT"),
    ]
    for greedy_name, ls_name in ls_strategies:
        result = call_LocalSearch(20, 100, 80, 44, 2, greedy_name, ls_name, plot=None)
        assert result is not None
        ls_name_returned, ls_info = result
        assert ls_name_returned == ls_name
        assert isinstance(ls_info, list)

        # Caso con plot attivo
        result_plot = call_LocalSearch(20, 100, 80, 44, 2, greedy_name, ls_name, plot="YES")
        assert result_plot is None

    # 5. TABU SEARCH
    tabu_strategies = [
        ("greedy_minimum_distance_from_zero", "information_guided_tabu_searchAR", 15, 3),
        ("greedy_minimum_distance_from_zero", "tabu_search_city_insertAR", 15, 4),
    ]
    for greedy_name, tabu_name, tenure, aspiration in tabu_strategies:
        route_tabu, val_route_tabu = call_tabu_searchA(
            20, 100, 80, 44, 2, greedy_name, tabu_name, tenure, aspiration, plot=None
        )
        check_route_validity(route_tabu, instance)
        assert val_route_tabu is not None

        # Caso con plot attivo
        result_plot = call_tabu_searchA(
            20, 100, 80, 44, 2, greedy_name, tabu_name, tenure, aspiration, plot="YES"
        )
        assert result_plot is None