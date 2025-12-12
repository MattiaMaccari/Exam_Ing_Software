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
        self.assertGreater(val, 0)

class TestGreedy(unittest.TestCase):
    def test_greedy_opening(self):
        instance = generate_tsp_instance(n=20, max_coordinate=100, max_opening_time=80, seed_coordinates=44, seed_opening_times=2)
        route = greedy_minimum_opening_time(instance)
        obj = calculate_objective(route, instance)
        self.assertEqual(len(route), 20)
        self.assertIsInstance(route, list)

        # Confronto la route attesa con la route restituita dalla greedy
        ids = [el["id"] for el in route]
        expected_route = [0, 18, 7, 2, 14, 4, 13, 8, 15, 16, 1, 19, 5, 11, 9, 12, 17, 3, 6, 10]
        self.assertEqual(expected_route, ids)
        expected_obj = 9959
        self.assertEqual(expected_obj, obj)


    def test_greedy_distance(self):
        instance = generate_tsp_instance(n=20, max_coordinate=100, max_opening_time=80, seed_coordinates=44, seed_opening_times=2)
        route = greedy_minimum_distance_from_zero(instance)
        obj = calculate_objective(route, instance)
        self.assertEqual(len(route), 20)
        self.assertIsInstance(route, list)

        # Confronto la route attesa ed il valore atteso della funzione obbiettivo della route con i valori della greedy
        ids = [el["id"] for el in route]
        expected_route = [0, 9, 4, 13, 1, 18, 17, 8, 5, 12, 15, 19, 6, 2, 3, 16, 14, 7, 11, 10]
        self.assertEqual(expected_route, ids)
        obj_expected = 9656
        self.assertEqual(obj_expected, obj)

    def test_nn_greedy(self):
        instance = generate_tsp_instance(n=20, max_coordinate=100, max_opening_time=80, seed_coordinates=44, seed_opening_times=2)
        route = nn_greedy(instance)
        obj = calculate_objective(route, instance)
        self.assertEqual(len(route), 20)
        self.assertIsInstance(route, list)

        # Confronto la route attesa ed il valore atteso della funzione obbiettivo della route con i valori della greedy
        ids = [el["id"] for el in route]
        expected_route = [0, 9, 4, 17, 5, 19, 2, 1, 18, 15, 6, 16, 14, 7, 11, 10, 12, 3, 8, 13] # Route attesa
        self.assertEqual(expected_route, ids)
        obj_expected = 3952                     # Valore funzione obbiettivo attesa
        self.assertEqual(obj_expected, obj)


class TestLocalSearch(unittest.TestCase):
    def test_ls_swap(self):
        instance = generate_tsp_instance(n=20, max_coordinate=100, max_opening_time=80, seed_coordinates=44, seed_opening_times=2)
        route = nn_greedy(instance)
        obj_val = calculate_objective(route, instance)
        new_route, fo, moves, extra = LS_swap_adjacent(route, obj_val, instance)
        self.assertEqual(len(new_route), 20)
        self.assertGreaterEqual(obj_val, fo)
        self.assertGreater(moves, 0)
        self.assertIsInstance(extra, list)

        ids = [el["id"] for el in new_route]
        expected_route = [0, 4, 9, 17, 5, 19, 2, 1, 18, 15, 6, 16, 14, 7, 11, 10, 12, 3, 8, 13]
        self.assertEqual(expected_route, ids)
        expected_obj = 3867
        self.assertEqual(expected_obj, fo)

    def test_ls_insert(self):
        instance = generate_tsp_instance(n=20, max_coordinate=100, max_opening_time=80, seed_coordinates=44, seed_opening_times=2)
        route = nn_greedy(instance)
        obj_val = calculate_objective(route, instance)
        new_route, fo, moves, extra = LSH_city_insert(route, obj_val, instance, H=5)
        self.assertEqual(len(new_route), 20)
        self.assertGreaterEqual(obj_val, fo)
        self.assertGreater(moves, 0)
        self.assertIsInstance(extra, list)

        ids = [el["id"] for el in new_route]
        expected_route = [0, 4, 9, 17, 5, 19, 2, 1, 18, 15, 6, 16, 14, 7, 11, 10, 12, 3, 8, 13]
        expected_obj = 3867
        self.assertEqual(expected_route, ids)
        self.assertEqual(expected_obj, fo)


    def test_ls_insert_tail(self):
        instance = generate_tsp_instance(n=20, max_coordinate=100, max_opening_time=80, seed_coordinates=44, seed_opening_times=2)
        route = nn_greedy(instance)
        obj_val = calculate_objective(route, instance)
        new_route, fo, moves, extra = LSH_city_insertT(route, obj_val, instance, H=5)
        self.assertEqual(len(new_route), 20)
        self.assertGreaterEqual(obj_val, fo)
        self.assertGreater(moves, 0)
        self.assertIsInstance(extra, list)

        ids = [el["id"] for el in new_route]
        expected_route = [0, 4, 9, 17, 5, 19, 2, 1, 18, 15, 6, 16, 14, 7, 11, 10, 12, 3, 8, 13]
        expected_obj = 3867
        self.assertEqual(expected_route, ids)
        self.assertEqual(expected_obj, fo)


class TestTabuSearch(unittest.TestCase):
    def test_tabu_city_insert(self):
        istance = generate_tsp_instance(n=20, max_coordinate=100, max_opening_time=80, seed_coordinates=44, seed_opening_times=2)
        route = greedy_minimum_distance_from_zero(istance)
        obj_val = calculate_objective(route, istance)
        best_route, fo, extra1, extra2, tabu = tabu_search_city_insertAR(route, obj_val, istance, tabu=15, stall=4)
        self.assertEqual(len(best_route), 20)
        self.assertIsInstance(fo, (int, float))
        self.assertGreaterEqual(obj_val, fo)
        self.assertIsInstance(extra1, list)
        self.assertIsInstance(extra2, list)
        self.assertIsInstance(tabu, list)

        ids = [el["id"] for el in best_route]
        expected_route = [0, 9, 4, 13, 18, 12, 3, 8, 1, 15, 6, 16, 10, 11, 14, 7, 5, 19, 2, 17]
        expected_obj = 5361
        self.assertEqual(expected_route, ids)
        self.assertEqual(expected_obj, fo)


    def test_information_guided_tabu(self):
        instance = generate_tsp_instance(n=20, max_coordinate=100, max_opening_time=80, seed_coordinates=44, seed_opening_times=2)
        route = greedy_minimum_distance_from_zero(instance)
        obj_val = calculate_objective(route, instance)
        best_route, fo, extra1, extra2, tabu  = information_guided_tabu_searchAR(route, obj_val, instance, tabu=15, stall=4)
        self.assertEqual(len(best_route), 20)
        self.assertIsInstance(fo, (int, float))
        self.assertGreaterEqual(obj_val, fo)
        self.assertIsInstance(extra1, list)
        self.assertIsInstance(extra2, list)
        self.assertIsInstance(tabu, list)

        ids = [el["id"] for el in best_route]
        expected_route = [0, 4, 9, 13, 18, 1, 15, 6, 16, 10, 11, 14, 7, 5, 19, 2, 17, 12, 3, 8]
        expected_obj = 3803
        self.assertEqual(expected_route, ids)
        self.assertEqual(expected_obj, fo)

class TestILS(unittest.TestCase):
    def test_ils(self):
        instance = generate_tsp_instance(n=20, max_coordinate=100, max_opening_time=80, seed_coordinates=44, seed_opening_times=2)
        best_route, fo, extra = IT_LS_INFORMATION_GUIDED(instance, max_iterations=5)
        self.assertEqual(len(best_route), 20)
        self.assertIsInstance(fo, (int,float))
        self.assertIsInstance(extra, list)

if __name__ == '__main__':
    unittest.main()
