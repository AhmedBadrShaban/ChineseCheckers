import math
import numpy as np

import ChinChecker


class Disk:
    def __init__(self, rows, columns, default_value):
        height = rows
        width = columns - self.fColum(rows)
        self.array = np.ones((height, width)) * default_value

    def get(self, col, row):
        try:
            return self.array[row][col - self.fColum(row)]
        except IndexError:
            return None

    def set(self, col, row, cell):
        self.array[row][col - self.fColum(row)] = cell

    def run(self, func):
        return func(self.array)

class RectangleStorage(Disk):
    def __init__(self, rows, columns, default_value):
        super().__init__(rows, columns, default_value)
        pass
    @staticmethod
    def fColum(row):
        return -math.floor(row / 2)


class Shape:
    def __init__(self, rows, columns, default_value):
        self.rows = rows
        self.columns = columns
        self.disk = RectangleStorage(rows, columns, default_value)

    def __str__(self):
        retval = ''
        for row in range(self.rows):
            if row % 2 == 1:
                retval += ' '
            offset = self.disk.fColum(row)
            for col in range(offset, self.columns + offset):
                value = self.disk.get(col, row)
                if value == 0:
                    retval += 'o'
                elif value > 0:
                    retval += str(int(value))
                else:
                    retval += ' '
                retval += ' '
            retval += '\n'
        return retval
    def getCell(self, col, row):
        return self.disk.get(col, row)

    def setCell(self, col, row, value):
        self.disk.set(col, row, value)

    def fColum(self, r):
        return self.disk.fColum(r)
    def iterate(self):
        for row in range(self.rows):
            offset = self.fColum(row)
            for col in range( offset , self.columns + offset):
                yield col , row

    def move(self, from_col, from_row, to_col, to_row):
        sourceCell = self.disk.get(from_col, from_row)
        self.disk.set(to_col, to_row, sourceCell)
        self.disk.set(from_col, from_row, 0)

    def run(self, func):
        return self.disk.run(func)

    @staticmethod
    def distance(col1, row1, col2, row2):
        return (abs(col1 - col2)
                + abs(col1+ row1 - col2 - row2)
                + abs(row1 -row2)) / 2

if __name__ == '__main__':
    hg = ccai.generate_star()
    print(hg)
    for c in hg.iterate():
        print(c)