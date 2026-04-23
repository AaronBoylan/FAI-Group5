#!/usr/bin/env python3

#from main import *
from peg_solitaire import *
from peg_duotaire import *
from peg_board import *
from search4e import *
from games4e import *
import time

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

"""{'depth_first_bfs': {
        'Triangle': {
            'time_ms': 6.856707972474396,
            'counts': Counter(
                {'result': 494, 'action_cost': 494, 'actions': 265, 'is_goal': 253, 'cost': 13, 'initial': 2})
        },
        'English': {
            'time_ms': 29.019667010288686,
            'counts': Counter(
                {'result': 2509, 'action_cost': 2509, 'actions': 1123, 'is_goal': 1093, 'cost': 31, 'initial': 2})
        },
    },
    'greedy_bfs': {
        'Triangle': {
            'time_ms': 1.021541014779359, 
            'counts': Counter(
                {'result': 106, 'action_cost': 106, 'actions': 64, 'is_goal': 52, 'cost': 13, 'initial': 2, 'h': 1})
        },               
        'English': {
            'time_ms': 158.05516595719382, 
            'counts': Counter(
                {'result': 32970, 'action_cost': 32970, 'actions': 7382, 'is_goal': 7352, 'cost': 31,'initial': 2, 'h': 1})
        }
    }
"""
def test_performance(searchers, shapes, verbose=False):
    """Show summary statistics for each searcher (and on each problem unless verbose is false)."""
    results = {}
    for searcher in searchers:
        # name = searcher.__name__
        from utils import SEARCH_ALGORITHMS
        name = [v['short_name'] for k, v in SEARCH_ALGORITHMS.items() if v['method'] == searcher][0]
        results[name] = {}
        print(f'\n{name}:')

        total_counts = Counter()
        for shape in shapes:
            problem = PegSolitaire(shape=shape)
            time_ms, counts = run_search(searcher, problem)

            results[name][shape] = {
                'time_ms': time_ms,
                'counts': counts.copy()
            }

            total_counts += counts

            print_time_counts(time_ms, counts, str(problem)[:12] + ' ' + problem.shape)

        # results[name]['total_counts'] = total_counts

    if verbose:
        compare_search_algorithms(results)

    return results

def test_data_structures():
    from pympler import asizeof

    # Define the Tracking Wrapper
    original_PQ = search4e.PriorityQueue

    class TrackingPriorityQueue(original_PQ):
        # We'll use a class variable to keep track across the search
        max_size = 0

        def add(self, item):
            super().add(item)
            # Update the peak size whenever an item is added
            TrackingPriorityQueue.max_size = max(TrackingPriorityQueue.max_size, len(self))

        @classmethod
        def reset_tracker(cls):
            cls.max_size = 0

    # Monkey Patch the global PriorityQueue
    search4e.PriorityQueue = TrackingPriorityQueue

    try:
        # TEST 1: DefaultDict
        print('Testing DefaultDict')

        TrackingPriorityQueue.reset_tracker()

        peg_sol_dict = PegSolitaireDict(shape='English')
        time_ms, counts = run_search(astar_search, peg_sol_dict)

        size = asizeof.asizeof(peg_sol_dict.initial.pegs)
        max_nodes = TrackingPriorityQueue.max_size
        throughput = counts['result']/(time_ms/1000)

        print(f'State Size: {size} bytes')
        print(f'Max Frontier Nodes: {max_nodes:,}')
        print(f'Max Frontier Size: {size*max_nodes/(1024*1024):.2f} MB')
        print(f'Throughput: {throughput:,.2f} (Nodes per Second)')
        print_time_counts(time_ms, counts, 'Dict English')

        # TEST 2: Bitmask
        print('\nTesting Bitmask')

        TrackingPriorityQueue.reset_tracker()

        peg_sol = PegSolitaire(shape='English')
        time_ms, counts = run_search(astar_search, peg_sol)

        size = asizeof.asizeof(peg_sol.initial.state)
        max_nodes = TrackingPriorityQueue.max_size
        throughput = counts['result']/(time_ms/1000)

        print(f'State Size: {size} bytes')
        print(f'Max Frontier Nodes: {max_nodes:,}')
        print(f'Max Frontier Size: {size*max_nodes/(1024*1024):.2f} MB')
        print(f'Throughput: {throughput:,.2f} (Nodes per Second)')
        print_time_counts(time_ms, counts, 'Bitmask English')

    finally:
        # Restore the original PriorityQueue to avoid side effects
        search4e.PriorityQueue = original_PQ

from itertools import permutations

def test_directions(searcher, shape):
    print(f'\n{searcher.__name__} on {shape} board')

    if shape == 'English' or shape == 'French':
        DIR = {'North': (-1, 0), 'South': (1, 0), 'East': (0, 1), 'West': (0, -1)}
    elif shape == 'Triangle':
        DIR = {'East': (0, 1), 'West': (0, -1), 'Southeast': (1, 1), 'Southwest': (1, 0), 'Northeast': (-1, 0), 'Northwest': (-1, -1)}

    for names in permutations(DIR.keys()):
        directions = [DIR[n] for n in names]

        problem = PegSolitaire(shape=shape)
        problem.initial.DIRECTIONS = directions
        problem.initial.__class__.MOVES = []
        problem.initial.gen_moves()

        # print(problem.initial.MOVES)

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
    