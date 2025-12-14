
import time
import unittest
import copy

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

# PARAMETRI ISTANZA

INSTANCE_PARAMS = dict(
    n=20,
    max_coordinate=100,
    max_opening_time=80,
    seed_coordinates=44,
    seed_opening_times=2
)

class Integration_test(unittest.TestCase):

    def test_full_integration_pipeline(self):
        
        # Genera istanza
        
        instance = generate_tsp_instance(**INSTANCE_PARAMS)
        assert len(instance) == 20
        assert instance[0]['id'] == 0

        for node in instance:
            self.assertIn('id', node)
            self.assertIn('coordinates', node)
            self.assertIn('opening_time', node)
            self.assertIn('distance_vector', node)
            self.assertEqual(len(node['distance_vector']), 20)

        #results = {}

        
        # GREEDY
        
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
            greedy_solutions[name] = (copy.deepcopy(route), fo)
            #results[name] = fo
            assert len(route) == 20
            assert fo > 0
            assert time.time() - start < 5

            if name == "greedy_opening":
                ids = [el["id"] for el in route]
                expected_route = [0, 18, 7, 2, 14, 4, 13, 8, 15, 16, 1, 19, 5, 11, 9, 12, 17, 3, 6, 10]
                self.assertEqual(expected_route, ids)
                self.assertEqual(fo, 9959)

            elif name == "greedy_dist0":
                ids = [el["id"] for el in route]
                expected_route = [0, 9, 4, 13, 1, 18, 17, 8, 5, 12, 15, 19, 6, 2, 3, 16, 14, 7, 11, 10]
                self.assertEqual(expected_route, ids)
                self.assertEqual(fo, 9656)

            else:
                ids = [el["id"] for el in route]
                expected_route = [0, 9, 4, 17, 5, 19, 2, 1, 18, 15, 6, 16, 14, 7, 11, 10, 12, 3, 8, 13]
                self.assertEqual(expected_route, ids)
                self.assertEqual(fo, 3952)
                

        # LOCAL SEARCH

        ls_methods = {
            "ls_swap": lambda r, fo: LS_swap_adjacent(r, fo, instance),
            "ls_insert": lambda r, fo: LSH_city_insert(r, fo, instance, H=5),
            "ls_insertT": lambda r, fo: LSH_city_insertT(r, fo, instance, H=5)
        }

        (start_route, start_fo) = greedy_solutions["greedy_opening"]

        for name, func in ls_methods.items():
            start = time.time()
            route, fo, moves, extra = func(start_route, start_fo)
            assert len(route) == 20
            assert fo > 0
            assert moves > 0
            assert isinstance(extra, list)
            assert time.time() - start < 10

            if name == "ls_swap":
                ids = [el["id"] for el in route]
                expected_route = [0, 18, 14, 7, 2, 4, 13, 8, 16, 15, 1, 5, 19, 11, 12, 9, 17, 6, 10, 3]
                self.assertEqual(expected_route, ids)
                self.assertEqual(fo, 7877)

            elif name == "ls_insert":
                ids = [el["id"] for el in route]
                expected_route = [0, 18, 1, 15, 6, 16, 10, 11, 14, 7, 5, 19, 2, 17, 4, 9, 13, 8, 3, 12]
                self.assertEqual(expected_route, ids)
                self.assertEqual(fo, 3333)

            else:
                ids = [el["id"] for el in route]
                expected_route = [0, 18, 1, 15, 6, 16, 10, 11, 14, 7, 5, 19, 2, 17, 4, 9, 13, 8, 3, 12]
                self.assertEqual(expected_route, ids)
                self.assertEqual(fo, 3333)

        
        # TABU SEARCH
        
        ts_methods = {
            "tabu_AR": tabu_search_city_insertAR,
            "info_guided_AR": information_guided_tabu_searchAR
        }

        (start_route, start_fo) = greedy_solutions["greedy_dist0"]

        for name, func in ts_methods.items():
            #start = time.time()
            route, val, curr, best, tabu = func(start_route, start_fo, instance, tabu=15, stall=4)
            assert len(route) == 20
            assert val > 0
            assert isinstance(curr, list)
            assert isinstance(best, list)
            assert isinstance(tabu, list)

            if name == "tabu_AR":
                ids = [el["id"] for el in route]
                expected_route = [0, 9, 4, 13, 18, 12, 3, 8, 1, 15, 6, 16, 10, 11, 14, 7, 5, 19, 2, 17]
                self.assertEqual(expected_route, ids)
                self.assertEqual(val, 5361)

            elif name == "info_guided_AR":
                ids = [el["id"] for el in route]
                expected_route = [0, 4, 9, 13, 18, 1, 15, 6, 16, 10, 11, 14, 7, 5, 19, 2, 17, 12, 3, 8]
                self.assertEqual(expected_route, ids)
                self.assertEqual(val, 3803)


        # ITERATED LOCAL SEARCH

        start = time.time()
        route, val, extra = IT_LS_INFORMATION_GUIDED(instance, max_iterations=60)

        assert len(route) == 20
        assert val > 0
        assert isinstance(extra, list)
            
