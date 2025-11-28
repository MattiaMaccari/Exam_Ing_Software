import unittest

from exam.exam import (
    generate_tsp_instance,
    calculate_objective,
    greedy_minimum_opening_time,
    greedy_minimum_distance_from_zero,
    nn_greedy,
    LS_swap_adjacent,
    LSH_city_insert,
    tabu_search_city_insertAR,
    IT_LS_INFORMATION_GUIDED,
    information_guided_tabu_searchAR,
    LSH_city_insertT,
)

class TestGenerateInstance(unittest.TestCase):
    def test_instance_structure(self):
        instance = generate_tsp_instance(10, 200, 3, 4)
        self.assertEqual(len(instance), 10)
        for node in instance:
            self.assertIn('id', node)
            self.assertIn('coordinates', node)
            self.assertIn('opening_time', node)
            self.assertIn('distance_vector', node)
            self.assertEqual(len(node['distance_vector']), 10)

class TestObjective(unittest.TestCase):
    def test_objective_validity(self):
        instance = generate_tsp_instance(n=5, max_coordinate=200, seed_coordinates=3, seed_opening_times=4)
        route = greedy_minimum_distance_from_zero(instance)
        val = calculate_objective(route, instance)
        self.assertIsInstance(val, (int, float))
        self.assertGreaterEqual(val, 0)

class TestGreedy(unittest.TestCase):
    def test_greedy_opening(self):
        instance = generate_tsp_instance(20, 200, 3, 4)
        route = greedy_minimum_opening_time(instance)
        self.assertEqual(len(route), 20)

    def test_greedy_distance(self):
        instance = generate_tsp_instance(20, 200, 3, 4)
        route = greedy_minimum_distance_from_zero(instance)
        self.assertEqual(len(route), 20)

    def test_nn_greedy(self):
        instance = generate_tsp_instance(20, 200, 3, 4)
        route = nn_greedy(instance)
        self.assertEqual(len(route), 20)

class TestLocalSearch(unittest.TestCase):
    def test_ls_swap(self):
        instance = generate_tsp_instance(n=20, max_coordinate=200, seed_coordinates=3, seed_opening_times=4)
        route = nn_greedy(instance)
        obj_val = calculate_objective(route, instance)
        new_route, fo, _, _ = LS_swap_adjacent(route, obj_val, instance)
        self.assertEqual(len(new_route), 20)

    def test_ls_insert(self):
        instance = generate_tsp_instance(n=20, max_coordinate=200, seed_coordinates=3, seed_opening_times=4)
        route = nn_greedy(instance)
        obj_val = calculate_objective(route, instance)
        new_route, fo, _, _ = LSH_city_insert(route, obj_val, instance, H=5)
        self.assertEqual(len(new_route), 20)

    def test_ls_insert_tail(self):
        # NUOVO TEST: verifica della variante "tail" della local search
        instance = generate_tsp_instance(n=20, max_coordinate=200, seed_coordinates=3, seed_opening_times=4)
        route = nn_greedy(instance)
        obj_val = calculate_objective(route, instance)
        new_route, fo, _, _ = LSH_city_insertT(route, obj_val, instance, H=5)
        self.assertEqual(len(new_route), 20)
        self.assertIsInstance(fo, (int, float))

class TestTabuSearch(unittest.TestCase):
    def test_tabu(self):
        istance = generate_tsp_instance(10, 200, 3, 4)
        route = nn_greedy(istance)
        obj_val = calculate_objective(route, istance)
        best_route, fo, _, _, _ = tabu_search_city_insertAR(route, obj_val, istance, tabu=15, stall=4)
        self.assertEqual(len(best_route), 10)

    def test_information_guided_tabu(self):
        # NUOVO TEST: verifica della variante information-guided della Tabu Search
        instance = generate_tsp_instance(10, 200, 3, 4)
        route = nn_greedy(instance)
        obj_val = calculate_objective(route, instance)
        best_route, best_fo, _, _, _  = information_guided_tabu_searchAR(route, obj_val, instance, tabu=15, stall=4)
        self.assertEqual(len(best_route), 10)
        self.assertIsInstance(best_fo, (int, float))

class TestILS(unittest.TestCase):
    def test_ils(self):
        instance = generate_tsp_instance(n=20, max_coordinate=200, seed_coordinates=3, seed_opening_times=4)
        best_route, _, _ = IT_LS_INFORMATION_GUIDED(instance, max_iterations=5)
        self.assertEqual(len(best_route), 20)

if __name__ == '__main__':
    unittest.main()
