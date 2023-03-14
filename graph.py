from mazegenerator import Cell


class Node:
    """Node (vertex) to represent a maze as a non-weighted graph"""

    def __init__(self, coords: list[int]):
        self.coords = coords
        self.children = []
        self.parent = None
        self.total_distance = float('inf')
        self.covered_distance = float('inf')
        self.heuristic_distance = float('inf')

    # Connected cells
    def add_child(self, child):
        self.children.append(child)

    # This method is required for PriorityQueue to work
    def __gt__(self, other):
        return self.total_distance > other.total_distance


class Graph:
    # Non-weighted graph (each step is 1)
    def __init__(self, maze: list[list[Cell]]):
        self.maze = maze

    def build(self) -> dict:
        nodes = {}
        # Create nodes (vertices)
        for y_pos in range(len(self.maze)):
            for x_pos in range(len(self.maze[y_pos])):
                node = Node([y_pos, x_pos])
                nodes[(y_pos, x_pos)] = node

        # Add children to each node
        for y_pos in range(len(self.maze)):
            for x_pos in range(len(self.maze[y_pos])):
                if self.maze[y_pos][x_pos].top_wall == 0:
                    nodes[(y_pos, x_pos)].add_child(nodes[(y_pos - 1, x_pos)])
                if self.maze[y_pos][x_pos].bottom_wall == 0:
                    nodes[(y_pos, x_pos)].add_child(nodes[(y_pos + 1, x_pos)])
                if self.maze[y_pos][x_pos].left_wall == 0:
                    nodes[(y_pos, x_pos)].add_child(nodes[(y_pos, x_pos - 1)])
                if self.maze[y_pos][x_pos].right_wall == 0:
                    nodes[(y_pos, x_pos)].add_child(nodes[(y_pos, x_pos + 1)])

        return nodes
