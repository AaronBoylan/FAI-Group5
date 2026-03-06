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
class PegBoard(defaultdict):
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
        for (i, j) in self.pegs:
            for di, dj in self.directions:
                to_i, to_j = i + di, j + dj
                mid_i, mid_j = i + di//2, j + dj//2
                if self[(to_i, to_j)] == self.empty and self[(mid_i, mid_j)] == self.peg:
                    actions.append(((i, j), (to_i, to_j)))
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
        for (i, j) in self.pegs:
            movable = False
            for di, dj in self.directions:
                to_i, to_j = i + di, j + dj
                mid_i, mid_j = i + di//2, j + dj//2
                if self[(to_i, to_j)] == self.empty and self[(mid_i, mid_j)] == self.peg:
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

class EnglishPegBoard(PegBoard):
    def __init__(self, width=7, height=7, init_hole=(3, 3), to_move=None):
        super().__init__(width, height, init_hole, to_move)

    @property
    def directions(self): #North, South, East, West
        return [(-2, 0), (2, 0), (0, 2), (0, -2)]

    def _in_shape(self, i, j):
        return not((i < 2 or i > 4) and (j < 2 or j > 4))

class TrianglePegBoard(PegBoard):
    def __init__(self, width=5, height=5, init_hole=(0,0), to_move=None):
        super().__init__(width, height, init_hole, to_move)

    @property
    def directions(self): #East, West, Southeast, Southwest, Northeast, Northwest
        return [(0, 2), (0, -2), (2, 2), (2, 0), (-2, 0), (-2, -2)]

    def _in_shape(self, i, j):
        return j <= i