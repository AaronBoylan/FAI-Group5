"""
EnglishPegBoard Bit Mapping (1: Peg, 0: Empty Hole)
          0   1   2
          3   4   5
  6   7   8   9  10  11  12
 13  14  15  16  17  18  19
 20  21  22  23  24  25  26
         27  28  29
         30  31  32

TrianglePegBoard Bit Mapping (1: Peg, 0: Empty Hole)
 0
 1	 2
 3	 4	 5
 6	 7	 8	 9
10	11	12	13	14

MOVES is a precomputed list of tuples: (f, o, t, delta), which is used to store:
1. legal move index: from index, over index, and to index
2. pagoda delta: (pagoda value of to) - (pagoda value of from) - (pagoda value of over)

SYM_MAPS is a precomputed list of symmetry mapping:
identity (no rotation), rotate 90 degree, 180 degree, 270 degree
flip horizontally, flip vertically, flip along the main diagonal, and flip along the anti-diagonal
"""
import copy

class PegBoardInt:
    empty = 'O'
    peg = 'X'
    MOVES = []
    SYM_MAPS = []

    def __init__(self, total_holes, init_hole, to_move):
        self.total_holes, self.init_hole, self.to_move = total_holes, init_hole, to_move
        self.state = (1 << total_holes) - 1
        self.state ^= (1 << init_hole)
        self.pagoda = self.compute_pagoda(self.state)

    def actions(self, reverse=False):
        """Generate all possible actions.
        Forward search (reverse=False), (Peg, Peg, Empty) is a legal action
        Backward search (reverse=True), (Peg, Empty, Empty) is a legal action"""
        actions = []
        if not reverse:
            for f, o, t, delta in self.MOVES:
                if (self.state & f) and (self.state & o) and not (self.state & t):
                    actions.append((f, o, t, delta))
        else:
            for f, o, t, delta in self.MOVES:
                if (self.state & f) and not (self.state & o) and not (self.state & t):
                    actions.append((f, o, t, delta))
        return actions

    def result(self, move, reverse=False):
        """Apply the move and update the pagoda value.
        Forward move (reverse=False), (Peg, Peg, Empty) -> (Empty, Empty, Peg)
        Backward move (reverse=True), (Peg, Empty, Empty) -> (Empty, Peg, Peg)"""
        new_board = copy.copy(self)
        if hasattr(new_board, "_canon"):
            del new_board._canon
        if hasattr(new_board, "_hash"):
            del new_board._hash

        f, o, t, delta = move
        if not reverse:
            new_board.state &= ~f
            new_board.state &= ~o
            new_board.state |= t
            new_board.pagoda = self.pagoda + delta
        else:
            new_board.state &= ~f
            new_board.state |= o
            new_board.state |= t
            new_board.pagoda = self.pagoda - delta

        return new_board

    def canonical_state(self):
        """Return the canonical state under symmetry to reduce the redundant node."""
        if hasattr(self, "_canon"):
            return self._canon
        s = self.state
        best = s
        maps = self.__class__.SYM_MAPS
        for perm in maps:
            t = self.apply_symmetry(s, perm)
            if t < best:
                best = t
        self._canon = best
        return best

    @staticmethod
    def apply_symmetry(state, perm):
        """Convert a state using a symmetry mapping."""
        new_state = 0
        for i, p in enumerate(perm):
            if state & (1 << i):
                new_state |= (1 << p)
        return new_state

    def check_pagoda(self, reverse=False):
        """Check the pagoda constraint against the goal state.
        Forward move (reverse=False): current pagoda >= goal pagoda
        Backward move (reverse=True): current pagoda <= goal pagoda
        Return False if the state cannot reach the goal."""
        if self.pagoda is None:
            return True
        if not reverse:
            return self.pagoda >= type(self).GOAL_PAGODA
        else:
            return self.pagoda <= type(self).GOAL_PAGODA

    def compute_pagoda(self, state):
        """Count pagoda score of entire board"""
        if not hasattr(type(self), "PAGODA"):
            return None
        weights = type(self).PAGODA
        value = 0
        for i in range(self.total_holes):
            if state & (1 << i):
                value += weights[i]
        return value

    def check_parity(self):
        """Parity check"""
        return True

    def check_merson(self):
        """Merson region check"""
        return True

    def count_isolated_pegs(self, reverse=False):
        """Count isolated pegs, called by heuristic function"""
        movable = 0
        if not reverse:
            for f, o, t, _ in self.MOVES:
                if (self.state & f) and (self.state & o) and not (self.state & t):
                    movable |= f
        else:
            for f, o, t, _ in self.MOVES:
                if (self.state & f) and not (self.state & o) and not (self.state & t):
                    movable |= f
        return (self.state & ~movable).bit_count()

    def lookup_pdb(self):
        """Pattern Database, called by heuristic function"""
        return 0

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        return self.state == other.state

    def __hash__(self):
        return hash(self.state)

    def __repr__(self):
        raise NotImplementedError

def print_actions(actions):
    for f, o, t, _ in actions:
        action = f.bit_length() - 1, o.bit_length() - 1, t.bit_length() - 1
        print(f'Action(from, over, to): {action}')

class EnglishPegBoardInt(PegBoardInt):
    INDEX_MAP = {
        (0, 2): 0, (0, 3): 1, (0, 4): 2,
        (1, 2): 3, (1, 3): 4, (1, 4): 5,
        (2, 0): 6, (2, 1): 7, (2, 2): 8, (2, 3): 9, (2, 4): 10, (2, 5): 11, (2, 6): 12,
        (3, 0): 13, (3, 1): 14, (3, 2): 15, (3, 3): 16, (3, 4): 17, (3, 5): 18, (3, 6): 19,
        (4, 0): 20, (4, 1): 21, (4, 2): 22, (4, 3): 23, (4, 4): 24, (4, 5): 25, (4, 6): 26,
        (5, 2): 27, (5, 3): 28, (5, 4): 29,
        (6, 2): 30, (6, 3): 31, (6, 4): 32
    }
    PAGODA = [
          #       0, 0, 1,
          #       0, 1, 0,
          # 1, 0, 1, 0, 1, 0, 1,
          # 0, 1, 0, 2, 0, 1, 0,
          # 1, 0, 1, 0, 1, 0, 1,
          #       0, 1, 0,
          #       0, 0, 1
          #
          #       0, 0, 0,
          #       0, 1, 0,
          # 0, 0, 0, 0, 0, 0, 0,
          # 0, 1, 0, 1, 0, 1, 0,
          # 0, 0, 0, 0, 0, 0, 0,
          #       0, 1, 0,
          #       0, 0, 0
          #
                0, 0, 0,
                0, 1, 0,
         -1, 1, 0, 1, 0, 1, -1,
          0, 2, 0, 2, 0, 2, 0,
         -1, 1, 0, 1, 0, 1, -1,
                0, 1, 0,
                0, 0, 0

          #       0, 1, 0,
          #       1, 0, 1,
          # 0, 1, 0, 1, 0, 1, 0,
          # 1, 0, 2, 0, 2, 0, 1,
          # 0, 1, 0, 1, 0, 1, 0,
          #       1, 0, 1,
          #       0, 1, 0
    ]
    GOAL_INDEX = 16
    GOAL_PAGODA = PAGODA[GOAL_INDEX]

    def __init__(self, total_holes=33, init_hole=16, to_move=None):
        super().__init__(total_holes, init_hole, to_move)
        if not self.MOVES:
            self.gen_moves()
        if not self.SYM_MAPS:
            self.gen_symmetry_maps()

    @property
    def DIRECTIONS(self): #North, South, East, West
        return [(-1, 0), (1, 0), (0, 1), (0, -1)]

    def gen_moves(self):
        INDEX_MAP = EnglishPegBoardInt.INDEX_MAP
        for (r, c), start in INDEX_MAP.items():
            for dr, dc in self.DIRECTIONS:
                over = (r + dr, c + dc)
                to = (r + 2 * dr, c + 2 * dc)
                if over in INDEX_MAP and to in INDEX_MAP:
                    f = 1 << start
                    o = 1 << INDEX_MAP[over]
                    t = 1 << INDEX_MAP[to]

                    fi = start
                    oi = INDEX_MAP[over]
                    ti = INDEX_MAP[to]
                    delta = self.PAGODA[ti] - self.PAGODA[fi] - self.PAGODA[oi]
                    self.MOVES.append((f, o, t, delta))

    def gen_symmetry_maps(self):
        coords = {v: k for k, v in self.INDEX_MAP.items()}
        def rot90(r, c):    return (c, 6 - r)
        def rot180(r, c):   return (6 - r, 6 - c)
        def rot270(r, c):   return (6 - c, r)
        def mirror_h(r, c): return (6 - r, c)
        def mirror_v(r, c): return (r, 6 - c)
        transforms = [lambda r, c: (r, c), rot90, rot180, rot270,
                      mirror_h, mirror_v, lambda r, c: rot90(*mirror_h(r, c)), lambda r, c: rot90(*mirror_v(r, c))]
        maps = []

        for T in transforms:
            perm = [0] * 33
            for i, (r, c) in coords.items():
                r2, c2 = T(r, c)
                perm[i] = self.INDEX_MAP[(r2, c2)]
            maps.append(perm)

        type(self).SYM_MAPS = maps

    def __repr__(self):
        board = [[" "]*7 for _ in range(7)]
        for (r, c), idx in EnglishPegBoardInt.INDEX_MAP.items():
            if self.state & (1 << idx):
                board[r][c] = self.peg
            else:
                board[r][c] = self.empty
        rows = []
        for r in range(7):
            rows.append(" ".join(board[r]).rstrip())
        return "\n".join(rows)

class TrianglePegBoardInt(PegBoardInt):
    INDEX_MAP = {
        (0, 0): 0,
        (1, 0): 1, (1, 1): 2,
        (2, 0): 3, (2, 1): 4, (2, 2): 5,
        (3, 0): 6, (3, 1): 7, (3, 2): 8, (3, 3): 9,
        (4, 0): 10, (4, 1): 11, (4, 2): 12, (4, 3): 13, (4, 4): 14
    }
    MOVES = []

    def __init__(self, total_holes=15, init_hole=0, to_move=None):
        super().__init__(total_holes, init_hole, to_move)
        if not self.MOVES:
            self.gen_moves()

    @property
    def DIRECTIONS(self): #East, West, Southeast, Southwest, Northeast, Northwest
        return [(0, 1), (0, -1), (1, 1), (1, 0), (-1, 0), (-1, -1)]

    def gen_moves(self):
        INDEX_MAP = TrianglePegBoardInt.INDEX_MAP
        for (r, c), start in INDEX_MAP.items():
            for dr, dc in self.DIRECTIONS:
                over = (r + dr, c + dc)
                to = (r + 2 * dr, c + 2 * dc)
                if over in INDEX_MAP and to in INDEX_MAP:
                    f = 1 << start
                    o = 1 << INDEX_MAP[over]
                    t = 1 << INDEX_MAP[to]
                    self.MOVES.append((f, o, t, 0))

    def __repr__(self):
        board = [[" "]*5 for _ in range(5)]
        for (r, c), idx in TrianglePegBoardInt.INDEX_MAP.items():
            if self.state & (1 << idx):
                board[r][c] = self.peg
            else:
                board[r][c] = self.empty
        rows = []
        for r in range(5):
            rows.append(" ".join(board[r]).rstrip())
        return "\n".join(rows)

from collections import defaultdict
"""
EnglishPegBoard Coordinate				
    	       	0, 2	0, 3	0, 4	
               	1, 2	1, 3	1, 4	
2, 0	2, 1	2, 2	2, 3	2, 4	2, 5	2, 6
3, 0	3, 1	3, 2	3, 3	3, 4	3, 5	3, 6
4, 0	4, 1	4, 2	4, 3	4, 4	4, 5	4, 6
               	5, 2	5, 3	5, 4	
               	6, 2	6, 3	6, 4	

TrianglePegBoard Coordinate
0, 0	
1, 0	1, 1	
2, 0	2, 1	2, 2	
3, 0	3, 1	3, 2	3, 3	
4, 0	4, 1	4, 2	4, 3	4, 4
"""
class PegBoardDict(defaultdict):
    """PegBoard is used to store the state of a board for Peg Solitaire or Duotaire
    This is a generic class that handles the game rules.
    Agents should create an instance of EnglishPegBoard or TrianglePegBoard to initialize the board.
    """
    invalid = '_'
    empty = 'O'
    peg = 'X'

    def __init__(self, width, height, init_hole, to_move=None):
        """to_move should only be used by Peg Duotaire"""
        super().__init__()
        self.width, self.height, self.init_hole, self.to_move = width, height, init_hole, to_move
        self.pegs = set()

        for i in range(self.height):
            for j in range(self.width):
                if (i, j) == self.init_hole:
                    self[(i, j)] = self.empty
                elif self._in_shape(i,j):
                    self[(i, j)] = self.peg
                    self.pegs.add((i, j))
                else:
                    self[(i, j)] = self.invalid

    def _in_shape(self, i, j):
        raise NotImplementedError

    @property
    def DIRECTIONS(self):
        raise NotImplementedError

    def _clone(self):
        new_board = type(self)(self.width, self.height, self.init_hole, self.to_move)
        new_board.update(self)
        new_board.pegs = set(self.pegs)
        return new_board

    #Public API
    def actions(self):
        """Return a collection of the allowable moves from this state.
        [((x1, y1), (x2, y2)), ((x3, y3), (x4, y4))] means moving from (x1, y1) to (x2, y2) and (x3, y3) to (x4, y4)"""
        actions = []
        for (r, c) in self.pegs:
            for dr, dc in self.DIRECTIONS:
                over = (r + dr, c + dc)
                to = (r + 2 * dr, c + 2 * dc)
                if self[to] == self.empty and self[over] == self.peg:
                    actions.append(((r, c), to))
        return actions

    def result(self, move):
        """Return the state that results from making a move from a state."""
        new_board = self._clone()
        (i, j), (to_i, to_j) = move
        mid_i, mid_j = i + (to_i-i)//2, j + (to_j-j)//2

        new_board[(i, j)] = self.empty
        new_board[(mid_i, mid_j)] = self.empty
        new_board[(to_i, to_j)] = self.peg

        new_board.pegs.remove((i, j))
        new_board.pegs.remove((mid_i, mid_j))
        new_board.pegs.add((to_i, to_j))

        new_board.to_move = 'O' if self.to_move == 'X' else 'X'
        return new_board

    def dead_count(self):
        dead = 0
        for (r, c) in self.pegs:
            movable = False
            for dr, dc in self.DIRECTIONS:
                over = (r + dr, c + dc)
                to = (r + 2 * dr, c + 2 * dc)
                if self[to] == self.empty and self[over] == self.peg:
                    movable = True
                    break
            if not movable:
                dead += 1
        return dead

    def __eq__(self, other):
        return dict(self) == dict(other)

    def __hash__(self):
        return hash(tuple(sorted(self.items())))

    def __missing__(self, key):
        i, j = key
        if i < 0 or i >= self.height or j < 0 or j >= self.width:
            return self.invalid
        return self.empty if self._in_shape(i, j) else self.invalid

    def __repr__(self):
        rows = []
        for i in range(self.height):
            row = [self[(i, j)] for j in range(self.width)]
            rows.append(" ".join(row))
        return "\n".join(rows)

class EnglishPegBoardDict(PegBoardDict):
    def __init__(self, width=7, height=7, init_hole=(3, 3), to_move=None):
        super().__init__(width, height, init_hole, to_move)

    @property
    def DIRECTIONS(self): #North, South, East, West
        return [(-1, 0), (1, 0), (0, 1), (0, -1)]

    def _in_shape(self, i, j):
        return not((i < 2 or i > 4) and (j < 2 or j > 4))

class TrianglePegBoardDict(PegBoardDict):
    def __init__(self, width=5, height=5, init_hole=(0,0), to_move=None):
        super().__init__(width, height, init_hole, to_move)

    @property
    def DIRECTIONS(self): #East, West, Southeast, Southwest, Northeast, Northwest
        return [(0, 1), (0, -1), (1, 1), (1, 0), (-1, 0), (-1, -1)]

    def _in_shape(self, i, j):
        return j <= i