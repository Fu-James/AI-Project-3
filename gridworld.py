from __future__ import annotations
import random
from enum import Enum

class Status(Enum):
    Empty = 0
    Blocked = 1
    Unconfirmed = 2
    Target = 3
    Examine = 4
    Path = 5

class TerrainType(Enum):
    Flat = 0
    Hilly = 1
    Forest = 2
    Unknown = 3
    Blocked = 4

class Cell():
    def __init__(self, parent, x: int, y: int, dim: int,
                 status: Status = Status.Unconfirmed) -> None:
        self.x = x
        self.y = y
        self._g = 0
        self._h = 0
        self._f = 0
        self._parent = parent
        self._status = status
        self._terrain_type = None
        self.isVisited = False
        self._index: int = x * dim + y

    def set_g(self, g: float) -> None:
        self._g = g
    
    def get_g(self) -> float:
        return self._g
    
    def set_h(self, goal: list) -> float:
        self._h = abs(self.x - goal[0]) + abs(self.y - goal[1])

    def update_f_g_h(self, g: int, goal: list) -> None:
        self.set_g(g)
        self.set_h(goal)
        self._f = self._g + self._h
    
    def get_f(self) -> float:
        return self._f

    def set_parent(self, parent: Cell) -> None:
        self._parent = parent
    
    def get_parent(self) -> Cell:
        return self._parent

    def set_status(self, s: int):
        self._status = Status(s)

    def get_status(self) -> Status:
        return self._status

    def set_terrain_type(self, terrain_type: TerrainType) -> None:
        self._terrain_type = TerrainType(terrain_type)
    
    def set_random_terrain_type(self) -> None:
        self._terrain_type = TerrainType(random.randrange(3))

    def get_terrain_type(self) -> TerrainType:
        return self._terrain_type

    def get_index(self) -> int:
        return self._index

    def is_blocked(self) -> bool:
        return self._status is Status.Blocked

    def is_empty(self) -> bool:
        return self._status is Status.Empty
    
    def is_unconfirmed(self) -> bool:
        return self._status is Status.Unconfirmed

    def is_target(self) -> bool:
        return self._status is Status.Target

    # def is_flat(self) -> bool:
    #     return self._terrain_type is TerrainType.Flat

    # def is_hilly(self) -> bool:
    #     return self._terrain_type is TerrainType.Hilly

    # def is_forest(self) -> bool:
    #     return self._terrain_type is TerrainType.Forest

class GridWorld():
    def __init__(self, dim: int, is_maze: bool, density: float = None) -> None:
        if is_maze == True and density == None:
            raise ValueError('Density should be inputed for maze')
        
        self._dim = dim
        self._is_maze = is_maze
        self._target = None

        if self._is_maze:
            self.create_maze(density)
        else:
            self.create_knowledge()

    def create_maze(self, density):
        maze = [[Cell(None, x, y, self._dim, Status.Empty) 
                 for y in range(self._dim)] for x in range(self._dim)]
        for row in range(self._dim):
            for col in range(self._dim):
                if random.uniform(0, 1) < density:
                    maze[row][col].set_status(Status.Blocked)
                    maze[row][col].set_terrain_type(TerrainType.Blocked)
                else:
                    maze[row][col].set_random_terrain_type()

        maze[0][0].set_status(Status.Empty)
        maze[0][0].set_random_terrain_type()

        while True:
            pos = random.randrange(self._dim * self._dim)
            x, y = pos // self._dim, pos % self._dim
            if maze[x][y].is_empty():
                self._target = [x, y]
                maze[x][y].set_status(Status.Target)
                break
        self.gridworld = maze

    def create_knowledge(self):
        knowledge = [[Cell(None, x, y, self._dim) for y in range(self._dim)]
                     for x in range(self._dim)]
        for row in knowledge:
            for cell in row:
                cell.set_terrain_type(TerrainType.Unknown)
        self.gridworld = knowledge
    
    def get_dim(self) -> int:
        return self._dim

    def get_target(self) -> list:
        return self._target
    
    def set_target(self, target: list):
        self._target = target    
    
    def get_cell(self, x: int, y: int) -> Cell:
        if not 0 <= x < self._dim:
            raise ValueError('Index x should be in the interval [0, dim)')
        if not 0 <= y < self._dim:
            raise ValueError('Index y should be in the interval [0, dim)')
        return self.gridworld[x][y]

    def get_neighbors(self, current: Cell) -> list[Cell]:
        neighbors = []
        # N
        if current.x - 1 >= 0:
            neighbors.append(self.gridworld[current.x-1][current.y])
        # E
        if current.y + 1 < self._dim:
            neighbors.append(self.gridworld[current.x][current.y+1])
        # S
        if current.x + 1 < self._dim:
            neighbors.append(self.gridworld[current.x+1][current.y])
        # W
        if current.y - 1 >= 0:
            neighbors.append(self.gridworld[current.x][current.y-1])   
        return neighbors
    
    def get_all_neighbors(self, current: Cell) -> list[Cell]:
        # N, S, E, W
        neighbors = self.get_neighbors(current)
        # NW
        if current.x - 1 >= 0 and current.y-1 >= 0:
            neighbors.append(self.gridworld[current.x-1][current.y-1])
        # NE
        if current.x - 1 >= 0 and current.y+1 < self._dim:
            neighbors.append(self.gridworld[current.x-1][current.y+1])
        # SW
        if current.x + 1 < self._dim and current.y-1 >= 0:
            neighbors.append(self.gridworld[current.x+1][current.y-1])
        # SE
        if current.x+1 < self._dim and current.y+1 < self._dim:
            neighbors.append(self.gridworld[current.x+1][current.y+1])
        return neighbors        

    def print_grid(self) -> str:
        maze = ''
        for row in self.gridworld:
            maze += ' '.join([str(cell.get_status().value)
                                for cell in row]) + "\n"
        print(maze)

    def get_grid_ascii(self) -> list[list[int]]:
        return [[cell.get_status().value for cell in row] for row in self.gridworld]
