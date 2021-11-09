from agent_6 import Agent6
from gridworld import GridWorld, Status
from astar_search import *

def main() -> None:
    density = 0.3
    start = [0, 0]
    while True:
        maze = GridWorld(50, True, 0.3)
        maze.print_grid()
        path = astar_search(maze.get_cell(0, 0), maze.get_target(), maze)
        if path != None:
            agent = Agent6(maze, density, [0.2, 0.5, 0.8])
            examine_count, path, status_string = agent.solve(start, 10000)
            if(status_string == 'find goal'):
                for cell in path:
                    maze.get_cell(cell.x, cell.y).set_status(Status.Path)

                print(f'examine count = {examine_count}')
                print(f'trajectory length = {len(path)}')
                maze.print_grid()
            else:
                print('agent did not solve the maze')
            break

if __name__ == '__main__':
    main()