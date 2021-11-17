
import matplotlib.pyplot as plt
import numpy as np
import csv

from gridworld import TerrainType

def length_by_type(terrain_list, len_6, len_7, len_9, dim):
    data = None
    font_style = {'family': 'serif', 'color': 'black', 'size': 12}
    def setup():
        data = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for j, terrain in enumerate(["Flat", "Hilly", "Forest"]):
            for z, value in enumerate([len_6, len_7, len_9]):
                data[z][j] = [value[i] for i in [i for i, x in enumerate(terrain_list) if x == terrain]]
        return data
        
    
    data = setup()
    for j, terrain in enumerate(["Flat", "Hilly", "Forest"]):
            
        title = f"What was the Trajectory Length when the target was\nin {terrain} Terrain?"
        plt.figure(num=title, tight_layout=True)
        plt.title(title, fontdict=font_style)
        plt.grid()
        plt.plot(data[0][j], label="Agent 6")
        plt.plot(data[1][j], label="Agent 7")
        plt.ylabel("Trajectory Length", fontdict=font_style)
        plt.legend()
        filename = f"images/trajectory_length_{terrain}_{dim}_6_7.png"
        plt.savefig(filename)
        plt.close()
        
    title = f"What was the Trajectory Length for Agent 9 when the target was\nin Flat, Hilly or Forest Terrain?"
    plt.figure(num=title, tight_layout=True)
    plt.title(title, fontdict=font_style)
    
    plt.ylabel("Trajectory Length", fontdict=font_style)
    
    for j, terrain in enumerate(["Flat", "Hilly", "Forest"]):
        plt.plot(data[2][j], label=terrain)
        
    filename = f"images/trajectory_length_Terrain_{dim}_9.png"
    
    plt.grid()
    plt.legend()
    plt.savefig(filename)
    plt.close()
    
    
def examine_by_type(terrain_list, len_6, len_7, len_9, dim):
    data = None
    font_style = {'family': 'serif', 'color': 'black', 'size': 12}
    def setup():
        data = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for j, terrain in enumerate(["Flat", "Hilly", "Forest"]):
            for z, value in enumerate([len_6, len_7, len_9]):
                data[z][j] = [value[i] for i in [i for i, x in enumerate(terrain_list) if x == terrain]]
        return data
        
    
    data = setup()
    for j, terrain in enumerate(["Flat", "Hilly", "Forest"]):
            
        title = f"Number of Times Examined when Target was\nin {terrain} Terrain"
        plt.figure(num=title, tight_layout=True)
        plt.title(title, fontdict=font_style)
        plt.grid()
        plt.plot(data[0][j], label="Agent 6")
        plt.plot(data[1][j], label="Agent 7")
        plt.ylabel("Number of Examine", fontdict=font_style)
        plt.legend()
        filename = f"images/examine_count_{terrain}_{dim}_6_7.png"
        plt.savefig(filename)
        plt.close()
        
    title = f"Number of Times Examined for Agent 9 when Target was\nin Flat, Hilly or Forest Terrain"
    plt.figure(num=title, tight_layout=True)
    plt.title(title, fontdict=font_style)
    
    plt.ylabel("Number of Examine", fontdict=font_style)
    
    for j, terrain in enumerate(["Flat", "Hilly", "Forest"]):
        plt.plot(data[2][j], label=terrain)
        
    filename = f"images/examine_count_Terrain_{dim}_9.png"
    
    plt.grid()
    plt.legend()
    plt.savefig(filename)
    plt.close()

def trajectory_length(len_6, len_7, len_9, dim):
    def setup():
        font_style = {'family': 'serif', 'color': 'black', 'size': 12}
        title = "Trajectory Length"
        plt.figure(num=title, tight_layout=True)
        plt.title(title, fontdict=font_style)

        plt.xlabel("Number of Runs", fontdict=font_style)
        plt.ylabel("Trajectory Length", fontdict=font_style)
        plt.grid()
    
    setup()
    plt.plot(len_6, label="Agent 6")
    filename = f"images/trajectory_length_{dim}_6.png"
    plt.savefig(filename)
    plt.close()
    
    setup()
    plt.plot(len_7, label="Agent 7")
    filename = f"images/trajectory_length_{dim}_7.png"
    plt.savefig(filename)    
    plt.close()
    
    setup()
    plt.plot(len_9, label="Agent 9")
    filename = f"images/trajectory_length_{dim}_9.png"    
    plt.savefig(filename)
    plt.close()
    
    setup()
    plt.plot(len_6, label="Agent 6")
    plt.plot(len_7, label="Agent 7")
    plt.plot(len_9, label="Agent 9")
    plt.legend()
    filename = f"images/trajectory_length_{dim}_6_7_9.png"    
    plt.savefig(filename)
    plt.close()
    
def examine_count(len_6, len_7, len_9, dim):
    def setup():
        font_style = {'family': 'serif', 'color': 'black', 'size': 12}
        title = "Number of Examine"
        plt.figure(num=title, tight_layout=True)
        plt.title(title, fontdict=font_style)

        plt.xlabel("Number of Runs", fontdict=font_style)
        plt.ylabel("Number of Examine", fontdict=font_style)
        plt.grid()
    
    setup()
    plt.plot(len_6, label="Agent 6")
    filename = f"images/examine_count_{dim}_6.png"
    plt.savefig(filename)
    plt.close()
    
    setup()
    plt.plot(len_7, label="Agent 7")
    filename = f"images/examine_count_{dim}_7.png"
    plt.savefig(filename)    
    plt.close()
    
    setup()
    plt.plot(len_9, label="Agent 9")
    filename = f"images/examine_count_{dim}_9.png"    
    plt.savefig(filename)
    plt.close()
    
    setup()
    plt.plot(len_6, label="Agent 6")
    plt.plot(len_7, label="Agent 7")
    plt.plot(len_9, label="Agent 9")
    plt.legend()
    filename = f"images/examine_count_{dim}_6_7_9.png"    
    plt.savefig(filename)
    plt.close()
    
    
def target_in(terrain_list, dim):
    def setup():
        font_style = {'family': 'serif', 'color': 'black', 'size': 12}
        title = "Target Distribution by Terrain Type"
        plt.figure(num=title, tight_layout=True)
        plt.title(title, fontdict=font_style)
        
        plt.ylabel("Number of Examine", fontdict=font_style)
        plt.grid()
    flat, hilly, forest = 0, 0, 0
    for i, val in enumerate(terrain_list):
        if val == "Flat":
            flat += 1
        elif val == "Hilly":
            hilly += 1
        elif val == "Forest":
            forest += 1
    
    setup()
    plt.bar(["Flat", "Hilly", "Forest"], [flat, hilly, forest])
    filename = f"images/target_in_{dim}.png"    
    plt.savefig(filename)
    plt.close()
    
    
    
def graph_main(dim, runs):
    with open(f"agent_{dim}_x_{dim}_for_{runs}_6_7_9.csv", "r") as f:
        reader = csv.reader(f, delimiter="\t")
        terrain_list = list(map(str, f.readline().split(',')))
        f.readline()
        trajectory_length_6 = list(map(int, f.readline().split(',')))
        f.readline()
        trajectory_length_7 = list(map(int, f.readline().split(',')))
        f.readline()
        trajectory_length_9 = list(map(int, f.readline().split(',')))
        f.readline()
        examine_count_6 = list(map(int, f.readline().split(',')))
        f.readline()
        examine_count_7 = list(map(int, f.readline().split(',')))
        f.readline()
        examine_count_9 = list(map(int, f.readline().split(',')))
        
    trajectory_length(trajectory_length_6, trajectory_length_7, trajectory_length_9, dim)
    examine_count(examine_count_6, examine_count_7, examine_count_9, dim)
    target_in(terrain_list, dim)
    length_by_type(terrain_list, trajectory_length_6, trajectory_length_7, trajectory_length_9, dim)
    examine_by_type(terrain_list, examine_count_6, examine_count_7, examine_count_9, dim)
    
if __name__ == '__main__':
    graph_main(100, 100)
    
    