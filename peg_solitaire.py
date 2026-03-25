#!/usr/bin/env python3

from peg_board import *
from search4e import *
import copy
import time

class PegSolitaire(Problem):
    """PegSolitaire, a subclass of Problem, is used to find a solution to a Peg Solitaire puzzle.
    It initializes the board according to the input shape, checks legal moves,
    performs actions, compares the state with the goal, and defines three heuristics."""
    def __init__(self, shape='English', reverse=False):
        assert shape in ('English', 'French', 'Triangle')
        self.shape = shape
        if shape == 'English':
            # board = EnglishPegBoardDict()
            board = EnglishPegBoardInt()
        elif shape == 'French':
            board = FrenchPegBoardInt()
        elif shape == 'Triangle':
            # board = TrianglePegBoardDict()
            board = TrianglePegBoardInt()

        self.initial = board
        if isinstance(board, PegBoardDict):
            self.goal = board.init_hole
        else:
            self.goal = copy.copy(self.initial)
            self.goal.state = 1 << board.GOAL_INDEX
            self.goal.pagoda = self.goal.compute_pagoda(self.goal.state)
            self.goal.__dict__.pop("_canon", None)
            self.goal.__dict__.pop("_hash", None)
        self.reverse = reverse

    def actions(self, board):
        """Return a collection of the allowable moves from this state."""
        return board.actions(self.reverse)

    def result(self, board, action):
        """Return the state that results from making a move from a state."""
        return board.result(action, self.reverse)

    def is_goal(self, board):
        """Return True if this is a final state for the game."""
        if isinstance(board, PegBoardDict):
            return len(board.pegs) == 1 and self.goal in board.pegs
        else:
            return board.state == self.goal.state
            # return board.canonical_state() == self.goal.canonical_state()

   # def action_cost(self, s, a, s1):
   #      """Return the value of this final state to player."""
   #      return 1

    def h1(self, board):
        # Number of remaining pegs
        if isinstance(board, PegBoardDict):
            return len(board.pegs) - 1
        else:
            return board.state.bit_count() - 1

    def h2(self, board):
        # Manhattan distance to the goal position
        if isinstance(board, PegBoardDict):
            gi, gj = self.goal
            return sum(abs(i-gi) + abs(j-gj) for (i,j) in board.pegs)
        else:
            return 0

    def h3(self, board):
        # Number of isolated pegs
        return board.count_isolated_pegs()

    def h(self, node):
        board = node.state
        if not board.check_pagoda(self.reverse):
            return float('inf')

        return (
            1.0 * self.h1(board) +
            0.1 * self.h2(board) +
            0.5 * self.h3(board)
        )

def peg_bidirectional_astar_search(problem_f):
    """Bidirectional A* search for Peg Solitaire."""
    problem_b = peg_inverse_problem(problem_f)
    return peg_bidirectional_best_first_search(problem_f, lambda n: g(n) + problem_f.h(n),
                                           problem_b, lambda n: g(n) + problem_b.h(n), peg_terminated)

def peg_bidirectional_uniform_cost_search(problem_f):
    """Bidirectional uniform-cost search."""
    problem_b = peg_inverse_problem(problem_f)
    return peg_bidirectional_best_first_search(problem_f, g,
                                           problem_b, g, peg_terminated)

def peg_bidirectional_best_first_search(problem_f, f_f, problem_b, f_b, peg_terminated):
    """Generic bidirectional best-first search."""
    node_f = Node(problem_f.initial)
    node_b = Node(problem_b.initial)
    frontier_f, reached_f = PriorityQueue([node_f], key=f_f), {node_f.state: node_f}
    frontier_b, reached_b = PriorityQueue([node_b], key=f_b), {node_b.state: node_b}
    solution = failure
    while frontier_f and frontier_b and not peg_terminated(solution, frontier_f, f_f, frontier_b, f_b):
        if len(frontier_f) < len(frontier_b):
            solution = peg_proceed('f', problem_f, frontier_f, reached_f, reached_b, solution)
        else:
            solution = peg_proceed('b', problem_b, frontier_b, reached_b, reached_f, solution)
    return solution

def peg_inverse_problem(problem):
    """Create the reverse search problem for Peg Solitaire bidirectional search."""
    if hasattr(problem, '_object'):
        problem = problem._object

    inv = copy.copy(problem)
    inv.initial, inv.goal = inv.goal, inv.initial
    inv.initial.pagoda = inv.initial.compute_pagoda(inv.initial.state)
    inv.reverse = True

    if hasattr(inv.initial, "_canon"):
        del inv.initial._canon
    if hasattr(inv.initial, "_hash"):
        del inv.initial._hash
    return inv

def peg_terminated(solution, frontier_f, f_f, frontier_b, f_b):
    """Termination condition for Peg Solitaire bidirectional search."""
    if solution is failure:
        return False
    return solution.path_cost <= f_f(frontier_f.top()) + f_b(frontier_b.top())

def peg_proceed(direction, problem, frontier, reached, reached2, solution):
    """Expand one Peg Solitaire node in the given search direction."""
    node = frontier.pop()
    for child in expand(problem, node):
        board = child.state
        key = board._canon if hasattr(board, "_canon") else board.canonical_state()
        if key not in reached or child.path_cost < reached[key].path_cost:
            frontier.add(child)
            reached[key] = child
            if key in reached2:
                solution2 = (
                    join_nodes(child, reached2[key]) if direction == 'f'
                    else join_nodes(reached2[key], child)
                )
                if solution is failure or solution2.path_cost < solution.path_cost:
                    solution = solution2
    return solution

def test_board(peg_sol):
    """Check if board is valid."""
    print('Initial board:\n', peg_sol.initial)
    print('Goal board:\n', peg_sol.goal)
    board = peg_sol.initial
    print('MOVES:\n', board.MOVES)
    actions = peg_sol.actions(board)

    while actions:
        print('Legal actions:\n', actions)
        board = peg_sol.result(board, actions[0])
        print('After performing ', actions[0], '\n', board)
        actions = peg_sol.actions(board)

def test_performance(searchers, shapes, verbose=True):
    """Show summary statistics for each searcher (and on each problem unless verbose is false)."""
    for searcher in searchers:
        print(f'\n{searcher.__name__}:')
        total_counts = Counter()
        for shape in shapes:
            problem = PegSolitaire(shape=shape)
            time_ms, counts = run_search(searcher, problem)
            total_counts += counts
            if verbose: print_time_counts(time_ms, counts, str(problem)[:12] + ' ' + problem.shape)

def test_data_structures():
    return

from itertools import permutations

def test_directions(searcher, shape):
    DIR = {'North': (-1, 0), 'South': (1, 0), 'East': (0, 1), 'West': (0, -1)}

    print(f'\n{searcher.__name__} on {shape} board')

    if shape == 'English':
        board = EnglishPegBoardInt
    elif shape == 'French':
        board = FrenchPegBoardInt
    else:
        board = TrianglePegBoardInt

    for names in permutations(DIR.keys()):
        directions = [DIR[n] for n in names]
        board.DIRECTIONS = directions

        problem = PegSolitaire(shape=shape)
        time_ms, counts = run_search(searcher, problem)
        print_time_counts(time_ms, counts, f'{shape} {list(names)}')

def run_search(searcher, problem):
    prob = peg_CountCalls(problem)

    start = time.perf_counter()
    soln = searcher(prob)
    end = time.perf_counter()

    time_ms = (end - start) * 1000

    counts = prob._counts
    counts.update(actions=len(soln), cost=soln.path_cost)

    return time_ms, counts

def print_time_counts(time, counts, name):
    """Print one line of the counts report."""
    print('{:7.2f} ms {:9,d} nodes |{:9,d} goal |{:5.0f} cost |{:8,d} actions | {}'.format(
          time, counts['result'], counts['is_goal'], counts['cost'], counts['actions'], name))

class peg_CountCalls:
    """Delegate all attribute gets to the object, and count them in ._counts"""
    def __init__(self, obj):
        self._object = obj
        self._counts = Counter()

    def __getattr__(self, attr):
        "Delegate to the original object, after incrementing a counter."
        if attr in ('_object', '_counts'):
            return object.__getattribute__(self, attr)
        self._counts[attr] += 1
        return getattr(self._object, attr)