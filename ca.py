"""
Cell & Plane class for generating various 2d cellular automata
I used Class attributes to allow for easy reformatting for different output streams such as HTTP
"""
import copy
import random

class Cell:
    fmt = '%s' # others: '%s', '<td>%s</td>'
    states = [' ', '#']

class Plane:
    rowstart = ''    # others: '<tr>', ''
    rowstop = '\n'  # others '</tr></br>', '\n'
    def __init__(self, width=16, height=16):
        self.width = width
        self.height = height
        self.plane = "%s%s%s" % (Plane.rowstart, Cell.fmt * width, Plane.rowstop) * height
        self.cells = [Cell.fmt % random.choice(Cell.states) for x in range(0, width * height)]

    def __str__(self):
        return self.plane % tuple(self.cells)

    def get(self, x, y):
        """
        adjust coords so edge coords 'wrap', (toroidal topology)
         (keeping the IndexError handler for now)
        """
        if y >= self.height:
            y %= self.height
        if y < 0:
            y = self.height-1
        if x >= self.width:
            x %= self.width
        if x < 0:
            x = self.width-1
        try:
            cell = self.cells[y * self.width + x]
        except IndexError:
            cell = None
        return cell

    def set(self, x, y, cell):
        # does not use toroidal topology
        cell = [cell]
        start = y * self.width + x
        if start < 0:
            raise IndexError
        if start >= len(self.cells):
            raise IndexError

        new_cells = self.cells[:start] + cell + self.cells[start+1:]

        self.cells = copy.copy(new_cells)

    def neighbors(self, x, y):
        if y >= self.height:
            y %= self.height
        if y < 0:
            y = self.height-1
        if x >= self.width:
            x %= self.width
        if x < 0:
            x = self.width-1

        return [self.get(x-1, y-1), self.get(x,y-1), self.get(x+1,y-1),
                self.get(x-1,y), self.get(x+1,y),
                self.get(x-1,y+1), self.get(x,y+1), self.get(x+1,y+1)]

    def morph(self, target=5):

        next_gen = [Cell.fmt % calc(self.neighbors(x,y).count('#'), target) # make sure this state is possible
                    for x in range(0, self.width) for y in range(0, self.height)]
        self.cells= []
        self.cells.extend(next_gen)

        return self # a convenience so caller can chain results of multiple mutations on one line


def calc(count, target):
    if count >= target:
        return Cell.states[1]
    else:
        return Cell.states[0]