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
"""
class PegBoardInt:
    empty = 'O'
    peg = 'X'

    def __init__(self, total_holes, init_hole, to_move=None):
        self.total_holes, self.init_hole, self.to_move = total_holes, init_hole, to_move
        self.state = (1 << total_holes) - 1
        self.state ^= (1 << init_hole)

    def actions(self):
        actions = []
        for f, o, t in self.moves_f:
            if (self.state & f) and (self.state & o) and not (self.state & t):
                actions.append((f, o, t))
        return actions

    def result(self, move):
        new_board = self.__class__(self.total_holes, self.init_hole, self.to_move)
        new_board.state = self.state

        f, o, t = move
        new_board.state &= ~f
        new_board.state &= ~o
        new_board.state |= t

        return new_board

    def dead_count(self):
        movable = 0
        for f, o, t in self.moves_f:
            if (self.state & f) and (self.state & o) and not (self.state & t):
                movable |= f
                movable |= o
        return (self.state & ~movable).bit_count()

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        return self.state == other.state

    def __hash__(self):
        return hash(self.state)

    def __repr__(self):
        raise NotImplementedError

def print_actions(actions):
    for f, o, t in actions:
        action = f.bit_length() - 1, o.bit_length() - 1, t.bit_length() - 1
        print(f'Action(from, over, to): {action}')

class EnglishPegBoardInt(PegBoardInt):
    index_map = {
        (0, 2): 0, (0, 3): 1, (0, 4): 2,
        (1, 2): 3, (1, 3): 4, (1, 4): 5,
        (2, 0): 6, (2, 1): 7, (2, 2): 8, (2, 3): 9, (2, 4): 10, (2, 5): 11, (2, 6): 12,
        (3, 0): 13, (3, 1): 14, (3, 2): 15, (3, 3): 16, (3, 4): 17, (3, 5): 18, (3, 6): 19,
        (4, 0): 20, (4, 1): 21, (4, 2): 22, (4, 3): 23, (4, 4): 24, (4, 5): 25, (4, 6): 26,
        (5, 2): 27, (5, 3): 28, (5, 4): 29,
        (6, 2): 30, (6, 3): 31, (6, 4): 32
    }
    moves_f = []

    def __init__(self, total_holes=33, init_hole=16, to_move=None):
        super().__init__(total_holes, init_hole, to_move)
        if not self.moves_f:
            self.gen_moves_forward()

    @property
    def directions(self): #North, South, East, West
        return [(-1, 0), (1, 0), (0, 1), (0, -1)]

    def gen_moves_forward(self):
        index_map = EnglishPegBoardInt.index_map
        for (r, c), start in index_map.items():
            for dr, dc in self.directions:
                over = (r + dr, c + dc)
                to = (r + 2 * dr, c + 2 * dc)
                if over in index_map and to in index_map:
                    f = 1 << start
                    o = 1 << index_map[over]
                    t = 1 << index_map[to]
                    self.moves_f.append((f, o, t))

    def __repr__(self):
        board = [[" "]*7 for _ in range(7)]
        for (r, c), idx in EnglishPegBoardInt.index_map.items():
            if self.state & (1 << idx):
                board[r][c] = self.peg
            else:
                board[r][c] = self.empty
        rows = []
        for r in range(7):
            rows.append(" ".join(board[r]).rstrip())
        return "\n".join(rows)

class TrianglePegBoardInt(PegBoardInt):
    index_map = {
        (0, 0): 0,
        (1, 0): 1, (1, 1): 2,
        (2, 0): 3, (2, 1): 4, (2, 2): 5,
        (3, 0): 6, (3, 1): 7, (3, 2): 8, (3, 3): 9,
        (4, 0): 10, (4, 1): 11, (4, 2): 12, (4, 3): 13, (4, 4): 14
    }
    moves_f = []

    def __init__(self, total_holes=15, init_hole=0, to_move=None):
        super().__init__(total_holes, init_hole, to_move)
        if not self.moves_f:
            self.gen_moves_forward()

    @property
    def directions(self): #East, West, Southeast, Southwest, Northeast, Northwest
        return [(0, 1), (0, -1), (1, 1), (1, 0), (-1, 0), (-1, -1)]

    def gen_moves_forward(self):
        index_map = TrianglePegBoardInt.index_map
        for (r, c), start in index_map.items():
            for dr, dc in self.directions:
                over = (r + dr, c + dc)
                to = (r + 2 * dr, c + 2 * dc)
                if over in index_map and to in index_map:
                    f = 1 << start
                    o = 1 << index_map[over]
                    t = 1 << index_map[to]
                    self.moves_f.append((f, o, t))

    def __repr__(self):
        board = [[" "]*5 for _ in range(5)]
        for (r, c), idx in TrianglePegBoardInt.index_map.items():
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
    def directions(self):
        raise NotImplementedError

    def _clone(self):
        new_board = self.__class__(self.width, self.height, self.init_hole, self.to_move)
        new_board.update(self)
        new_board.pegs = set(self.pegs)
        return new_board

    #Public API
    def actions(self):
        """Return a collection of the allowable moves from this state.
        [((x1, y1), (x2, y2)), ((x3, y3), (x4, y4))] means moving from (x1, y1) to (x2, y2) and (x3, y3) to (x4, y4)"""
        actions = []
        for (r, c) in self.pegs:
            for dr, dc in self.directions:
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
            for dr, dc in self.directions:
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
    def directions(self): #North, South, East, West
        return [(-1, 0), (1, 0), (0, 1), (0, -1)]

    def _in_shape(self, i, j):
        return not((i < 2 or i > 4) and (j < 2 or j > 4))

class TrianglePegBoardDict(PegBoardDict):
    def __init__(self, width=5, height=5, init_hole=(0,0), to_move=None):
        super().__init__(width, height, init_hole, to_move)

    @property
    def directions(self): #East, West, Southeast, Southwest, Northeast, Northwest
        return [(0, 1), (0, -1), (1, 1), (1, 0), (-1, 0), (-1, -1)]

    def _in_shape(self, i, j):
        return j <= i