#!/usr/bin/env python3

from peg_board import EnglishPegBoard, TrianglePegBoard
from peg_board import *
from search4e import *

class PegSolitaire(Problem):
    """PegSoltaire, a subclass of Problem, is used to find a solution to a Peg Solitaire puzzle.
    It initializes the board according to the input shape, checks legal moves,
    performs actions, compares the state with the goal, and defines three heuristics."""
    def __init__(self, shape='English'):
        assert shape == 'English' or shape == 'Triangle'
        if shape == 'English':
            board = EnglishPegBoard()
        elif shape == 'Triangle':
            board = TrianglePegBoard()

        self.initial = board
        self.goal = board.init_hole

    def actions(self, board):
        """Return a collection of the allowable moves from this state."""
        return board.actions()

    def result(self, board, action):
        """Return the state that results from making a move from a state."""
        return board.result(action)

    def is_goal(self, board):
        """Return True if this is a final state for the game."""
        return len(board.pegs) == 1 and self.goal in board.pegs

   # def action_cost(self, s, a, s1):
   #      """Return the value of this final state to player."""
   #      return 1

    def h1(self, board):
        # peg count heuristic
        return len(board.pegs) - 1

    def h2(self, board):
        # distance heuristic
        gi, gj = self.goal
        return sum(abs(i-gi) + abs(j-gj) for (i,j) in board.pegs)

    def h3(self, board):
        # dead pegs heuristic
        return board.dead_count()

    def h(self, node):
        board = node.state
        return (
            1.0 * self.h1(board) +
            0.1 * self.h2(board) +
            0.5 * self.h3(board)
        )