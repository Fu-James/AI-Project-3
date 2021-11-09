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

def astar_search(start: Cell, goal: list, grid: GridWorld) -> list[Cell]:
    fringe = PriorityQueue()
    fringe.put(PrioritizedItem(0, copy(start)))

    visited = set()

    while not fringe.empty():
        current = fringe.get().item
        if (current.x, current.y) in visited:
            continue
        visited.add((current.x, current.y))

        if [current.x, current.y] == goal:
            return backtrack(current)

        current_g = current.get_g()
        neighbors = grid.get_neighbors(current)

        for neighbor in neighbors:
            if (not neighbor.is_blocked() and 
                (neighbor.x, neighbor.y) not in visited):

                neighbor_copy = copy(neighbor)
                neighbor_copy.update_f_g_h(current_g, goal)
                neighbor_copy.set_parent(current)
                fringe.put(PrioritizedItem(neighbor_copy.get_f(), 
                                           neighbor_copy))

    return None