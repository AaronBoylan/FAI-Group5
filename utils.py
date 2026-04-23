#!/usr/bin/env python

from peg_solitaire import peg_bidirectional_astar_search, test_performance, test_data_structures, test_directions
from games4e import random_player, h_alphabeta_search, monte_carlo_tree_search, user_player, player
from search4e import depth_first_bfs, greedy_bfs, astar_search, mcts_search


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
        'name': "Greedy Best-First Search",
        'short_name': "Greedy BFS",
        'method': greedy_bfs
    },
    3: {
        'name': "A* Search",
        'short_name': "A*",
        'method': astar_search
    },
    4: {
        'name': "Bidirectional A* Search",
        'short_name': "Bidirectional A*",
        'method': peg_bidirectional_astar_search
    },
    5: {
         'name': "MCTS Monte Carlo Tree Search",
         'short_name': "MCTS",
         'method': mcts_search
     }
}



GAME_PLAYERS = {
    1: {
        'name': "Random Player",
        'short_name': "Random",
        'method': random_player
    },
    2: {
        'name': "AlphaBeta Player",
        'short_name': "AlphaBeta",
        'method': player(h_alphabeta_search)
    },
    3: {
        'name': "MCTS Player",
        'short_name': "MCTS",
        'method': player(monte_carlo_tree_search)
    },
    4: {
        'name': "User Player",
        'short_name': "User",
        'method': user_player
    }
}




TESTING_MENUS = {
    1: {
        'name': "Compare Performance of Search Algorithms",
        'short_name': "Peg Solitaire Search Performance",
        'method': test_performance
    },
    2: {
        'name': "Compare Performance of Game Algorithms",
        'short_name': "Peg Duotaire Game Performance",
        'method': test_performance
    },
    3: {
        'name': "Compare Performance of Dict and Bitmask Data Structures",
        'short_name': "Peg Board Bitmask Performance",
        'method': test_data_structures
    },
    4: {
        'name': "Compare Performance of Different Direction Orders",
        'short_name': "DFS Search Direction Comparison",
        'method': test_directions
    }
}