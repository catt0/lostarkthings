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

"""
PoC for an engraving calculator.
For now you need to edit the data in this file directly.
Check the comments for what to change.
"""

# Disclaimer notes:
# the simple algo has its limits, it only does works 100% and impossible
# it also prefers +3 instead of going cheaper if possible, but you see the acc list, so you can tweak that on your own
# also it always grabs the books for the first 1 or 2 engravings even though it could be better to do it for the less prio ones, but I guess that is how it is usually done anyway


from enum import Enum, auto
from pprint import pprint


class Engraving(Enum):
    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name)

    # add new engravings below, names must not contain spaces
    Grudge = auto()
    CursedDoll = auto()
    KeenBlunt = auto()
    Firepower = auto()
    BlessedAura = auto()


# your target points
# order determines the priority
# it will first use books to fulfill these
target = [
    (Engraving.Grudge, 15),
    (Engraving.CursedDoll, 15),
    (Engraving.KeenBlunt, 15),
    (Engraving.Firepower, 15),
]


# the points you get from books
books = {
    Engraving.Grudge: 12,
    Engraving.Firepower: 12,
}


# the points you get from your stone
stone = {
    Engraving.KeenBlunt: 8,
    Engraving.Grudge: 5,
}


MAX_ACCS = 5


def find_acc_slots(accs, engraving, needed_levels):
    if needed_levels <= 0:
        return True
    added_levels = 0
    while True:
        if added_levels >= needed_levels:
            return True
        if len(accs) < MAX_ACCS:
            level_to_add = min(needed_levels - added_levels, 3)
            accs.append(((engraving, level_to_add), None))
            # print('Added acc with {}: {}'.format(engraving, level_to_add))
            needed_levels -= level_to_add
        else:
            for i in range(len(accs)):
                acc = accs[i]
                if acc[1] is None:
                    level_to_add = min(needed_levels - added_levels, 3)
                    accs[i] = (acc[0], (engraving, level_to_add))
                    needed_levels -= level_to_add
                    # print('Added acc with {}: {}'.format(engraving, level_to_add))
                if added_levels >= needed_levels:
                    return True
            return False


accs = []
books_equipped = []
success = True
for engraving, target_level in target:
    print("Trying to reach {} on {}".format(target_level, engraving))
    current_level = 0
    if engraving in stone:
        current_level += stone[engraving]
        # print('Used {} from stone'.format(engraving))
    if current_level >= target_level:
        print('{} reached target {}'.format(engraving, target_level))
        continue
    if engraving in books and len(books_equipped) < 2:
        current_level += books[engraving]
        books_equipped.append(engraving)
        # print('Used {} from book'.format(engraving))
    if current_level >= target_level:
        print('{} reached target {}'.format(engraving, target_level))
        continue
    # print('{} at {} after books and stone'.format(engraving, current_level))
    if not find_acc_slots(accs, engraving, target_level - current_level):
        print('Unable to reach target {} for {}'.format(target_level, engraving))
        success = False
        break
    print('{} reached target {}'.format(engraving, target_level))

if not success:
    print('Impossible')
else:
    print('Books:')
    pprint(books_equipped)
    print('Accessories:')
    pprint(accs)
