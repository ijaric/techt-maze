import io
import os
from time import sleep

import cv2 as cv
import imageio
import numpy as np

from graph import Cell


class ImageGenerator():
    def __init__(self, maze: list[list[Cell]], width: int, height: int, line_thickness: int):
        self.maze = maze
        self.width = width
        self.height = height
        self.line_thickness = line_thickness
        self.cell_size = 20

    def _get_maze_image(self) -> np.ndarray:
        image_size = [self.width * self.cell_size, self.height * self.cell_size]
        img = np.zeros([image_size[0], image_size[1], 3], dtype=np.uint8)
        img.fill(255)

        start_point = (0, 0)
        end_point = (self.width * self.cell_size, self.height * self.cell_size)
        cv.rectangle(img, start_point, end_point, (0, 0, 0), self.line_thickness)

        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                if self.maze[y][x].right_wall == 1:
                    vertical_pos_a = [(x + 1) * self.cell_size, y * self.cell_size]
                    vertical_pos_b = [(x + 1) * self.cell_size, (y + 1) * self.cell_size]
                    cv.line(img, vertical_pos_a, vertical_pos_b, (0, 0, 0), thickness=self.line_thickness)

                if self.maze[y][x].bottom_wall == 1:
                    horizontal_pos_a = [x * self.cell_size, (y + 1) * self.cell_size]
                    horizontal_pos_b = [(x + 1) * self.cell_size, (y + 1) * self.cell_size]
                    cv.line(img, horizontal_pos_a, horizontal_pos_b, (0, 0, 0), thickness=self.line_thickness)

        return img

    def save_maze_png(self):
        image = self._get_maze_image()
        cv.imwrite("./images/maze.png", image)

    def show_maze(self):
        image = self._get_maze_image()
        cv.imshow("Maze", image)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def save_solution_gif(self, path: list[list[int]]):
        image = self._get_maze_image()
        frames = []
        half_cell = self.cell_size / 2
        for i in range(len(path) - 1):
            pos_a = (int(path[i][1] * self.cell_size + half_cell),
                     int(path[i][0] * self.cell_size + half_cell))
            pos_b = (int(path[i + 1][1] * self.cell_size + half_cell),
                     int(path[i + 1][0] * self.cell_size + half_cell))

            cv.line(image, pos_a, pos_b, (255, 0, 0), thickness=self.line_thickness)

            is_success, buffer = cv.imencode(".png", image)
            io_buf = io.BytesIO(buffer)
            frame = imageio.v3.imread(io_buf, index=None)
            frames.append(frame)

        imageio.v3.imwrite("./images/solution.gif", frames)

    def show_solution(self):
        filepath = "./images/solution.gif"
        if os.path.isfile(filepath):
            cap = cv.VideoCapture(filepath)
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break
                cv.imshow("Maze Solution", frame)
                sleep(0.05)
                if cv.waitKey(1) == ord("q"):
                    break
            cap.release()
            cv.destroyAllWindows()
        else:
            raise Exception("Generate solution before")
