

from test import main
from graph import graph_main

if __name__ == '__main__':
    runs, density, dim = 500, 0.3, 101
    main(runs, density, dim)
    graph_main(dim, runs)
    
    runs, density, dim = 500, 0.3, 100
    main(runs, density, dim)
    graph_main(dim, runs)