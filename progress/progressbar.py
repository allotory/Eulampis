# -*- coding: utf-8 -*-

import sys, time
from datetime import datetime
# j = '#'
# if __name__ == '__main__':
#     for i in range(1,61):
#         j += '#'
#         sys.stdout.write(str(int((i/60)*100))+'% ||'+j+'->'+"\r")
#         sys.stdout.flush()
#         time.sleep(0.1)
# print()

class Progressbar(object):

    def __init__(self, finallcount, block_char='#', block_length=50):
        self.finallcount = finallcount
        self.block_char = block_char
        self.block_length = block_length
        self.block = ''

        self.f = sys.stdout
        self.start = datetime.now()
    def percentage(self, index):
        return str(round((index / self.finallcount) * 100, 2))

    def blockunit(self):
        return int(self.finallcount / self.block_length)

    def runtime(self):
        now = datetime.now()
        return str(now - self.start)

    def progress(self):

        j = 0
        unit = self.blockunit()

        for i in range(1, self.finallcount + 1):
            j += 1

            if j == unit:
                self.block += self.block_char
                j = 0
            
            self.f.write(self.percentage(i) + '% ||' + self.block + '=> ' + 'time '+ self.runtime() + '\r')
            self.f.flush()
            time.sleep(0.1)

def main():
    p = Progressbar(1000)
    p.progress()

if __name__ == '__main__':
    main()