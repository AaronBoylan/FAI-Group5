#!/usr/bin/env python3


from peg_board import *
from search4e import *

class PegSolitaire(Problem):
    """PegSoltaire, a subclass of Problem, is used to find a solution to a Peg Solitaire puzzle.
    It initializes the board according to the input shape, checks legal moves,
    performs actions, compares the state with the goal, and defines three heuristics."""
    def __init__(self, shape='English'):
        assert shape == 'English' or shape == 'Triangle'
        if shape == 'English':
            # board = EnglishPegBoardDict()
            board = EnglishPegBoardInt()
        elif shape == 'Triangle':
            # board = TrianglePegBoardDict()
            board = TrianglePegBoardInt()

        self.initial = board
        if isinstance(board, PegBoardDict):
            self.goal = board.init_hole
        else:
            self.goal = 1 << board.init_hole

    def actions(self, board):
        """Return a collection of the allowable moves from this state."""
        return board.actions()

    def result(self, board, action):
        """Return the state that results from making a move from a state."""
        return board.result(action)

    def is_goal(self, board):
        """Return True if this is a final state for the game."""
        if isinstance(board, PegBoardDict):
            return len(board.pegs) == 1 and self.goal in board.pegs
        else:
            return board.state.bit_count() == 1 and board.state == self.goal

   # def action_cost(self, s, a, s1):
   #      """Return the value of this final state to player."""
   #      return 1

    def h1(self, board):
        # peg count heuristic
        if isinstance(board, PegBoardDict):
            return len(board.pegs) - 1
        else:
            return board.state.bit_count() - 1

    def h2(self, board):
        # distance heuristic
        if isinstance(board, PegBoardDict):
            gi, gj = self.goal
            return sum(abs(i-gi) + abs(j-gj) for (i,j) in board.pegs)
        else:
            return 0

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