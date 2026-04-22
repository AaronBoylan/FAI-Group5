#!/usr/bin/env python3
import copy
import math

from games4e import Game, minmax_decision, play_game
from peg_board import *
from peg_solitaire import PegSolitaire
from search4e import astar_search, failure, greedy_bfs

class PegDuotaire(Game):
    """PegDuotaire, a subclass of Game, represents one player in a Peg Duotaire game."""
    def __init__(self, shape='English'):
        assert shape in ('English', 'Triangle', 'French')
        self.shape = shape
        if shape == 'English':
            # board = EnglishPegBoardDict(to_move='X')
            board = EnglishPegBoardInt(to_move='X')
        elif shape == 'French':
            board = FrenchPegBoardInt(to_move='X')
        elif shape == 'Triangle':
            # board = TrianglePegBoardDict(to_move='X')
            board = TrianglePegBoardInt(to_move='X')

        self.initial = board
        if isinstance(board, PegBoardDict):
            self.goal = board.init_hole
        else:
            self.goal = copy.copy(self.initial)
            self.goal.state = 1 << board.GOAL_INDEX
            self.goal.pagoda = self.goal.compute_pagoda(self.goal.state)
            self.goal.__dict__.pop("_canon", None)
            self.goal.__dict__.pop("_hash", None)

    def actions(self, board):
        """Return a collection of the allowable moves from this state."""
        return board.actions()

    def result(self, board, action):
        """Return the state that results from making a move from a state."""
        new_board = board.result(action)
        new_board.to_move = 'O' if board.to_move == 'X' else 'X'
        return new_board

    def is_terminal(self, board):
        """Return True if this is a final state for the game."""
        return len(board.actions()) == 0

    def terminal_test(self, board):
        return self.is_terminal(board)

    def to_move(self, board):
        return board.to_move

    def utility(self, board, player):
        """Return the value of this final state to player."""
        if board.to_move == player:
            return -1
        else:
            return 1


def _board_for_solitaire_search(board):
    """Detach Duotaire turn metadata; refresh pagoda for PegSolitaire search.
    Safely detach the board from the Duotaire game. for analysis without modifying the original board.
    """
    b = copy.copy(board) #copy the board
    b.__dict__.pop("_canon", None) #remove the canonical representation of the board
    b.__dict__.pop("_hash", None) #remove the hash of the board (to avoid hash collisions)
    b.pagoda = b.compute_pagoda(b.state) #compute the pagoda of the board
    return b


def _solitaire_path_cost(game, board_after_move, searcher): 
    """Cost of a solitaire solution from this layout, or inf if none found."""
    problem = PegSolitaire(shape=game.shape) #create a new PegSolitaire problem
    problem.initial = _board_for_solitaire_search(board_after_move)
    node = searcher(problem)
    if node is failure: #if no solution is found, return infinity
        return math.inf
    return node.path_cost


def _duotaire_search_pick_move(game, state, searcher):
    """Choose a jump that minimizes solitaire solution length, then opponent mobility."""
    actions = list(game.actions(state))
    if not actions:
        raise ValueError("No legal moves from this state.")
    best_move = None
    best_key = None
    for a in actions: #check all moves and pick the best one
        nxt = game.result(state, a)
        cost = _solitaire_path_cost(game, nxt, searcher)
        opp_moves = len(game.actions(nxt))
        key = (cost, opp_moves)
        if best_key is None or key < best_key: #if the key is better than the best key, update the best key and the best move
            best_key, best_move = key, a
    return best_move


def duotaire_astar_search(game, state):
    """ move from A* on PegSolitaire per successor."""
    return (0, _duotaire_search_pick_move(game, state, astar_search))


def duotaire_greedy_bfs_search(game, state):
    """Greedy-BFS Duotaire policy (for player() in games4e).

    Each candidate jump is scored by running greedy_bfs on a
    PegSolitaire problem from the board after that jump; the jump with the
    shortest solitaire solution wins, with fewer opponent moves as tie-break.

    Returns (0, move): player() only uses the move at index 1,
    """
    
    return (0, _duotaire_search_pick_move(game, state, greedy_bfs))


def duotaire_minimax_search(game, state):
    """Full-depth minimax Duotaire policy (for player() in games4e).

    games4e.minmax_decision returns a move (not (score, move)).
    Returns (0, move): player() only uses the move at index 1.
    """
    return (0, minmax_decision(state, game))


def test_duotaire(searchers, shapes, times, verbose=False):
    import itertools

    results = {}

    for shape in shapes:
        for p1_name, p2_name in itertools.combinations(searchers, 2):
            from utils import GAME_PLAYERS
            p1 = [v['method'] for k, v in GAME_PLAYERS.items() if v['short_name'] == p1_name][0]
            p2 = [v['method'] for k, v in GAME_PLAYERS.items() if v['short_name'] == p2_name][0]

            print(f'Running Peg Duotaire match {times} times on {shape} board: {p1_name} v.s. {p2_name}')
            results[(shape, p1_name, p2_name)] = [0, 0]

            peg_duo = PegDuotaire(shape=shape)

            for _ in range(int(times/2)):
                final_board = play_game(peg_duo, dict(X=p1, O=p2), verbose=False)
                idx = 0 if peg_duo.utility(final_board, 'X') == 1 else 1
                results[(shape, p1_name, p2_name)][idx] += 1

                final_board = play_game(peg_duo, dict(X=p2, O=p1), verbose=False)
                idx = 0 if peg_duo.utility(final_board, 'O') == 1 else 1
                results[(shape, p1_name, p2_name)][idx] += 1

            print('Result:', results[(shape, p1_name, p2_name)])

    print(results)
    # if verbose:

    return results
