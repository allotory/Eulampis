# -*- coding: utf-8 -*-

import sys, time
from datetime import datetime


class Progressbar(object):

    def __init__(self, finallcount, block_char='#', block_length=50):
        self.finallcount = finallcount
        self.block_char = block_char
        self.block_length = block_length
        self.block = ''

        self.f = sys.stdout
        self.start = datetime.now()

    def percentage(self, index):
        if index >= self.finallcount:
            index = self.finallcount
        return str(round((index / self.finallcount) * 100, 2))

    def blockunit(self, index):
        if index >= self.finallcount:
            index = self.finallcount
        return int((index * self.block_length) / self.finallcount)

    def runtime(self):
        now = datetime.now()
        return str(now - self.start)

    def progress(self, index):

        unit = self.blockunit(index)
        self.block = self.block_char * unit
        
        self.f.write(self.percentage(index) + '% ||' + self.block + '=> ' + 'Time: '+ self.runtime() + '\r')
        self.f.flush()

        if index >= self.finallcount:
            self.f.write('\n')

def main():
    p = Progressbar(1000)
    for i in range(1, 1001):
        p.progress(i)
        time.sleep(0.01)

    p = Progressbar(30, '*')
    p.progress(2)
    time.sleep(1)
    p.progress(9)
    time.sleep(1)
    p.progress(19)
    time.sleep(1)
    p.progress(30)

if __name__ == '__main__':
    main()