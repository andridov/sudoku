"""
The MIT License (MIT)

Copyright (c) 2024 Andridov.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

class Cell:
    def __init__(self, val, candidates={}):
        self.value = val
        self.candidates = candidates if candidates else \
            {1, 2, 3, 4, 5, 6, 7, 8, 9} if not val else {}

    def __str__(self) -> str:
        return f'{self.value} ' # comment this return-line to see the candidates
        return f"{self.value}:{''.join(str(c) for c in self.candidates):9} "
    
    def exclude_ch(self, val):
        if self.value:
            self.candidates = {}
            return
        if self.candidates and val in self.candidates:
            self.candidates.remove(val)
            if len(self.candidates) == 1:
                self.value = self.candidates.pop()


class Board:
    def __init__(self, a):
        self.arr = a
        self.sqrs = []
        for i in range(3):
            for j in range(3):
                self.sqrs.append(
                    [a[3*i+0][3*j], a[3*i+0][3*j+1], a[3*i+0][3*j+2],
                     a[3*i+1][3*j], a[3*i+1][3*j+1], a[3*i+1][3*j+2],
                     a[3*i+2][3*j], a[3*i+2][3*j+1], a[3*i+2][3*j+2]])
        self.rows = [[a[i][j] for j in range(9)] for i in range(9)]
        self.cols = [[a[j][i] for j in range(9)] for i in range(9)]
        
    @classmethod
    def from2dArr(cls, arr2d):
        return cls([[Cell(arr2d[i][j]) for j in range(9)] for i in range(9)])
        # return cls(a)

    @classmethod
    def fromBoard(cls, board):
        a = [[Cell(board.arr[i][j].value, board.arr[i][j].candidates.copy()) \
            for j in range(9)] for i in range(9)]
        return cls(a)

    def is_valid(self) -> bool:
        def chk(group) -> bool:
            for g in group:
                gv = [x.value for x in g]
                for i in range(1,10):
                    if gv.count(i) > 1:
                        return False
            return True
        if chk(self.rows) and chk(self.cols) and chk(self.sqrs):
            return True
        return False
    
    def is_filled(self) -> bool:
        for i in range(9):
            for j in range(9):
                if not self.arr[i][j].value:
                    return False
        return True
    
    def print(self):
        for n in range (9):
            print('{}{}{}  {}{}{}  {}{}{}{}'.format( *self.arr[n]
                , '' if n not in [2,5,8] else '\n') )
    
        
class Sudoku:
    def solve(self, board):
        self.__solve(board, *self.__next_pos(board, 0, 0))

    def __iterate_cells(self, board):
        def strike(arr, val):
            for c in arr:
                c.exclude_ch(val)
        for i in range(9):
            for j in range(9):
                if value := board.arr[i][j].value:
                    strike(board.rows[i], value)
                    strike(board.cols[j], value)
                    strike(board.sqrs[3*(i//3)+(j//3)], value) 

    def __next_pos(self, board, i, j):
        while True:
            j += 1
            if j > 8:
                j = 0
                i += 1
                if i > 8:
                    print('There is no solution for input data you provided !')
                    exit(1)
            if not board.arr[i][j].value:
                return (i, j)
        
    def __solve(self, board, i, j):
        candidates = board.arr[i][j].candidates.copy()
        # print(f's1: ({i},{j}) v={board.arr[i][j].value}, c={candidates}')
        while len(candidates) > 0:
            b = Board.fromBoard(board)
            b.arr[i][j].value = candidates.pop()
            b.arr[i][j].candidates = {}
            # print(f's2: pos=({i},{j}) v={b.arr[i][j].value}, c={candidates}')
            self.__iterate_cells(b)
            # b.print()
            if b.is_valid():
                if b.is_filled():
                    print(f'Solution:')
                    b.print()
                    exit(0)
                # print(f's3: ({i},{j}) v={b.arr[i][j].value}, c={candidates}')
                self.__solve(b, *self.__next_pos(b, i, j))
            # else:
            #     print(f's4: Not valid {i},{j} -- {b.arr[i][j].value}')
            # print(f's5: ({i},{j}) is done. Go next\n\n')

        
def main():
    b = Board.from2dArr([
        [8, 0, 0,   0, 0, 0,   0, 0, 0],
        [0, 0, 3,   6, 0, 0,   0, 0, 0],
        [0, 7, 0,   0, 9, 0,   2, 0, 0],

        [0, 5, 0,   0, 0, 7,   0, 0, 0],
        [0, 0, 0,   0, 4, 5,   7, 0, 0],
        [0, 0, 0,   1, 0, 0,   0, 3, 0],

        [0, 0, 1,   0, 0, 0,   0, 6, 8],
        [0, 0, 8,   5, 0, 0,   0, 1, 0],
        [0, 9, 0,   0, 0, 0,   4, 0, 0]])
    Sudoku().solve(b)


if __name__ == "__main__":
    main()
    
