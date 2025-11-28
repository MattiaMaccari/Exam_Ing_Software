
import time

from exam.exam import (
    generate_tsp_instance,
    greedy_minimum_opening_time,
    greedy_minimum_distance_from_zero,
    nn_greedy,
    calculate_objective,
    LS_swap_adjacent,
    LSH_city_insert,
    LSH_city_insertT,
    tabu_search_city_insertAR,
    information_guided_tabu_searchAR,
    IT_LS_INFORMATION_GUIDED
)

# -----------------------------------------------------------
# PARAMETRI ISTANZA
# -----------------------------------------------------------
INSTANCE_PARAMS = dict(
    n=20,
    max_coordinate=200,
    seed_coordinates=3,
    seed_opening_times=4
)


def test_full_integration_pipeline():
    # -------------------------------------------------------
    # 1) Genera istanza
    # -------------------------------------------------------
    instance = generate_tsp_instance(**INSTANCE_PARAMS)
    assert len(instance) == 20
    assert instance[0]['id'] == 0

    results = {}

    # -------------------------------------------------------
    # 2) GREEDY
    # -------------------------------------------------------
    greedy_methods = {
        "greedy_opening": greedy_minimum_opening_time,
        "greedy_dist0": greedy_minimum_distance_from_zero,
        "greedy_nn": nn_greedy
    }

    greedy_solutions = {}

    for name, func in greedy_methods.items():
        start = time.time()
        route = func(instance)
        fo = calculate_objective(route, instance)
        greedy_solutions[name] = (route, fo)
        results[name] = fo
        assert len(route) == 20
        assert fo >= 0
        assert time.time() - start < 5


    # -------------------------------------------------------
    # 3) LOCAL SEARCH
    # -------------------------------------------------------
    ls_methods = {
        "ls_swap": lambda r, fo: LS_swap_adjacent(r, fo, instance),
        "ls_insert": lambda r, fo: LSH_city_insert(r, fo, instance, H=3),
        "ls_insertT": lambda r, fo: LSH_city_insertT(r, fo, instance, H=3)
    }

    start_route, start_fo = greedy_solutions["greedy_opening"]

    for name, func in ls_methods.items():
        start = time.time()
        route, fo, moves, extra = func(start_route, start_fo)
        results[name] = fo
        assert len(route) == 20
        assert fo >= 0
        assert moves >= 0
        assert isinstance(extra, list)
        assert time.time() - start < 10


    # -------------------------------------------------------
    # 4) TABU SEARCH
    # -------------------------------------------------------
    ts_methods = {
        "tabu_AR": tabu_search_city_insertAR,
        "info_guided_AR": information_guided_tabu_searchAR
    }

    for name, func in ts_methods.items():
        start = time.time()
        route, val, curr, best, tabu = func(start_route, start_fo, instance, tabu=10, stall=10)
        results[name] = val
        assert len(route) == 20
        assert val >= 0
        assert isinstance(curr, list)
        assert isinstance(best, list)
        assert isinstance(tabu, list)
        # assert time.time() - start < 20   # timeout accettabile


    # -------------------------------------------------------
    # 5) ITERATED LOCAL SEARCH
    # -------------------------------------------------------
    start = time.time()
    route, val, extra = IT_LS_INFORMATION_GUIDED(instance, max_iterations=60)
    results["ILS"] = val

    assert len(route) == 20
    assert val >= 0
    assert isinstance(extra, list)
    # assert time.time() - start < 20

    # -------------------------------------------------------
    # 6) Check finale risultati
    # -------------------------------------------------------
    #print("\n=== RISULTATI INTEGRATION TEST ===")
    #for k, v in results.items():
    #    print(f"{k:20s} → FO = {v}")

    #assert True  # se arrivi qui, tutto ok
