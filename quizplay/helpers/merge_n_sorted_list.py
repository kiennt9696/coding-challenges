from heapq import heappush, heappop
from typing import List, Tuple


def get_top_k_from_sorted_lists(sorted_lists: List[List[Tuple[str, int]]], k: int) -> List[Tuple[str, int]]:
    """
    Get top K elements from multiple sorted lists in descending order.
    Time Complexity: O(k * log(n)) where n is number of lists
    Space Complexity: O(n) for heap + O(k) for result

    Args:
        sorted_lists: List of sorted lists, each containing (string, score) tuples
        k: Number of top elements to return

    Returns:
        List of top K (string, score) tuples in descending order
    """
    # Min heap to store (-score, string, list_index, element_index)
    # Using negative score to convert max heap to min heap
    heap = []
    result = []

    # Initialize heap with first element from each list
    for list_index, sorted_list in enumerate(sorted_lists):
        if sorted_list:  # Check if list is not empty
            score = sorted_list[0][1]
            string = sorted_list[0][0]
            heappush(heap, (-score, string, list_index, 0))

    # Get top K elements
    while heap and len(result) < k:
        neg_score, string, list_index, element_index = heappop(heap)
        result.append((string, -neg_score))  # Convert score back to positive

        # If there are more elements in this list, add the next one
        if element_index + 1 < len(sorted_lists[list_index]):
            next_element = sorted_lists[list_index][element_index + 1]
            heappush(heap, (-next_element[1], next_element[0], list_index, element_index + 1))
    return result