#!/usr/bin/env python3
import json
from random import randrange, choice

from inventory import add_bottle, use_shot, stock_take
from recipes import RECIPES, serve_drink

def formatted_stock_take():
    response = ""
    for item_name, values in stock_take().items():
        percentage = values['percentage']
        response += '%s: %s %% \n' % (item_name, percentage)
        while percentage > 99:
            # print full bottles
            response += '|%-20s|  ' % ('='*20)
            percentage -= 100
        if percentage:
            # print the remaining bottle
            response += '|%-20s|' % ('=' * int(percentage / 5))
        response += '\n'
    return response



# setup bottles
spirits = [
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

mixers = [
    'soda',
    'sugar syrup',
    'lemon juice',
]

for spirit_name in spirits:
    add_bottle(spirit_name, quantity=randrange(1, 4))

for mixer_name in mixers:
    add_bottle(mixer_name, quantity=randrange(5, 8), each_size=375)

print(formatted_stock_take())

orders = []
while len(orders) < 8:
    drink = choice(list(RECIPES.keys()))
    ordered = randrange(1,6)
    served = serve_drink(drink, ordered)
    orders.append({'drink': drink, 'ordered': ordered, 'served': served})

for x in orders:
    print(x)

print(formatted_stock_take())
