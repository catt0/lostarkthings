#!/usr/bin/env python3

"""
Presses G ever 6-8 seconds, useful for the egg mining.
Uses xdotool on Linux, start script, focus Lost Ark.
"""

import os
import time
import random

print('Sleeping for 5s until sequence start.')
time.sleep(5)

while True:
    print('Pressing key.')
    os.system('xdotool key g')
    delay = random.randrange(6, 8)
    print('Sleeping for {}s.'.format(delay))
    time.sleep(delay)
