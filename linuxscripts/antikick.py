#!/usr/bin/env python3

"""
Test of an anti afk kick using xdotool, did not seem to work.
"""

import os
import time
import random

print('Sleeping for 5s until sequence start.')
time.sleep(5)

while True:
    print('Pressing key.')
    os.system('xdotool key space')
    delay = random.randrange(264, 297)
    print('Sleeping for {}s.'.format(delay))
    time.sleep(delay)
