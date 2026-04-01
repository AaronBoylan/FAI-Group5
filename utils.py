#!/usr/bin/env python

from peg_solitaire import *
from peg_duotaire import *
from peg_board import *
from search4e import *
from games4e import *

# Centralized search algorithms configuration
SEARCH_ALGORITHMS = {
    1: {
        'name': "Depth-First Search",
        'short_name': "DFS",
        'method': depth_first_bfs
    },
    2: {
        'name': "A* Search",
        'short_name': "A* Search",
        'method': astar_search
    },
    3: {
        'name': "Greedy Best-First Search",
        'short_name': "Greedy BFS",
        'method': greedy_bfs
    },
    4: {
        'name': "Bidirectional A* Search",
        'short_name': "Bidirectional A* Search",
        'method': peg_bidirectional_astar_search
    },
    5: {
        'name': "MCTS Monte Carlo Tree Search",
        'short_name': "MCTS Search",
        'method': mcts_search
    }
    
}

# Backward compatibility - maintain existing dictionaries
search_methods = {k: v['method'] for k, v in SEARCH_ALGORITHMS.items()}
search_names = {k: v['short_name'] for k, v in SEARCH_ALGORITHMS.items()}

TESTING_MENUS = {
    1: {
        'name': "Compare Performance of Search Algorithms",
        'short_name': "test_performance",
        'method': test_performance
    },
    2: {
        'name': "Compare Performance of Different Data Structures",
        'short_name': "test_data_structures",
        'method': test_data_structures
    },
    3: {
        'name': "Compare Performance of Different Direction Orders",
        'short_name': "test_directions",
        'method': test_directions
    }
}