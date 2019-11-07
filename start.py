#!/usr/bin/env python3
from random import randrange, choice

from functional.inventory import add_bottle, stock_take, StockLevelError, use_shot
# from classy.inventory import add_bottle, stock_take, StockLevelError, use_shot
from recipes import RECIPES


CRED = '\033[91m'
CEND = '\033[0m'

# setup bottles
SPIRITS = [
    'gin',
    'rum',
    # 'scotch',
    # 'bourbon',
    # 'cognac',
    # 'tequila',
    # 'vodka',
    # 'cointreau',
    # 'campari',
    'vermouth',
    # 'absinthe',
    # 'maraschino',
    # 'sherry'
]

MIXERS = [
    'soda',
    'sugar syrup',
    'lemon juice',
]


def formatted_stock_take():
    """ display the stock """
    response = ""
    for item_name, values in stock_take().items():
        percentage = values['percentage']
        response += '%s: %.1f%% \n' % (item_name, percentage)
        while percentage > 99:
            # print full bottles
            response += '|%-20s|  ' % ('=' * 20)
            percentage -= 100
        if percentage:
            # print the remaining bottle
            response += '|%-20s|' % ('=' * int(percentage / 5))
        response += '\n'
    return response


def serve_drink(title, quantity):
    """ take an order of drinks """
    served = 0
    drink = RECIPES.get(title, {})
    while served < quantity:
        try:
            for ingredient, amount in drink.items():
                use_shot(ingredient, amount)
            served += 1
        except StockLevelError as e:
            print('warning', CRED, e, ingredient, 'for', title, CEND)
            break
    return served


# setup the bar


for spirit_name in SPIRITS:
    add_bottle(spirit_name, quantity=randrange(1, 4))

for mixer_name in MIXERS:
    add_bottle(mixer_name, quantity=randrange(5, 6), each_size=375)

# show the bar is full of stock

print(formatted_stock_take())
input()

# take some orders


orders = []

while len(orders) < 12:
    drink_choice = choice(list(RECIPES.keys()))
    drinks_ordered = randrange(1, 9)
    drinks_served = serve_drink(drink_choice, drinks_ordered)
    orders.append({
        'drink': drink_choice,
        'ordered': drinks_ordered,
        'served': drinks_served,
    })


for x in orders:
    print("ordered %s %s, served:" % (x['ordered'], x['drink']), end=' ')
    if x['ordered'] != x['served']:
        print(CRED + str(x['served']) + CEND)
    else:
        print(x['served'])
# print the stock take

input()

print(formatted_stock_take())
