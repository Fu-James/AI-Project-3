import numpy as np
from random import choice
import time
import copy
from agent_7 import Agent7
from astar_search import astar_search
from gridworld import GridWorld, Cell, Status, TerrainType
import math
from queue import Queue
from dataclasses import dataclass

@dataclass
class Node():
    pos: tuple
    distance: int

class Agent9(Agent7):
    def __init__(self, maze: GridWorld, density: float,
                 false_negative_rates: list, debug: bool=False) -> None:
        self._density = density
        self._fnr = false_negative_rates

        unknown_terrain_fnr = np.mean([(1 - fnr) for fnr in self._fnr])
        self._confidence = [(1 - fnr) / unknown_terrain_fnr for fnr in self._fnr]
        self.extra_h = 0
        self.extra_flat = 0
        self.extra_fore = 0
        self._maze = maze
        self._dim = maze.get_dim()
        self._knowledge = GridWorld(self._dim, False)
        self._belief_state = np.ones((self._dim, self._dim))
        #self._belief_state = np.array([[(1 / (self._dim ** 2)) for _ in range(self._dim)] for _ in range(self._dim)])
        self._debug = debug
        
    def update_belief_state(self, cell: Cell, belief: list[list], status: Status) -> None:
        if status == Status.Blocked:
            belief[cell.x, cell.y] = 0
        elif status == Status.Empty:
            pass
        elif status == Status.Examine:
            fnr = self._fnr[cell.get_terrain_type().value]
            belief[cell.x, cell.y] *= fnr
        else:
            raise ValueError('Status for calling get_scalar should be either blocked, empty, or examine')
        
    def breadth_first_search(self, start: tuple, belief: list[list], target_value: np.float64) -> list:
        if self._debug:
            print(f'Inside bfs with belief')
        visited = set(start)
        queue: Queue[Node] = Queue()
        queue.put(Node(start, 0))
        targets = []

        while not queue.empty():
            node = queue.get()
            
            if math.isclose(belief[node.pos], target_value):
                target_distance = node.distance
                targets.append(node.pos)
                while not queue.empty:
                    node = queue.get()
                    if node.distance > target_distance:
                        return targets
                    if math.isclose(belief[node.pos], target_value):
                        targets.append(node.pos)
                break
            neighbors = self.get_neighbors(node.pos)
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.put(Node(neighbor, node.distance + 1))
        return targets

    
    def get_target(self, start: list, belief: list[list]) -> list:
        target_value = np.amax(belief)
        targets = self.breadth_first_search(tuple(start), belief, target_value)
        if len(targets) < 1:
            raise Exception('Logical error in breadth_first_search()')
        return list(choice(targets))
    
    def partial_sensing(self, current: Cell) -> None:
        neighbors = self._maze.get_all_neighbors(current)
        for neighbor in neighbors:
            if neighbor.is_target():
                return True
        return False
    
    def move_target(self):
        x, y = self._maze.get_target()
        target = self._maze.get_cell(x, y)        
        target.set_status(Status.Empty)
        new_target = choice([i for i in self._maze.get_all_neighbors(target) if not i.is_blocked()])
        self._maze.set_target([new_target.x, new_target.y])
        new_target.set_status(Status.Target)
        if self._debug:
            print(f'Target moved from ({x}, {y}) to ({new_target.x}, {new_target.y})')    

    def execute(self, path: list[Cell]) -> list:
        for count, cell_in_knowledge in enumerate(path):
            cell_in_maze = self._maze.get_cell(cell_in_knowledge.x, cell_in_knowledge.y)
            test = self._knowledge.get_cell(cell_in_knowledge.x, cell_in_knowledge.y)
            
            if not cell_in_knowledge.isVisited:
                cell_in_knowledge.isVisited = True
                if cell_in_maze.is_blocked():
                    if self._debug:
                        print(f'Blocked encountered at ({cell_in_knowledge.x}, {cell_in_knowledge.y})')
                        print(f'Test cell: ({test.x}, {test.y}) isVisisted: {test.isVisited} parent: {test.get_parent()}')
                    cell_in_knowledge.set_status(Status.Blocked)
                    self.update_belief_state(cell_in_knowledge, self._belief_state, Status.Blocked)
                    if cell_in_knowledge.get_parent() is None:
                        return path[-1], count - 1, 'blocked'
                    return cell_in_knowledge.get_parent(), count - 1, 'blocked'
                else:
                    cell_in_knowledge.set_status(Status.Empty)
                    cell_in_knowledge.set_terrain_type(cell_in_maze.get_terrain_type())
                    
                    if self.update_confidence(cell_in_knowledge):
                        if self.belief_is_greater(cell_in_knowledge, path[-1]):
                            break
                    else:
                        if cell_in_knowledge is path[-1]:
                            if self._belief_state[cell_in_knowledge.x][cell_in_knowledge.y] < np.amax(self._belief_state):
                                return cell_in_knowledge, count, 'Target change'                   
                    
        if self.partial_sensing(cell_in_maze):
            neighbors = self._knowledge.get_all_neighbors(cell_in_knowledge)
            
            copy_belief_state = copy.deepcopy(self._belief_state)     
            
            self.update_belief_state(cell_in_knowledge, copy_belief_state, Status.Blocked)
            
            for i, val in enumerate(copy_belief_state):
                for j, v in enumerate(val):
                    if i > cell_in_knowledge.x - 2 and i < cell_in_knowledge.x + 2 and j > cell_in_knowledge.y - 2 and j < cell_in_knowledge.y + 2:
                        pass
                    else:
                        temp_cell = self._knowledge.get_cell(i, j)
                        self.update_belief_state(temp_cell, copy_belief_state, Status.Blocked)                                              
                        
            potential_target = self.get_target([cell_in_knowledge.x, cell_in_knowledge.y], copy_belief_state)
            
            if self._debug:
                print(f'New Potential Target at({potential_target[0]}, {potential_target[1]})')
                
            potential_target = self._knowledge.get_cell(potential_target[0], potential_target[1])
            
            if not potential_target.isVisited:
                potential_target.set_parent(cell_in_knowledge)
            return potential_target, count, 'move in potential target direction'
        else:           
            no_of_checks = 1
            if cell_in_knowledge.get_terrain_type() == TerrainType.Flat:
                no_of_checks = 2
            elif cell_in_knowledge.get_terrain_type() == TerrainType.Hilly:
                no_of_checks = 3
            elif cell_in_knowledge.get_terrain_type() == TerrainType.Forest:
                no_of_checks = 4
            
            
            for i in range(no_of_checks):                
                if self.examine(cell_in_maze):
                    return cell_in_knowledge, count, 'find goal'
                else:
                    if cell_in_knowledge.get_terrain_type() == TerrainType.Flat:
                        self.extra_flat += 1
                    elif cell_in_knowledge.get_terrain_type() == TerrainType.Hilly:
                        self.extra_h += 1
                    elif cell_in_knowledge.get_terrain_type() == TerrainType.Forest:
                        self.extra_fore += 1
                    self.examine_count += 1
            self.update_belief_state(cell_in_knowledge, self._belief_state, Status.Examine)
            return cell_in_knowledge, count, 'examine failed'
        
    def solve(self, start: list, steps: int) -> list:
        self.examine_count = 0
        total_path = []
        time_to_find_goal = 0
        time_to_run_astar = 0
        astar_run_count = 0
        for _ in range(steps):
            while True:
                start_time = time.time_ns()
                goal = self.get_target(start, self._belief_state)
                if self._debug:
                    print(f'Starting at ({start[0]}, {start[1]})\tGoal cell might be at ({goal[0]}, {goal[1]})')
                end_time = time.time_ns()
                time_to_find_goal += end_time - start_time

                start_time = time.time_ns()
                path = astar_search(start, goal, self._knowledge, True)
                end_time = time.time_ns()
                time_to_run_astar += end_time - start_time
                astar_run_count += 1

                
                if path != None:
                    if self._debug:
                        print(f'Path exists, Path: {[(i.x, i.y) for i in path]}')
                        self.print_belief_state()
                    break

                # If the cell is unreachable, we can assume the cell is blocked
                cell_in_knowledge = self._knowledge.get_cell(goal[0], goal[1])
                cell_in_knowledge.set_status(Status.Blocked)
                self.update_belief_state(cell_in_knowledge, self._belief_state, Status.Blocked)
                self.move_target()

            end_cell, count, status_string = self.execute(path)
            start = [end_cell.x, end_cell.y]
            total_path.extend(path[1:count + 1])
            if status_string == 'find goal' or status_string == 'examine failed':
                self.examine_count += 1

            if status_string == 'find goal':
                print(f'A* search run {astar_run_count} times')
                print(f'Extra examine count Hilly {self.extra_h} times')
                print(f'Extra examine count Flat {self.extra_flat} times')
                print(f'Extra examine count Forrest {self.extra_fore} times')
                print(f'time to run A* search: {time_to_run_astar}')
                print(f'time to guess goals: {time_to_find_goal}')
                return self.examine_count, total_path, status_string
            if self._debug:
                print("Belief State:")
                self.print_belief_state()            
            self.move_target()
        
        return self.examine_count, total_path, 'cannot find goal in limited steps'        
