# -*- coding: utf-8 -*-

import random

class Game2048(object):

    def __init__(self):

        # initial of martrix
        self.init_martrix()

        # get random position
        self.random_position()

        # get sys actions dictionary
        self.actions_dictionary()

        # moving dictionary
        self.move_dict()

    def init_martrix(self):
        # initial of martrix
        #   row = [0 for i in range(4)]
        #   martrix = [row for j in range(4)]
        self.martrix = [[0 for i in range(4)] for j in range(4)]

    def random_position(self):
        # random position
        random_pos = random.sample(range(16), 2)
        # print(random_pos)
        self.martrix[random_pos[0] // 4][random_pos[0] % 4] = 2
        self.martrix[random_pos[1] // 4][random_pos[1] % 4] = 2

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
        self.moves['Right'] = lambda field: self.invert([self.move_left(row) for row in field])
        self.moves['Up'] = lambda field: self.transpose([self.move_left(row) for row in self.transpose(field)])
        self.moves['Down'] = lambda field: self.transpose(self.invert([self.move_left(row) for row in self.transpose(field)]))

    def move(self, direction):
               
        self.martrix = self.moves[direction](self.martrix)
        # print(direction)
        # print(self.martrix)
        # print(moves['Left'](self.martrix))
        # print(moves['Right'](self.martrix))
        # print(moves['Up'](self.martrix))
        # print(moves['Down'](self.martrix))

    def drop_zero(self, num):
        return num if num else ''

    def display(self):
        print('score: 0')
        print('┌' + ('─'*5 + '┬')*3 + '─'*5 + '┐')
        print('│%4s │%4s │%4s │%4s │' %(self.martrix[0][0], self.martrix[0][1], self.martrix[0][2], self.martrix[0][3]))
        print('├' + ('─'*5 + '┼')*3 + '─'*5 + '┤')
        print('│%4s │%4s │%4s │%4s │' %(self.martrix[1][0], self.martrix[1][1], self.martrix[1][2], self.martrix[1][3]))
        print('├' + ('─'*5 + '┼')*3 + '─'*5 + '┤')
        print('│%4s │%4s │%4s │%4s │' %(self.martrix[2][0], self.martrix[2][1], self.martrix[2][2], self.martrix[2][3]))
        print('├' + ('─'*5 + '┼')*3 + '─'*5 + '┤')
        print('│%4s │%4s │%4s │%4s │' %(self.martrix[3][0], self.martrix[3][1], self.martrix[3][2], self.martrix[3][3]))
        print('└' + ('─'*5 + '┴')*3 + '─'*5 + '┘')

    def start(self):
        self.display()
        direction = self.get_actions()
        self.move(self.actions_dict[direction])
        self.display()

def main():
    g = Game2048()
    g.start()

if __name__ == '__main__':
    main()