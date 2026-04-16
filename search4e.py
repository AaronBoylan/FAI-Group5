#!/usr/bin/env python
# coding: utf-8

# # Search for AIMA 4th edition
# 
# Implementation of search algorithms and search problems for AIMA.
# 
# # Problems and Nodes
# 
# We start by defining the abstract class for a `Problem`; specific problem domains will subclass this. To make it easier for algorithms that use a heuristic evaluation function, `Problem` has a default `h` function (uniformly zero), and subclasses can define their own default `h` function.
# 
# We also define a `Node` in a search tree, and some functions on nodes: `expand` to generate successors; `path_actions` and `path_states`  to recover aspects of the path from the node.  

import random
import heapq
import math
from collections import defaultdict, deque, Counter
import numpy as np

class Problem(object):
    """The abstract class for a formal problem. A new domain subclasses this,
    overriding `actions` and `results`, and perhaps other methods.
    The default heuristic is 0 and the default action cost is 1 for all states.
    When yiou create an instance of a subclass, specify `initial`, and `goal` states 
    (or give an `is_goal` method) and perhaps other keyword args for the subclass."""

    def __init__(self, initial=None, goal=None, **kwds): 
        self.__dict__.update(initial=initial, goal=goal, **kwds) 

    def actions(self, state):        raise NotImplementedError
    def result(self, state, action): raise NotImplementedError
    def is_goal(self, state):        return state == self.goal
    def action_cost(self, s, a, s1): return 1
    def h(self, node):               return 0

    def __str__(self):
        return '{}({!r}, {!r})'.format(
            type(self).__name__, self.initial, self.goal)


class Node:
    "A Node in a search tree."
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.__dict__.update(state=state, parent=parent, action=action, path_cost=path_cost)

    def __repr__(self): return '<{}>'.format(self.state)
    def __len__(self): return 0 if self.parent is None else (1 + len(self.parent))
    def __lt__(self, other): return self.path_cost < other.path_cost


failure = Node('failure', path_cost=math.inf) # Indicates an algorithm couldn't find a solution.
cutoff  = Node('cutoff',  path_cost=math.inf) # Indicates iterative deepening search was cut off.


def expand(problem, node):
    "Expand a node, generating the children nodes."
    s = node.state
    for action in problem.actions(s):
        s1 = problem.result(s, action)
        cost = node.path_cost + problem.action_cost(s, action, s1)
        yield Node(s1, node, action, cost)


def path_actions(node):
    "The sequence of actions to get to this node."
    if node.parent is None:
        return []  
    return path_actions(node.parent) + [node.action]


def path_states(node):
    "The sequence of states to get to this node."
    if node in (cutoff, failure, None): 
        return []
    return path_states(node.parent) + [node.state]


# # Queues
# 
# First-in-first-out and Last-in-first-out queues, and a `PriorityQueue`, which allows you to keep a collection of items, and continually remove from it the item with minimum `f(item)` score.


FIFOQueue = deque

LIFOQueue = list

class PriorityQueue:
    """A queue in which the item with minimum f(item) is always popped first."""

    def __init__(self, items=(), key=lambda x: x): 
        self.key = key
        self.items = [] # a heap of (score, item) pairs
        for item in items:
            self.add(item)

    def add(self, item):
        """Add item to the queuez."""
        pair = (self.key(item), item)
        heapq.heappush(self.items, pair)

    def pop(self):
        """Pop and return the item with min f(item) value."""
        return heapq.heappop(self.items)[1]

    def top(self): return self.items[0][1]

    def __len__(self): return len(self.items)


# # Search Algorithms: Best-First
# 
# Best-first search with various *f(n)* functions gives us different search algorithms. Note that A\*, weighted A\* and greedy search can be given a heuristic function, `h`, but if `h` is not supplied they use the problem's default `h` function (if the problem does not define one, it is taken as *h(n)* = 0).


def best_first_search(problem, f):
    "Search nodes with minimum f(node) value first."
    global reached # <<<<<<<<<<< Only change here
    node = Node(problem.initial)
    frontier = PriorityQueue([node], key=f)
    reached = {problem.initial: node}
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node
        for child in expand(problem, node):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                frontier.add(child)
    return failure


def g(n): return n.path_cost


def astar_search(problem, h=None):
    """Search nodes with minimum f(n) = g(n) + h(n)."""
    h = h or problem.h
    return best_first_search(problem, f=lambda n: g(n) + h(n))


def greedy_bfs(problem, h=None):
    """Search nodes with minimum h(n)."""
    h = h or problem.h
    return best_first_search(problem, f=h)


def depth_first_bfs(problem):
    "Search deepest nodes in the search tree first; using best-first."
    return best_first_search(problem, f=lambda n: -len(n))


class MCT_Node: #from utils4e.py
    """Node in the Monte Carlo search tree, keeps track of the children states."""
    def __init__(self, parent=None, state=None, U=0, N=0):
        self.__dict__.update(parent=parent, state=state, U=U, N=N)
        self.children = {}
        self.actions = None


def mcts_search(problem, h=None, N=1000, max_moves=2000, use_heuristic=True):
    """Monte Carlo tree search for single-agent problems.

    If ``use_heuristic`` is True (default), rollouts pick moves by lowest ``h``
    and non-goal terminal states get a shaped reward from ``h``.
    If False, rollouts are uniformly random and reward is 1.0 only on true goals
    (no heuristic in rollout or as a surrogate goal signal).
    """
    h_fn = h or problem.h

    def terminal_test(state):
        #check for goal or no action available.  i.e. emppty actions list
        return problem.is_goal(state) or not list(problem.actions(state))

    def ucb(n, C=1.4): #from utils4e.py
        return np.inf if n.N == 0 else n.U / n.N + C * np.sqrt(np.log(n.parent.N) / n.N)

    def select(n): #from games4e.py
        """select a leaf node in the tree"""
        if n.children:
            return select(max(n.children.keys(), key=ucb))
        else:
            return n

    def expand(n): #from games4e.py
        """expand the leaf node by adding all its children states"""
        if not n.children and not terminal_test(n.state):
            n.children = {MCT_Node(state=problem.result(n.state, action), parent=n): action
                          for action in list(problem.actions(n.state))}
        return select(n)

    def simulate(problem, state, max_steps=2000):
        """simulate the utility of current state by with hueristics.
        Note it was tried withh pure random rollout, but it did not solve Englishh or French boards.
        heuristics was added to encourage solutions to be found.
        max_steps is a safety cap to avoid infinite random walks in cyclic state spaces.
        """
        rollout = []
        steps = 0

        # Safety cap to avoid infinite random walks in cyclic state spaces.
        while not terminal_test(state) and steps < max_steps:
            actions = list(problem.actions(state))
            if not actions:
                break
            if use_heuristic:
                #check all actions for lowest h value
                scored = [(h_fn(Node(problem.result(state, a))), a) for a in actions]
                #find the best action based on h value
                scored.sort(key=lambda t: t[0])
                min_h = scored[0][0]
                if min_h == math.inf:
                    action = random.choice(actions)
                else:
                    ties = [a for hv, a in scored if hv == min_h]
                    #randomly choose one of the best actions if there are ties
                    action = random.choice(ties)
            else:
                action = random.choice(actions)
            state = problem.result(state, action)
            rollout.append((state, action))
            steps += 1
        if problem.is_goal(state):
            reward = 1.0
        elif use_heuristic:
            #reward shaping
            hv = h_fn(Node(state))
            reward = 0.0 if hv == math.inf else 1.0 / (1.0 + hv)
        else:
            reward = 0.0
        return reward, rollout, state

    def backprop(n, utility): #from games4e.py
        """passing the utility back to all parent nodes"""
        if utility > 0:
            n.U += utility
        # if utility == 0:
        #     n.U += 0.5
        n.N += 1
        if n.parent:
            backprop(n.parent, utility)

    def build_solution_node(tree_child, rollout, tail=None):
        """Convert a tree path + rollout into a search4e.Node chain.

        If `tail` is given (a Node ending at the inner MCTS root state), new
        nodes are appended after it. Otherwise the chain starts from ``problem.initial``.
        """
        chain = []
        n = tree_child
        while n is not None and n.parent is not None:
            a = n.parent.children.get(n)
            chain.append((n.state, a))
            n = n.parent
        chain.reverse()

        current = Node(problem.initial) if tail is None else tail
        for s, a in chain:
            current = Node(s, current, a, current.path_cost + 1)

        for s, a in rollout:
            current = Node(s, current, a, current.path_cost + 1)
        return current

    # Use MCTS as a policy: repeatedly choose the most-visited root child,
    # advancing the state until a goal is reached (or we hit a safety limit).
    state = problem.initial
    current = Node(state)

    for _move in range(max_moves): #limit the number of moves to avoid infinite loops
        if problem.is_goal(state): #check terminal state
            return current

        root = MCT_Node(state=state)

        for _ in range(N):  #ignore the iterator variable _
            leaf = select(root)
            child = expand(leaf)
            result, rollout, end_state = simulate(problem, child.state)
            backprop(child, result)
            if problem.is_goal(end_state):
                return build_solution_node(child, rollout, tail=current)

        if not root.children:
            return current

        #pick node with highest visit count
        max_state = max(root.children, key=lambda p: p.N) #p.N is the visit count of the child node
        #get thhe action that led to the best child
        best_action = root.children.get(max_state)

        if best_action is None:
            return current

        state = max_state.state
        current = Node(state, current, best_action, current.path_cost + 1)

    return current


#A-S-R + B-P-R => A-S-R-P + B-P
def join_nodes(nf, nb):
    """Join the reverse of the backward node nb to the forward node nf."""
    #print('join', S(nf), S(nb))
    join = nf
    while nb.parent is not None:
        cost = join.path_cost + nb.path_cost - nb.parent.path_cost
        join = Node(nb.parent.state, join, nb.action, cost)
        nb = nb.parent
        #print('  now join', S(join), 'with nb', S(nb), 'parent', S(nb.parent))
    return join


class CountCalls:
    """Delegate all attribute gets to the object, and count them in ._counts"""
    def __init__(self, obj):
        self._object = obj
        self._counts = Counter()

    def __getattr__(self, attr):
        "Delegate to the original object, after incrementing a counter."
        self._counts[attr] += 1
        return getattr(self._object, attr)


def report(searchers, problems, verbose=True):
    """Show summary statistics for each searcher (and on each problem unless verbose is false)."""
    for searcher in searchers:
        print(searcher.__name__ + ':')
        total_counts = Counter()
        for p in problems:
            prob   = CountCalls(p)
            soln   = searcher(prob)
            counts = prob._counts; 
            counts.update(actions=len(soln), cost=soln.path_cost)
            total_counts += counts
            if verbose: report_counts(counts, str(p)[:40])
        report_counts(total_counts, 'TOTAL\n')


def report_counts(counts, name):
    """Print one line of the counts report."""
    print('{:9,d} nodes |{:9,d} goal |{:5.0f} cost |{:8,d} actions | {}'.format(
          counts['result'], counts['is_goal'], counts['cost'], counts['actions'], name))