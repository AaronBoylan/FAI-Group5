#!/usr/bin/env python3
from games4e import Game
from peg_board import EnglishPegBoard, TrianglePegBoard

class PegDuotaire(Game):
    """PegDuotaire, a subclass of Game, represents one player in a Peg Duotaire game."""
    def __init__(self, shape='English'):
        assert shape == 'English' or shape == 'Triangle'
        if shape == 'English':
            board = EnglishPegBoard(to_move='X')
        elif shape == 'Triangle':
            board = TrianglePegBoard(to_move='X')

        self.initial = board

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
        return not board.actions()

    def utility(self, board, player):
        """Return the value of this final state to player."""
        if board.to_move == player:
            return -1
        else:
            return 1