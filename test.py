from agent_6 import Agent6
from agent_7 import Agent7
from gridworld import GridWorld, Status
from astar_search import *
import time

def main() -> None:
    density = 0.3
    start = [0, 0]
    total_time = 0
    for i in range(30):
        print(f'Run: {i}')
        while True:
            maze = GridWorld(101, True, 0.3)
            path = astar_search([0, 0], maze.get_target(), maze)
            if path != None:
                # print('maze')
                # maze.print_grid()
                agent = Agent6(maze, density, [0.2, 0.5, 0.8])
                start_time = time.time_ns()
                examine_count, path, status_string = agent.solve(start, 1000000)
                end_time = time.time_ns()
                if(status_string == 'find goal'):
                    for cell in path:
                        maze.get_cell(cell.x, cell.y).set_status(Status.Path)

                    # print('solution')
                    # maze.print_grid()
                    print(f'Solve time = {end_time - start_time}')
                    print(f'examine count: {examine_count}')
                    print(f'trajectory length: {len(path)}')
                else:
                    print('agent did not solve the maze')
                break
        total_time += end_time - start_time
    print(f'Average solving time = {total_time/30}')

if __name__ == '__main__':
    main()
