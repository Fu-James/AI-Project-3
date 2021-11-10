from math import dist
import numpy as np
from numpy.core.fromnumeric import amin
from random import randrange, uniform
import time
from queue import PriorityQueue
from dataclasses import dataclass, field

from gridworld import GridWorld, Cell, Status, TerrainType
from astar_search import astar_search

@dataclass(order=True)
class Node():
    distance: int
    pos: tuple = field(compare=False)

class Agent6:
    def __init__(self, maze: GridWorld, density: float,
                 false_negative_rates: list) -> None:
        self._density = density
        self._fnr = false_negative_rates
        self._maze = maze
        self._dim = maze.get_dim()

        self._knowledge = GridWorld(self._dim, False)
        self._belief_state = np.array([[(1 / (self._dim ** 2)) for _ in range(self._dim)] 
                              for _ in range(self._dim)])
    
    def update_belief_state(self, scalar: float) -> None:
        self._belief_state *= scalar

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

    def get_target(self, start: list) -> list:
        maximum = np.amax(self._belief_state)
        max_list = []    
        start = tuple(start)
        visited = set(start)
        queue = PriorityQueue()
        queue.put(Node(0, start))

        while not queue.empty():
            node = queue.get()
            pos = node.pos
            distance = node.distance

            if self._belief_state[pos] == maximum:
                max_list.append(pos)
                while not queue.empty():
                    node = queue.get()
                    if node.distance != distance:
                        break
                    if self._belief_state[node.pos] == maximum:
                        max_list.append(node.pos)
                break
            
            neighbors = self.get_neighbors(pos)
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.put(Node(distance + 1, neighbor))
                    visited.add(neighbor)

        return list(max_list[randrange(len(max_list))])

    def get_potential_target(self, start: list) -> list:
        targets_pos = np.argwhere(self._belief_state == np.amax(self._belief_state))
        if len(targets_pos) == 1:
            return list(targets_pos[0])
        
        targets_distance = [np.sum(np.abs(target_pos - start)) 
                            for target_pos in targets_pos]
        min_distance_pos = np.nonzero(targets_distance == np.amin(targets_distance))
        targets_pos = targets_pos[min_distance_pos]
        if len(targets_pos) == 1:
            return list(targets_pos[0])

        return list(targets_pos[randrange(len(targets_pos))])

    def get_scalar(self, belief: float, status: Status, terrain_type: TerrainType = None):
        if status == Status.Blocked:
            return 1 / (1 - belief)
        elif status == Status.Examine:
            return (1 - self._fnr[terrain_type.value] * belief) / (1 - belief)
        else:
            raise ValueError('Status for calling get_scalar should be either blocked or examine')
        
    def examine(self, cell: Cell, terrain_type: TerrainType) -> bool:
        return uniform(0, 1) > self._fnr[terrain_type.value] if self._maze.get_cell(cell.x, cell.y).is_target() else False
        #return bool(self._maze.get_cell(cell.x, cell.y).is_target() * self._fnr[terrain_type.value])

    def execute(self, path: list[Cell]) -> list:
        for count, cell in enumerate(path):
            cell_in_maze = self._maze.get_cell(cell.x, cell.y)
            cell_in_knowledge = self._knowledge.get_cell(cell.x, cell.y)
            if not cell_in_knowledge.isVisited:
                cell_in_knowledge.isVisited = True
                if cell_in_maze.is_blocked():
                    cell_in_knowledge.set_status(Status.Blocked)
                    self.update_belief_state(self.get_scalar(self._belief_state[cell.x][cell.y], 
                                                            Status.Blocked))
                    self._belief_state[cell.x, cell.y] = 0
                    return cell.get_parent(), count - 1, 'blocked'
                else:
                    cell_in_knowledge.set_status(Status.Empty)

        cell = path[-1]
        terrain_type = self._maze.get_cell(cell.x, cell.y).get_terrain_type()
        if self.examine(cell, terrain_type):
            return cell, count, 'find goal'
        else:
            belief = self._belief_state[cell.x][cell.y]
            self.update_belief_state(self.get_scalar(belief, Status.Examine, terrain_type))
            self._belief_state[cell.x, cell.y] = belief * self._fnr[terrain_type.value]
            return cell, count, 'examine failed'

    def solve(self, start: list, steps: int) -> list:
        examine_count = 0
        total_path = []
        time_to_find_goal = 0
        for _ in range(steps):
            goal = []
            path = []
            while True:
                start_time = time.time_ns()
                goal = self.get_target(start)
                end_time = time.time_ns()
                time_to_find_goal += end_time - start_time
                path = astar_search(self._knowledge.get_cell(start[0], start[1]), goal, self._knowledge)
                if path != None:
                    break
                # Not sure if we are allow to do this
                self.update_belief_state(self.get_scalar(self._belief_state[goal[0]][goal[1]], 
                                                         Status.Blocked))
                self._belief_state[goal[0], goal[1]] = 0
                self._knowledge.get_cell(goal[0], goal[1]).set_status(Status.Blocked)

            end_cell, count, status_string = self.execute(path)

            start = [end_cell.x, end_cell.y]
            total_path.extend(path[:count])
            if status_string == 'find goal' or status_string == 'examine failed':
                examine_count += 1

            if status_string == 'find goal':
                print(f'time to find the goal = {time_to_find_goal}')
                return examine_count, total_path, status_string
        
        return examine_count, total_path, 'cannot find goal in limited steps'
    
    def print_belief_state(self) -> None:
        bs = ''
        for row in self._belief_state:
            bs += ' '.join(['{:.4}\t'.format(belief)
                                for belief in row]) + "\n"
        print(bs)