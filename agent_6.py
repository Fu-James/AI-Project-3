import math
import time
import numpy as np
from random import uniform, choice
from queue import Queue
from dataclasses import dataclass

from gridworld import GridWorld, Cell, Status
from astar_search import astar_search

@dataclass
class Node():
    pos: tuple
    distance: int

class Agent6:
    def __init__(self, maze: GridWorld, density: float,
                 false_negative_rates: list) -> None:
        self._density = density
        self._fnr = false_negative_rates
        self._maze = maze
        self._dim = maze.get_dim()

        self._knowledge = GridWorld(self._dim, False)
        self._belief_state = np.ones((self._dim, self._dim))
    
    def update_belief_state(self, cell: Cell, status: Status) -> None:
        if status == Status.Blocked:
            self._belief_state[cell.x, cell.y] = 0
        elif status == Status.Empty:
            pass
        elif status == Status.Examine:
            fnr = self._fnr[cell.get_terrain_type().value]
            self._belief_state[cell.x, cell.y] *= fnr
        else:
            raise ValueError('Status for calling get_scalar should be either blocked, empty, or examine')

    def get_neighbors(self, pos: tuple) -> list[tuple]:
        neighbors = []
        # N
        if pos[0] - 1 >= 0:
            neighbors.append((pos[0] - 1, pos[1]))
        # E
        if pos[1] + 1 < self._dim:
            neighbors.append((pos[0], pos[1] + 1))
        # S
        if pos[0] + 1 < self._dim:
            neighbors.append((pos[0] + 1, pos[1]))
        # W
        if pos[1] - 1 >= 0:
            neighbors.append((pos[0], pos[1] - 1))   
        return neighbors

    def breadth_first_search(self, start: tuple, target_value: np.float64) -> list:
        visited = set(start)
        queue: Queue[Node] = Queue()
        queue.put(Node(start, 0))
        targets = []

        while not queue.empty():
            node = queue.get()
            
            if math.isclose(self._belief_state[node.pos], target_value):
                target_distance = node.distance
                targets.append(node.pos)
                while not queue.empty:
                    node = queue.get()
                    if node.distance > target_distance:
                        return targets
                    if math.isclose(self._belief_state[node.pos], target_value):
                        targets.append(node.pos)
                break
            neighbors = self.get_neighbors(node.pos)
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.put(Node(neighbor, node.distance + 1))
        return targets

    
    def get_target(self, start: list) -> list:
        target_value = np.amax(self._belief_state)
        targets = self.breadth_first_search(tuple(start), target_value)
        if len(targets) < 1:
            raise Exception('Logical error in breadth_first_search()')
        return list(choice(targets))
        
    def examine(self, cell: Cell) -> bool:
        terrain_type = cell.get_terrain_type()
        return uniform(0, 1) > self._fnr[terrain_type.value] if cell.is_target() else False

    def execute(self, path: list[Cell]) -> list:
        for count, cell_in_knowledge in enumerate(path):
            cell_in_maze = self._maze.get_cell(cell_in_knowledge.x, cell_in_knowledge.y)
            if not cell_in_knowledge.isVisited:
                cell_in_knowledge.isVisited = True
                if cell_in_maze.is_blocked():
                    cell_in_knowledge.set_status(Status.Blocked)
                    self.update_belief_state(cell_in_knowledge, Status.Blocked)
                    return cell_in_knowledge.get_parent(), count - 1, 'blocked'
                else:
                    cell_in_knowledge.set_status(Status.Empty)
                    cell_in_knowledge.set_terrain_type(cell_in_maze.get_terrain_type())
                    self.update_belief_state(cell_in_knowledge, Status.Empty)

        if self.examine(cell_in_maze):
            return cell_in_knowledge, count, 'find goal'
        else:
            self.update_belief_state(cell_in_knowledge, Status.Examine)
            return cell_in_knowledge, count, 'examine failed'

    def solve(self, start: list, steps: int) -> list:
        examine_count = 0
        total_path = []
        time_to_find_goal = 0
        time_to_run_astar = 0
        astar_run_count = 0

        for _ in range(steps):
            while True:
                start_time = time.time_ns()
                goal = self.get_target(start)
                end_time = time.time_ns()
                time_to_find_goal += end_time - start_time

                start_time = time.time_ns()
                path = astar_search(start, goal, self._knowledge)
                end_time = time.time_ns()
                time_to_run_astar += end_time - start_time
                astar_run_count += 1

                if path != None:
                    break

                # If the cell is unreachable, we can assume the cell is blocked
                cell_in_knowledge = self._knowledge.get_cell(goal[0], goal[1])
                cell_in_knowledge.set_status(Status.Blocked)
                self.update_belief_state(cell_in_knowledge, Status.Blocked)

            end_cell, count, status_string = self.execute(path)

            start = [end_cell.x, end_cell.y]
            total_path.extend(path[1:count + 1])
            if status_string == 'find goal' or status_string == 'examine failed':
                examine_count += 1

            if status_string == 'find goal':
                print(f'A* search run {astar_run_count} times')
                print(f'time to run A* search: {time_to_run_astar}')
                print(f'time to guess goals: {time_to_find_goal}')
                return examine_count, total_path, status_string
        
        return examine_count, total_path, 'cannot find goal in limited steps'
    
    def print_belief_state(self) -> None:
        bs = ''
        for row in self._belief_state:
            bs += ' '.join(['{:.4}\t'.format(belief)
                                for belief in row]) + "\n"
        print(bs)
