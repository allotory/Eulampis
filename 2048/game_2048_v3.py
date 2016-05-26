# -*- coding: utf-8 -*-

import random

def initial():
    # initial of martrix
    # row = [0 for i in range(4)]
    # martrix = [row for j in range(4)]
    martrix = [[0 for i in range(4)] for j in range(4)]

    # random position
    random_pos = random.sample(range(16), 2)
    print(random_pos)
    pos_1 = martrix[random_pos[0]//4][random_pos[0]%4]
    pos_2 = martrix[random_pos[1]//4][random_pos[1]%4]
    pos_1 = pos_2 = 2

    actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']
    letter_codes = [ch for ch in 'WASDRQwasdrq']
    actions_dict = dict(zip(letter_codes, actions * 2))
    print(actions_dict)

def tighten(row):
    # merge the non-zero unit to one side
    new_row = [i for i in row if i != 0]
    new_row += [0 for j in range(len(row) - len(new_row))]
    return new_row

def merge(row):
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


def transpose(field):
    return [list(row) for row in zip(*field)]

def invert(field):
    return [row[::-1] for row in field]

def notZero(num):
    return num if num else ''

def display(martrix):
    print("┌" + ("─"*5 + "┬")*3 + "─"*5 + "┐")
    print("│%4s │%4s │%4s │%4s │" %(notZero(martrix[0][0]), 
        notZero(martrix[0][1]), notZero(martrix[0][2]), notZero(martrix[0][3])))
    print("├" + ("─"*5 + "┼")*3 + "─"*5 + "┤")
    print("│%4s │%4s │%4s │%4s │" %(notZero(martrix[1][0]), 
        notZero(martrix[1][1]), notZero(martrix[1][2]), notZero(martrix[1][3])))
    print("├" + ("─"*5 + "┼")*3 + "─"*5 + "┤")
    print("│%4s │%4s │%4s │%4s │" %(notZero(martrix[2][0]), 
        notZero(martrix[2][1]), notZero(martrix[2][2]), notZero(martrix[2][3])))
    print("├" + ("─"*5 + "┼")*3 + "─"*5 + "┤")
    print("│%4s │%4s │%4s │%4s │" %(notZero(martrix[3][0]), 
        notZero(martrix[3][1]), notZero(martrix[3][2]), notZero(martrix[3][3])))
    print("└" + ("─"*5 + "┴")*3 + "─"*5 + "┘")

def main():
    m = [[2, 4, 4, 0],[0,0,0,0],[2, 4, 4, 0],[0,0,0,0]]
    left = lambda field: [tighten(merge(tighten(row))) for row in field]
    right = lambda field: invert([tighten(merge(tighten(row))) for row in field])
    up = lambda field: transpose([tighten(merge(tighten(row))) for row in transpose(field)])
    down = lambda field: transpose(invert([tighten(merge(tighten(row))) for row in transpose(field)]))
    print(left(m))
    print(right(m))
    print(up(m))
    print(down(m))
    print(transpose(m))
    print(invert(m))

if __name__ == '__main__':
    main()