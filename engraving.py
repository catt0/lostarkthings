#!/usr/bin/env python3

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
