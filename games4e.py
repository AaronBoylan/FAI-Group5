#!/usr/bin/env python
# coding: utf-8

# # Game Tree Search
# 
# We start with defining the abstract class `Game`, for turn-taking *n*-player games. We rely on, but do not define yet, the concept of a `state` of the game; we'll see later how individual games define states. For now, all we require is that a state has a `state.to_move` attribute, which gives the name of the player whose turn it is. ("Name" will be something like `'X'` or `'O'` for tic-tac-toe.) 
# 
# We also define `play_game`, which takes a game and a dictionary of  `{player_name: strategy_function}` pairs, and plays out the game, on each turn checking `state.to_move` to see whose turn it is, and then getting the strategy function for that player and applying it to the game and the state to get a move.

from collections import namedtuple, Counter, defaultdict
import random
import math
import functools
import numpy as np
from peg_board import *
cache = functools.lru_cache(10**6)

class Game:
    """A game is similar to a problem, but it has a terminal test instead of 
    a goal test, and a utility for each terminal state. To create a game, 
    subclass this class and implement `actions`, `result`, `is_terminal`, 
    and `utility`. You will also need to set the .initial attribute to the 
    initial state; this can be done in the constructor."""

    def actions(self, state):
        """Return a collection of the allowable moves from this state."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def is_terminal(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError


def play_game(
    game,
    strategies: dict,
    verbose=False,
    user_player=False,
    screen=None,
    draw_board=None,
    state_history=None,
):
    """Play a turn-taking game. `strategies` is a {player_name: function} dict,
    where function(state, game) is used to get the player's move.
    --If `state_history` is a list, append the initial state, then the state after
    each ply, for replay or visualization."""
    state = game.initial

    if state_history is not None:
        state_history.append(state)

    while not game.is_terminal(state):
        player = state.to_move
        move = strategies[player](game, state)
        state = game.result(state, move)

        if state_history is not None:
            state_history.append(state)

        # GUI UPDATE (independent of whether a replay list is being recorded)
        if screen and draw_board:
            # Avoid double-flipping if `draw_board` already calls pygame.display.flip().
            try:
                draw_board(screen, state.state, flip_display=False)
            except TypeError:
                draw_board(screen, state.state)

            import pygame
            pygame.display.flip()

        if verbose: 
            if user_player:
                "Player X is the user, while Player 0 is the computer."
                action = move[0].bit_length() - 1, move[1].bit_length() - 1, move[2].bit_length() - 1

                if player != 'X':
                    action = move[0].bit_length() - 1, move[1].bit_length() - 1, move[2].bit_length() - 1
                    print('\nPlayer', player, 'move(From, Over, To):', action)
                    print(state)
                else:
                    print('\nYour move(From, Over, To):', action)
                    print(state)
            else:    
                action = move[0].bit_length() - 1, move[1].bit_length() - 1, move[2].bit_length() - 1
                print('\nPlayer', player, 'move (From, Over, To):', action)
                print(state)
    return state


infinity = math.inf


def random_player(game, state): return random.choice(list(game.actions(state)))

def user_player(game, state):
    "Player with choices determined by user input."
    move = None
    while move not in game.actions(state):
        print("\nCurrent board:")
        print(state)
        actions = list(game.actions(state))

        if not actions:
            raise ValueError("No legal moves from this state.")
        for i, (f, o, t, _) in enumerate(actions, start=1):
            action = f.bit_length() - 1, o.bit_length() - 1, t.bit_length() - 1
            print(f'{i}. Action(from, over, to): {action}')
        user_input = input("Your move? ").strip()
        #check if the input is a valid
        try:
            choice = int(user_input)
        except ValueError:
            print("Invalid input: enter the number of one of the listed moves.")
            continue
        if choice < 1 or choice > len(actions):
            print(f"Invalid choice: enter a number from 1 to {len(actions)}.")
            continue
        move = actions[choice - 1]
    return move

def player(search_algorithm):
    """A game player who uses the specified search algorithm"""
    return lambda game, state: search_algorithm(game, state)[1]


def cache1(function):
    "Like lru_cache(None), but only considers the first argument of function."
    cache = {}
    def wrapped(x, *args):
        if x not in cache:
            cache[x] = function(x, *args)
        return cache[x]
    return wrapped


def cutoff_depth(d):
    """A cutoff function that searches to depth d."""
    return lambda game, state, depth: depth > d

def h_alphabeta_search(game, state, cutoff=cutoff_depth(6), h=lambda s, p: 0):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = state.to_move

    @cache1
    def max_value(state, alpha, beta, depth):
        if game.is_terminal(state):
            return game.utility(state, player), None
        if cutoff(game, state, depth):
            return h(state, player), None
        v, move = -infinity, None
        for a in game.actions(state):
            v2, _ = min_value(game.result(state, a), alpha, beta, depth+1)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    @cache1
    def min_value(state, alpha, beta, depth):
        if game.is_terminal(state):
            return game.utility(state, player), None
        if cutoff(game, state, depth):
            return h(state, player), None
        v, move = +infinity, None
        for a in game.actions(state):
            v2, _ = max_value(game.result(state, a), alpha, beta, depth + 1)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    return max_value(state, -infinity, +infinity, 0)


class CountCalls:
    """Delegate all attribute gets to the object, and count them in ._counts"""
    def __init__(self, obj):
        self._object = obj
        self._counts = Counter()

    def __getattr__(self, attr):
        "Delegate to the original object, after incrementing a counter."
        self._counts[attr] += 1
        return getattr(self._object, attr)

def report(game, searchers):
    for searcher in searchers:
        game = CountCalls(game)
        searcher(game, game.initial)
        print('Result states: {:7,d}; Terminal tests: {:7,d}; for {}'.format(
            game._counts['result'], game._counts['is_terminal'], searcher.__name__))


# ______________________________________________________________________________
# Monte Carlo tree node and ucb function


class MCT_Node:
    """Node in the Monte Carlo search tree, keeps track of the children states."""

    def __init__(self, parent=None, state=None, U=0, N=0):
        self.__dict__.update(parent=parent, state=state, U=U, N=N)
        self.children = {}
        self.actions = None


def ucb(n, C=1.4):
    return np.inf if n.N == 0 else n.U / n.N + C * np.sqrt(np.log(n.parent.N) / n.N)

# def monte_carlo_tree_search(state, game, N=1000):
def monte_carlo_tree_search(game, state, N=1000):

    def select(n):
        """select a leaf node in the tree"""
        if n.children:
            return select(max(n.children.keys(), key=ucb))
        else:
            return n

    def expand(n):
        """expand the leaf node by adding all its children states"""
        if not n.children and not game.terminal_test(n.state):
            n.children = {MCT_Node(state=game.result(n.state, action), parent=n): action
                          for action in game.actions(n.state)}
        return select(n)

    def simulate(game, state):
        """simulate the utility of current state by random picking a step"""
        player = game.to_move(state)
        while not game.terminal_test(state):
            action = random.choice(list(game.actions(state)))
            state = game.result(state, action)
        v = game.utility(state, player)
        return -v

    def backprop(n, utility):
        """passing the utility back to all parent nodes"""
        if utility > 0:
            n.U += utility
        # if utility == 0:
        #     n.U += 0.5
        n.N += 1
        if n.parent:
            backprop(n.parent, -utility)

    root = MCT_Node(state=state)

    for _ in range(N):
        leaf = select(root)
        child = expand(leaf)
        result = simulate(game, child.state)
        backprop(child, result)

    max_state = max(root.children, key=lambda p: p.N)

    # return root.children.get(max_state)
    return (0, root.children.get(max_state))



def minmax_decision(state, game):  #from games4e.py 
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Figure 5.3]"""

    player = game.to_move(state)

    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a)))
        return v

    def min_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a)))
        return v

    # Body of minmax_decision:
    return max(game.actions(state), key=lambda a: min_value(game.result(state, a)))