import random
import math
import os
from msvcrt import getch

WASD_TO_A = {'w':'U', 'a':'L', 's':'D', 'd':'R'}

class Game:
    def __init__(self, size=4, can_four=True):
        self.board = [[None]*size for _ in range(size)]
        self.size = size
        self.fill = 0
        self.moves = 0
        self.can_move = True
        self.score = 0
        self.can_four = can_four
        self.new_piece()
        self.display_board()

    def run(self):
        while self.can_move:
            inp = getch().decode("utf-8").lower()
            if inp == 'l':
                break
            action = WASD_TO_A.get(inp)
            if not action:
                print("Invalid input - press 'l' to quit")
                continue
            if not self.take_turn(action):
                print("Can't move")
                continue
            os.system('cls')
            self.moves += 1
            self.new_piece()
            self.display_board()
        print('FINAL SCORE: ', self.score)
        return not self.can_move

    def new_piece(self):
        piece = 4 if self.can_four and random.random() < 0.1 else 2
        pos = random.randrange(self.size**2 - self.fill)
        for i in range(self.size):
            for j in range(self.size):
                if not self.board[i][j]:
                    if pos == 0:
                        self.board[i][j] = piece
                    pos -= 1
        self.fill += 1

        if not self._is_move_possible():
            self.can_move = False

    def take_turn(self, action):
        if not self.can_move:
            return True

        is_change = False
        for i in range(self.size):
            if action == 'U':
                row = [self.board[j][i] for j in range(self.size)]
                new_row = self._resolve_row(row)
                if row != new_row:
                    is_change = True
                    for j in range(self.size):
                        self.board[j][i] = new_row[j]
            elif action == 'R':
                row = [self.board[i][self.size-j-1] for j in range(self.size)]
                new_row = self._resolve_row(row)
                if row != new_row:
                    is_change = True
                    for j in range(self.size):
                        self.board[i][self.size-j-1] = new_row[j]
            elif action == 'D':
                row = [self.board[self.size-j-1][i] for j in range(self.size)]
                new_row = self._resolve_row(row)
                if row != new_row:
                    is_change = True
                    for j in range(self.size):
                        self.board[self.size-j-1][i] = new_row[j]
            elif action == 'L':
                row = [self.board[i][j] for j in range(self.size)]
                new_row = self._resolve_row(row)
                if row != new_row:
                    is_change = True
                    for j in range(self.size):
                        self.board[i][j] = new_row[j]
            else:
                raise ValueError('Invalid input direction')
        return is_change

    def display_board(self):
        print(('='*(8*self.size-3)))
        for row in self.board:
            print(' '.join([str(x)+' '*(4-len(str(x))) if x else '-   ' for x in row]))
        print(('='*(8*self.size-3)))

    def _resolve_row(self, row):
        new_row = [None]*self.size
        prev = None
        i = 0
        for x in row:
            if not x:
                continue
            if x == prev:
                new_row[i] = x*2
                prev = None
                self.score += new_row[i]*(int(math.log2(new_row[i]))-1)
                self.fill -= 1
                i += 1    
            elif x:
                if prev:
                    new_row[i] = prev
                    i += 1
                prev = x
        if prev:
            new_row[i] = prev
        return new_row

    def _is_move_possible(self):
        if self.fill != self.size**2:
            return True
        for i in range(self.size):
            for j in range(self.size):
                if i < self.size-1 and self.board[i][j] == self.board[i+1][j]:
                    return True
                if j < self.size-1 and self.board[i][j] == self.board[i][j+1]:
                    return True