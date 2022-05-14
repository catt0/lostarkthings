#!/usr/bin/env python3

# MIT License

# Copyright (c) 2022 catt0

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# tested with python 3.8

"""
This bot sends a message to Discord channels every time the
configured Lost Ark server changes state between up and down.
The down notification has a slight delay to correct for
AGS issues where the status page sometimes bugs out.
"""

import requests
import time
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


def bs_parse(html):
    return BeautifulSoup(html, 'lxml')


def getstuff(targeturi):
    try:
        response = requests.get(
            targeturi,
            headers={
                'User-Agent': fakeagent
            }
        )
        pagesrc = response.text
        return pagesrc
    except:
        return None


def get_server_status():
    status_dict = {}
    content = getstuff(target)
    if content is None:
        return status_dict
    divs = bs_parse(content).find_all('div', attrs={
        'class': 'ags-ServerStatus-content-responses-response-server'})
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
    hook_list = []
    try:
        hook_list.append(webhook_url)
    except:
        pass
    try:
        hook_list.extend(webhook_urls)
    except:
        pass
    for url in hook_list:
        try:
            req = requests.post(
                url,
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


if __name__ == "__main__":
    checkerloop()
