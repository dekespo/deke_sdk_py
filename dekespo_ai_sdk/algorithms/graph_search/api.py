import sys

from dekespo_ai_sdk.core.utils import error_print
from dekespo_ai_sdk.core.graph import Graph

from dekespo_ai_sdk.algorithms.graph_search.depth_first_search import (
    DepthFirstSearch,
    DepthFirstSearchData,
)


class GraphSearch:
    class AStarFunctions:
        def __init__(self, heuristic_function, weight_function):
            self.heuristic_function = heuristic_function
            self.weight_function = weight_function

        # TODO: Generalise the parameters
        def run_heuristic_function(self, position1, position2):
            return self.heuristic_function(position1, position2)

        def run_weight_function(self, position1, position2):
            return self.weight_function(position1, position2)

    def __init__(self, graph: Graph, start_point):
        self.graph = graph
        self.start_point = start_point

    def _get_available_neighbours(self, point, neighbour_data):
        return self.graph.get_available_neighbours(point, neighbour_data)

    def depth_first_search(
        self, neighbour_data, depth_size=sys.maxsize, runs_with_thread=False
    ):
        dfs_data = DepthFirstSearchData(
            self.start_point,
            self._get_available_neighbours,
            neighbour_data,
            depth_size,
        )
        dfs = DepthFirstSearch(dfs_data, runs_with_thread)
        return dfs

    def breadth_first_search(self, neighbour_data):
        closed_set = []
        open_set = [self.start_point]
        while open_set:
            current_point = open_set.pop(0)
            if current_point not in closed_set:
                closed_set.append(current_point)
                for new_candidate_point, _ in self._get_available_neighbours(
                    current_point, neighbour_data
                ).items():
                    open_set.append(new_candidate_point)
        return closed_set

    def dijkstra_search(self, end_point, weight_function, neighbour_data):
        no_heuristic_function = lambda *_: 0
        a_star_functions = GraphSearch.AStarFunctions(
            heuristic_function=no_heuristic_function, weight_function=weight_function
        )
        return self.a_star_search(end_point, a_star_functions, neighbour_data)

    # pylint: disable=too-many-locals
    def a_star_search(self, end_point, a_star_functions, neighbour_data):
        def _reconstruct_path(came_from, current_point):
            total_path = [current_point]
            while current_point in came_from:
                current_point = came_from[current_point]
                total_path.append(current_point)
            total_path.reverse()
            return total_path

        def _initialize_a_star():
            closed_set = []
            open_set = [self.start_point]
            came_from = {}
            g_score = {}
            f_score = {}
            g_score[self.start_point] = 0
            f_score[self.start_point] = g_score[
                self.start_point
            ] + a_star_functions.run_heuristic_function(self.start_point, end_point)
            return closed_set, open_set, came_from, f_score, g_score

        def _get_minimum_f_score_index(open_set, f_score):
            minimum = float("inf")
            current = None
            for point in open_set:
                if f_score[point] < minimum:
                    minimum = f_score[point]
                    current = point
            return current

        closed_set, open_set, came_from, f_score, g_score = _initialize_a_star()

        while open_set:

            current_point = _get_minimum_f_score_index(open_set, f_score)
            if current_point == end_point:
                return _reconstruct_path(came_from, current_point)

            open_set.remove(current_point)
            closed_set.append(current_point)

            for new_candidate_point, _ in self._get_available_neighbours(
                current_point, neighbour_data
            ).items():
                if new_candidate_point not in closed_set:
                    tentative_g_score = g_score[
                        current_point
                    ] + a_star_functions.run_weight_function(
                        new_candidate_point, current_point
                    )
                    if new_candidate_point not in open_set:
                        open_set.append(new_candidate_point)
                        came_from[new_candidate_point] = current_point
                        g_score[new_candidate_point] = tentative_g_score
                        f_score[new_candidate_point] = g_score[
                            new_candidate_point
                        ] + a_star_functions.run_heuristic_function(
                            new_candidate_point, end_point
                        )
                    else:
                        # TODO: It looks like it never passes this one
                        if tentative_g_score < g_score[new_candidate_point]:
                            came_from[new_candidate_point] = current_point
                            g_score[new_candidate_point] = tentative_g_score
                            f_score[new_candidate_point] = g_score[
                                new_candidate_point
                            ] + a_star_functions.run_heuristic_function(
                                new_candidate_point, end_point
                            )
        error_print("A* cannot find the path, returning None")
        return []
