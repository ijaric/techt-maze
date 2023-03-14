import copy
import random


class Cell:
    def __init__(self, set: int, left_wall: int = 0, top_wall: int = 0, right_wall: int = 0, bottom_wall: int = 0):
        self.set = set
        self.left_wall = left_wall
        self.top_wall = top_wall
        self.right_wall = right_wall
        self.bottom_wall = bottom_wall


class MazeGenerator:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.rows = []

    def _get_unique_subsets(self, row):
        """Count size of each unique subset in a row"""
        new_row_set = {}
        for cell in row:
            new_row_set[cell.set] = 1 if cell.set not in new_row_set else new_row_set[cell.set] + 1
        return new_row_set

    def _assign_unique_subsets(self, row):
        """Generate unique subsets in a row"""
        new_row_set = self._get_unique_subsets(row)

        counter = 0 if row[0].set is None else row[0].set
        for i in range(len(row)):
            if row[i].set is None:
                while counter in new_row_set:
                    counter += 1
                row[i].set = counter
                counter += 1

    def _merge_subsets(self, subset, value_to_be, value_to_change):
        """Merge two subsets in a row"""
        # Cells belong to the same subset if they are connected
        for i in range(len(subset)):
            if subset[i].set == value_to_change:
                subset[i].set = value_to_be

        return subset

    def _build_right_walls(self, row):
        """Build right and left walls in a row, excpept for the last row"""
        for i in range(len(row) - 1):
            merge_cells = bool(random.getrandbits(1))
            # Cells belong to the same subset => Build vertical walls
            if row[i].set == row[i + 1].set:
                row[i].right_wall = 1
                row[i + 1].left_wall = 1
            elif merge_cells:
                # Merge subsets if NOT (that
                row = self._merge_subsets(row, row[i].set, row[i + 1].set)
            # If not merging cells => Build vertical walls
            else:
                row[i].right_wall = 1
                row[i + 1].left_wall = 1

    def _build_bottom_walls(self, row):
        """Build top and bottom walls in a row"""
        new_row_set = self._get_unique_subsets(row)

        for i in range(len(row)):
            build_wall = bool(random.getrandbits(1))
            # Build horizontal walls if it's allowed and random in favour of it
            if new_row_set[row[i].set] > 1 and build_wall:
                row[i].bottom_wall = 1
                new_row_set[row[i].set] -= 1

        return row

    def _build_right_walls_last_row(self, row):
        """Build right and left walls in the last row"""
        for i in range(len(row) - 1):
            # Merge cells if their are not belong to the same subset
            if row[i].set != row[i + 1].set:
                row = self._merge_subsets(row, row[i].set, row[i + 1].set)
                row[i].right_wall = 0
                row[i + 1].left_wall = 0
            # Build walls if cells belong to the same subset
            elif row[i].set == row[i + 1].set:
                row[i].right_wall = 1
                row[i + 1].left_wall = 1

    def _generate_row(self, previous_row, last_row=False):
        if previous_row is None:
            # Generate the first row
            new_row = [Cell(i, top_wall=1) for i in range(self.width)]
        else:
            # Copy previous row and prepare for a new row
            new_row = copy.deepcopy(previous_row)
            for cell in new_row:
                cell.right_wall = 0 if not last_row else cell.right_wall
                cell.left_wall = 0 if not last_row else cell.left_wall
                cell.top_wall = 0
                if cell.bottom_wall == 1:
                    cell.top_wall = 1
                    cell.set = None
                cell.bottom_wall = 0 if not last_row else 1

        new_row[0].left_wall = 1  # Each first cell in a row always has a left wall
        new_row[-1].right_wall = 1  # Each last cell in a row always has a right wall

        self._assign_unique_subsets(new_row)
        if not last_row:
            self._build_right_walls(new_row)
        else:
            self._build_right_walls_last_row(new_row)
        # Each cell at the last row has a bottom wall
        if not last_row:
            self._build_bottom_walls(new_row)

        self.rows.append(new_row)

    def generate(self):
        self._generate_row(None)
        for i in range(self.width - 2):
            self._generate_row(self.rows[-1])
        self._generate_row(self.rows[-1], True)

        return self.rows
