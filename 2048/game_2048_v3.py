# -*- coding: utf-8 -*-

import random

class Game2048(object):

    def __init__(self):

        # score 
        self.score = 0

        # initial of martrix
        self.init_martrix()

        # get random 2 position
        self.random_position()
        self.random_position()

        # get sys actions dictionary
        self.actions_dictionary()

        # moving dictionary
        self.move_dict()

        # check movable dictionary
        self.check_movable()

    def init_martrix(self):
        # initial of martrix
        #   row = [0 for i in range(4)]
        #   martrix = [row for j in range(4)]
        self.martrix = [[0 for i in range(4)] for j in range(4)]

    def random_position(self):
        # random position
        #   random_pos = random.sample(range(16), 1)
        #   self.martrix[random_pos[0] // 4][random_pos[0] % 4] = 2
        new_element = 4 if random.randrange(100) > 89 else 2
        (i,j) = random.choice([(i,j) for i in range(4) for j in range(4) if self.martrix[i][j] == 0])
        self.martrix[i][j] = new_element

    def actions_dictionary(self):
        # system actions dictionary
        actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']
        letter_codes = [ch for ch in 'WASDRQwasdrq']
        self.actions_dict = dict(zip(letter_codes, actions * 2))
        # print(self.actions_dict)        

    def get_actions(self):
        help_str = '(W)Up (S)Down (A)Left (D)Right\r\n     (R)Restart (Q)Exit\r\n'
        direct = input(help_str)
        while direct not in self.actions_dict:
            direct = input('Illegal key, you can only press W/S/A/D/R/Q:\r\n')
        # print(direct)
        return direct

    def tighten(self, row):
        # merge the non-zero element to one side
        new_row = [i for i in row if i != 0]
        new_row += [0 for j in range(len(row) - len(new_row))]
        return new_row

    def merge(self, row):
        # merge element
        is_pair = False
        new_row = []
        for i in range(len(row)):
            if is_pair:
                new_row.append(2 * row[i])
                self.score += 2 * row[i]
                is_pair = False
            else:
                if i + 1 < len(row) and row[i] == row[i + 1]:
                    is_pair = True
                    new_row.append(0)
                else:
                    new_row.append(row[i])
        return new_row


    def transpose(self, field):
        # matrix transpose
        #   a b      a c
        #         -> 
        #   c d      b d
        return [list(row) for row in zip(*field)]

    def invert(self, field):
        return [row[::-1] for row in field]

    def move_left(self, row):
        # move to left
        return self.tighten(self.merge(self.tighten(row)))

    def move_dict(self):
        # moving function dictionary
        self.moves = {}
        self.moves['Left'] = lambda field: [self.move_left(row) for row in field]
        self.moves['Right'] = lambda field: self.invert(self.moves['Left'](self.invert(field)))
        self.moves['Up'] = lambda field: self.transpose(self.moves['Left'](self.transpose(field)))
        self.moves['Down'] = lambda field: self.transpose(self.moves['Right'](self.transpose(field)))

    def move(self, direction):
        if direction in self.moves:
            if self.checking(direction):
                self.martrix = self.moves[direction](self.martrix)
                self.random_position()
                return True
            else:
                return False

    def row_can_movable(self, row, i):
        if row[i] == 0 and row[i + 1] != 0:
            # the element can move
            return True
        if row[i] != 0 and row[i] == row[i + 1]:
            # the element can merge
            return True
        return False

    def left_row_movable(self, row):
        # traversing martrix whether can move
        return any(self.row_can_movable(row, i) for i in range(len(row) - 1))

    def check_movable(self):
        # check movable dictionary
        self.check = {}
        self.check['Left'] = lambda field: any(self.left_row_movable(row) for row in field)
        self.check['Right'] = lambda field: self.check['Left'](self.invert(field))
        self.check['Up'] = lambda field: self.check['Left'](self.transpose(field))
        self.check['Down'] = lambda field: self.check['Right'](self.transpose(field))

    def checking(self, direction):
        if direction in self.check:
            return self.check[direction](self.martrix)
        else:
            return False

    def restart(self):
        self.score = 0
        self.init_martrix()
        self.random_position()
        self.random_position()
        self.display()

    def drop_zero(self, num):
        return num if num else ''

    def display(self):
        print('--------------')
        print('score: %s' %self.score)
        print('┌' + ('─'*5 + '┬')*3 + '─'*5 + '┐')
        print('│%4s │%4s │%4s │%4s │' %(self.drop_zero(self.martrix[0][0]), self.drop_zero(self.martrix[0][1]), self.drop_zero(self.martrix[0][2]), self.drop_zero(self.martrix[0][3])))
        print('├' + ('─'*5 + '┼')*3 + '─'*5 + '┤')
        print('│%4s │%4s │%4s │%4s │' %(self.drop_zero(self.martrix[1][0]), self.drop_zero(self.martrix[1][1]), self.drop_zero(self.martrix[1][2]), self.drop_zero(self.martrix[1][3])))
        print('├' + ('─'*5 + '┼')*3 + '─'*5 + '┤')
        print('│%4s │%4s │%4s │%4s │' %(self.drop_zero(self.martrix[2][0]), self.drop_zero(self.martrix[2][1]), self.drop_zero(self.martrix[2][2]), self.drop_zero(self.martrix[2][3])))
        print('├' + ('─'*5 + '┼')*3 + '─'*5 + '┤')
        print('│%4s │%4s │%4s │%4s │' %(self.drop_zero(self.martrix[3][0]), self.drop_zero(self.martrix[3][1]), self.drop_zero(self.martrix[3][2]), self.drop_zero(self.martrix[3][3])))
        print('└' + ('─'*5 + '┴')*3 + '─'*5 + '┘')

    def start(self):
        state = 'Init'
        self.display()
        while state != 'Exit':
            direction = self.get_actions()
            if self.actions_dict[direction] == 'Exit':
                state = 'Exit'
            if self.actions_dict[direction] == 'Restart':
                state = 'Restart'
                self.restart()
                continue

            self.move(self.actions_dict[direction])
            self.display()

def main():
    g = Game2048()
    g.start()
    
if __name__ == '__main__':
    main()