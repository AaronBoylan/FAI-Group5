#!/usr/bin/env python

from peg_solitaire import *
from peg_duotaire import *
from peg_board import *
from search4e import *
from games4e import *

search_methods = {
    1: depth_first_bfs,
    2: astar_search,
    3: greedy_bfs,
    4: peg_bidirectional_astar_search
}

search_names = {
    1: "DFS",
    2: "A* Search",
    3: "Greedy BFS",
    4: "Bidirectional A* Search"
}