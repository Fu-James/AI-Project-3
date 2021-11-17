from typing import Type
import time
import numpy as np
import csv

from agent_6 import Agent6
from agent_7 import Agent7
from agent_9 import Agent9
from gridworld import GridWorld, Status
from astar_search import *

def solve_maze(agent: Type[Agent6], dim: int) -> list:
    start = [0, 0]

    start_time = time.time_ns()
    examine_count, path, status_string = agent.solve(start, 1000000)
    end_time = time.time_ns()
    solve_time = end_time - start_time

    if(status_string == 'find goal'):
        print(f'\t\tSolve time = {solve_time}')
        print(f'\t\tExamine count: {examine_count}')
        print(f'\t\tTrajectory length: {len(path)}')
        print(f'\t\tTotal action: {examine_count + len(path)}')
    else:
        print('\t\tAgent did not solve the maze')
    
    return examine_count, len(path), solve_time

def main(runs, density, dim) -> None:
    false_negative_rate = [0.2, 0.5, 0.8]
    
    total_time_agent_list_6 = [] 
    total_time_agent_list_7 = []
    total_time_agent_list_9 = []

    examine_count_list_6 = []
    examine_count_list_7 = []
    examine_count_list_9 = []
    trajectory_length_list_6 = []
    trajectory_length_list_7 = []
    trajectory_length_list_9 = []
    terrain_type = []
    
    for i in range(runs):
        print(f'Run: {i + 1}')
        while True:
            maze = GridWorld(dim, True, 0.3)
            goal = maze.get_target()
            path = astar_search([0, 0], goal, maze)            
            
            if path != None:
                maze.print_grid()
                
                terrain_type_of_goal = maze.get_cell(goal[0], goal[1]).get_terrain_type().name 
                print(f'Terrain type of the target is: {terrain_type_of_goal}')
                terrain_type.append(terrain_type_of_goal)

                print('\tAgent 6:')
                agent_6 = Agent6(copy(maze), density, false_negative_rate)
                examine_count_6, trajectory_length_6, solve_time_6 = solve_maze(agent_6, dim)
                total_time_agent_list_6.append(solve_time_6)
                examine_count_list_6.append(examine_count_6)
                trajectory_length_list_6.append(trajectory_length_6)

                print('\tAgent 7:')
                agent_7 = Agent7(copy(maze), density, false_negative_rate)
                examine_count_7, trajectory_length_7, solve_time_7 = solve_maze(agent_7, dim)
                total_time_agent_list_7.append(solve_time_7)
                examine_count_list_7.append(examine_count_7)
                trajectory_length_list_7.append(trajectory_length_7)
                
                print('\t(Target can move) Agent 9:')
                agent_9 = Agent9(copy(maze), density, false_negative_rate)
                examine_count_9, trajectory_length_9, solve_time_9 = solve_maze(agent_9, dim)
                total_time_agent_list_9.append(solve_time_9)
                examine_count_list_9.append(examine_count_9)
                trajectory_length_list_9.append(trajectory_length_9)
                
                break
    
    print("\n")
    print(f'Average solving time for agent6: {np.mean(total_time_agent_list_6)}')
    print(f'Average solving time for agent7: {np.mean(total_time_agent_list_7)}')
    print(f'Average solving time for agent9: {np.mean(total_time_agent_list_9)}')

    with open(f'agent_{dim}_x_{dim}_for_{runs}_6_7_9.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(terrain_type)
        writer.writerow(examine_count_list_6)
        writer.writerow(examine_count_list_7)
        writer.writerow(examine_count_list_9)
        writer.writerow(trajectory_length_list_6)
        writer.writerow(trajectory_length_list_7)
        writer.writerow(trajectory_length_list_9)

if __name__ == '__main__':
    main(100, 0.3, 100)
    main(100, 0.3, 80)
    main(100, 0.3, 50)
