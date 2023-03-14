from pathfinder import Pathfinder
from graph import Graph
from imagegenerator import ImageGenerator
from mazegenerator import MazeGenerator

if __name__ == "__main__":
    width, height = 20, 20
    start_pos = [0, 0]  # Y, X
    finish_pos = [0, width - 1]  # Y, X
    line_thickness = 5

    # Generate a maze
    maze_object = MazeGenerator(width, height)
    maze = maze_object.generate()

    # Generate a graph based on the maze
    graph_object = Graph(maze)
    graph = graph_object.build()

    # Find solution for the graph (maze)
    pathfinder = Pathfinder(graph, start_pos, finish_pos)
    path = pathfinder.get_path()

    # Generate png, gif and show the maze & solution
    image_generator = ImageGenerator(maze, width, height, line_thickness)
    image_generator.save_maze_png()
    image_generator.show_maze()
    image_generator.save_solution_gif(path)
    image_generator.show_solution()
