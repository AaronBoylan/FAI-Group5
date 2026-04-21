#!/usr/bin/env python3
from games4e import *
from peg_board import *

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