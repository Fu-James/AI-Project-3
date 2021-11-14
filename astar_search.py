from queue import PriorityQueue
from dataclasses import dataclass, field
from copy import copy
from collections import deque

from gridworld import Cell, GridWorld

@dataclass(order=True)
class PrioritizedItem():
    priority: int
    item: Cell = field(compare=False)

def backtrack(current: Cell) -> list[Cell]:
    path = deque()
    while current is not None:
        path.appendleft(current)
        current = current.get_parent()
    return list(path)

def astar_search(start: list, goal: list, grid: GridWorld) -> list[Cell]:
    start_cell = grid.get_cell(start[0], start[1])
    start_cell.set_parent(None)

    fringe: PriorityQueue[PrioritizedItem] = PriorityQueue()
    fringe.put(PrioritizedItem(0, start_cell))

    visited = set()
    visited.add(start_cell.get_index())

    while not fringe.empty():
        current = fringe.get().item
        
        if [current.x, current.y] == goal:
            return backtrack(current)

        current_g = current.get_g()
        neighbors = grid.get_neighbors(current)

        for neighbor in neighbors:
            neighbor_index = neighbor.get_index()
            if (not neighbor.is_blocked() and 
                neighbor_index not in visited):
                visited.add(neighbor_index)

                neighbor.update_f_g_h(current_g + 1, goal)
                neighbor.set_parent(current)
                fringe.put(PrioritizedItem(neighbor.get_f(), neighbor))

    return None