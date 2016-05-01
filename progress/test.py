# -*- coding: utf-8 -*-

import sys, time
 
for i in range(5):
    sys.stdout.write(' ' * 10 + '\r')
    sys.stdout.flush()
    print(i)
    sys.stdout.write(str(i) * (5 - i) + '\r')
    sys.stdout.flush()
    time.sleep(1)