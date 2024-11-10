import unittest
from helpers.merge_n_sorted_list import get_top_k_from_sorted_lists


class TestHelpers(unittest.TestCase):
    def test_get_top_k(self):
        sorted_lists = [
            [("a", 5), ("b", 4)],
            [("c", 6), ("d", 5)]
        ]

        result = get_top_k_from_sorted_lists(sorted_lists, 3)
        self.assertEqual(result, [('c', 6), ('a', 5), ('d', 5)])

        result_empty = get_top_k_from_sorted_lists([], 3)
        self.assertEqual(result_empty, [])

        # Test with k larger than total elements
        result_large_k = get_top_k_from_sorted_lists(sorted_lists, 5)
        self.assertEqual(result_large_k, [('c', 6), ('a', 5), ('d', 5), ('b', 4)])
