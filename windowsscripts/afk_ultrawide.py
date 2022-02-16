import pyautogui as pg
import time
import random

BUTTONS = ['q', 'w', 'e', 'r', 'a', 's', 'd', 'f']

while(True):
    x = random.randrange(1500, 3000)
    y = random.randrange(1200, 1800)
    pg.moveTo(x, y)
    pg.click(button='right')
    x = random.randrange(0, len(BUTTONS))
    pg.typewrite(BUTTONS[int(x)])
    x = random.randrange(180, 360)
    time.sleep(x)
