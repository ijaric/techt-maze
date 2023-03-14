from queue import PriorityQueue

from graph import Node


class Pathfinder:
    """Search for the shortest path for a non-weighted graph (A* algorithm)"""

    def __init__(self, graph: dict[tuple, Node], start_pos: list[int], finish_pos: list[int]):
        self.graph = graph
        self.start_pos = start_pos
        self.finish_pos = finish_pos

    def _get_manhatten_distance(self, start_pos: list[tuple[int, int]], finish_pos: list[tuple[int, int]]) -> int:
        """Get Manhattan distance between two points"""
        distance = abs(finish_pos[0] - start_pos[0]) + abs(finish_pos[1] - start_pos[1])
        return distance

    def _astar(self):
        """ Search for the shortest path in a non-weighted graph using A* algorithm"""
        open_list = PriorityQueue()
        visited_list = set()

        # Set up the first (starting) node
        start_node = self.graph[tuple(self.start_pos)]
        start_node.covered_distance = 0
        start_node.heuristic_distance = self._get_manhatten_distance(self.start_pos, self.finish_pos)
        start_node.total_distance = start_node.heuristic_distance + start_node.covered_distance

        open_list.put((start_node.total_distance, start_node))

        while not open_list.empty():
            current_node = open_list.get()[1]

            # Break cycle if the path is found
            if current_node.coords == self.finish_pos:
                break

            # Add (update) children to the priority queue weighed by approx distance to finish
            for child in current_node.children:
                if child not in visited_list:
                    temp_heuristic_distance = self._get_manhatten_distance(child.coords, self.finish_pos)
                    temp_covered_distance = current_node.covered_distance + 1
                    temp_total_distance = temp_heuristic_distance + temp_covered_distance

                    if temp_total_distance < child.total_distance:
                        child.heuristic_distance = temp_heuristic_distance
                        child.covered_distance = temp_covered_distance
                        child.total_distance = temp_total_distance
                        child.parent = current_node
                        open_list.put((child.total_distance, child))

            visited_list.add(current_node)

    def get_path(self) -> list[int]:
        """ Get the shortest path between start and finish points using A* algorithm"""
        self._astar()

        path = []
        parent = self.finish_pos
        while self.graph[tuple(parent)].parent is not None:
            path.append(parent)
            parent = self.graph[tuple(parent)].parent.coords

        path.append(self.start_pos)
        path.reverse()
        return path
