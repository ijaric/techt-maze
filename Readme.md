# Techt. Python Test Assginment

### Key components
1. Maze Generator (`mazegenerator.py`). Generates a maze using Eller’s algorithm.
2. Graph (`graph.py`). Represents the generated maze as a non-weighted graph.
3. Pathfinder (`pathfinder.py`). Gets the shortest path from a start to finish using A* algorithm.
4. Image Generator (`imagegenerator.py`). Saves the maze as png (`/images/maze.png`) and the solution of the maze as a gif (`/images/solution.gif`).

### Run
Run `main.py`.

### Configuration
You can set up the following in `main.py`: 
- size of the maze (`width` and `height`);
- start and finish points (`start_pos` and `finish_pos`);
- line thickness (`line_thickness`).

### Results
- `maze.png` and `solution.gif` in `/images`;
- image of the maze in a window (push any button to close);
- solution in another windows (push any button to close).