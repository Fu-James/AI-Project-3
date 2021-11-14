import numpy as np

from agent_6 import Agent6
from gridworld import GridWorld, Cell, Status

class Agent7(Agent6):
    def __init__(self, maze: GridWorld, density: float,
                 false_negative_rates: list) -> None:
        self._density = density
        self._fnr = false_negative_rates

        unknown_terrain_fnr = np.mean([(1 - fnr) for fnr in self._fnr])
        self._confidence = [(1 - fnr) / unknown_terrain_fnr for fnr in self._fnr]

        self._maze = maze
        self._dim = maze.get_dim()
        self._knowledge = GridWorld(self._dim, False)
        self._belief_state = np.ones((self._dim, self._dim))

    def update_confidence(self, cell: Cell) -> bool:
        """
        Return true if confidence of the cell increase, otherwise false
        """
        confidence = self._confidence[cell.get_terrain_type().value]
        self._belief_state[cell.x, cell.y] *= confidence
        return True if confidence >= 0 else False

    def belief_is_greater(self, a: Cell, b: Cell) -> bool:
        if self._belief_state[a.x][a.y] >= self._belief_state[b.x][b.y]:
            return True
        return False

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
                    
                    if self.update_confidence(cell_in_knowledge):
                        if self.belief_is_greater(cell_in_knowledge, path[-1]):
                            break
                    else:
                        if cell_in_knowledge is path[-1]:
                            if self._belief_state[cell_in_knowledge.x][cell_in_knowledge.y] < np.amax(self._belief_state):
                                return cell_in_knowledge, count, 'Target change'                   
                    

        if self.examine(cell_in_maze):
            return cell_in_knowledge, count, 'find goal'
        else:
            self.update_belief_state(cell_in_knowledge, Status.Examine)
            return cell_in_knowledge, count, 'examine failed'
