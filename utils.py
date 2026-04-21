#!/usr/bin/env python

from peg_solitaire import *
from peg_duotaire import *
from peg_board import *
# from visualize_search import *
from search4e import *
from games4e import *

PEG_BOARDS = {
    1: {
        'name': "Triangle Peg Board (15 Holes)",
        'short_name': "Triangle",
        'method': "Triangle"
    },
    2: {
        'name': "English Peg Board (33 Holes)",
        'short_name': "English",
        'method': "English"
    },
    3: {
        'name': "French Peg Board (37 Holes)",
        'short_name': "French",
        'method': "French"
    }
}

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

GAME_PLAYERS = {
    1: {
        'name': "Random Player",
        'short_name': "random_player",
        'method': random_player
    },
    2: {
        'name': "AlphaBeta Player",
        'short_name': "h_alphabeta_search",
        'method': player(h_alphabeta_search)
    },
    3: {
        'name': "MCTS Player",
        'short_name': "mcts",
        'method': player(monte_carlo_tree_search)
    },
    4: {
        'name': "A* Player",
        'short_name': "astar_duotaire",
        'method': player(duotaire_astar_search)
    },
    5: {
        'name': "Greedy BFS Player",
        'short_name': "greedy_bfs_duotaire",
        'method': player(duotaire_greedy_bfs_search)
    }
    ,
    6: {
        'name': "Minimax Player (Full Depth) (***Warning very slow on English and French boards***)",
        'short_name': "minimax_decision",
        'method': player(duotaire_minimax_search)
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
        'name': "Compare Performance of Dict and Bitmask Data Structures",
        'short_name': "test_data_structures",
        'method': test_data_structures
    },
    3: {
        'name': "Compare Performance of Different Direction Orders",
        'short_name': "test_directions",
        'method': test_directions
    }
}