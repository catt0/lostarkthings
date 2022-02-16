# tested with python 3.8
# hackish dirty

# used libs
# pip install lxml
# pip install bs4
# if you want mp3 sound play:
# --   pip install playsound

# customize def checkerloop() to add own stuff
# def checkavailable(): gives back TRUE if NOT available, gives back FALSE if available
# it checks if this span exist, so if other stuff is out of stock it will trigger too

from urllib import request
import requests
import time
import random
from bs4 import BeautifulSoup
import os
from enum import Enum
import json

from config import *

class Status(Enum):
    Good = 1
    Busy = 2
    Full = 3
    Maintenance = 4

mapper_status_to_class = {
    Status.Good: 'ags-ServerStatus-content-responses-response-server-status--good',
    Status.Busy: 'ags-ServerStatus-content-responses-response-server-status--busy',
    Status.Full: 'ags-ServerStatus-content-responses-response-server-status--full',
    Status.Maintenance: 'ags-ServerStatus-content-responses-response-server-status--maintenance',
}

########

def bs_parse(html):
    return BeautifulSoup(html, 'lxml')


def add_random_time():
    return random.randint(1,5) + looptimer


def getstuff(targeturi):
    try:
        req = request.Request(
            targeturi,
            data=None,
            headers={
                'User-Agent': fakeagent
            }
        )
        response = request.urlopen(req)
        pagesrc = response.read().decode('utf-8')
        return pagesrc
    except:
        return None


def get_server_status():
    divs = bs_parse(getstuff(target)).find_all('div', attrs={
        'class': 'ags-ServerStatus-content-responses-response-server'})
    status_dict = {}
    for div in divs:
        name_div = div.find('div', attrs = {
            'class': 'ags-ServerStatus-content-responses-response-server-name'
        })
        status_div = div.find('div', attrs = {
            'class': 'ags-ServerStatus-content-responses-response-server-status'
        })
        name = name_div.text.strip()
        classes = status_div['class']
        status = None

        if mapper_status_to_class[Status.Maintenance] in classes:
            status = Status.Maintenance
        elif mapper_status_to_class[Status.Full] in classes:
            status = Status.Full
        elif mapper_status_to_class[Status.Busy] in classes:
            status = Status.Busy
        elif mapper_status_to_class[Status.Good] in classes:
            status = Status.Good
        else:
            print('Unknown status for {} with classes {}'.format(name, classes))
            continue

        is_up = False
        if status in [Status.Full, Status.Busy, Status.Good]:
            is_up = True
        status_dict[name] = is_up

        if name == target_server:
            print('Found server "{}" with status {}.'.format(name, status))
    return status_dict

def wait(long_sleep = False):
    if long_sleep:
        time.sleep(looptimer_long)
    else:
        time.sleep(looptimer)


def send_message(is_up):
    message = up_message
    if is_up == False:
        message = down_message
    try:
        req = requests.post(
            webhook_url,
            data=bytes(json.dumps({'content': message}), encoding='utf-8'),
            headers = {'Content-Type': 'application/json'}
        )
        print(req.text)
    except Exception as e:
        print(e)


def checkerloop():
    last_status = None
    status_confirms = 0
    while True:
        server_status = get_server_status()
        target_status = None
        if target_server in server_status:
            target_status = server_status[target_server]
        else:
            target_status = False
            print('Target {} is not in dict.'.format(target_server))
        # print('Target {} is up: {}.'.format(target_server, target_status))
        if last_status is None:
            last_status = target_status
            wait(target_status)
            continue
        if last_status != target_status:
            confirmed = False
            # status page might bug during updates, delay message until we are "sure"
            if target_status == False:
                status_confirms += 1
                if status_confirms >= confirmations_needed:
                    confirmed = True
            else:
                # up message is not delayed, get in before the queue!
                confirmed = True
            if confirmed:
                print('Target {} changed status from {} to {}.'.format(target_server, last_status, target_status))
                send_message(target_status)
                last_status = target_status
        else:
            status_confirms = 0

        wait(target_status)

checkerloop()
