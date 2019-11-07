from inventory import SHOTS, StockLevelError, use_item

RECIPES = {
    'tom collins': {
        'gin': 2 * SHOTS,
        'lemon juice': 1 * SHOTS,
        'sugar syrup': 10,
        'soda': 3 * SHOTS,
    },
    'martini': {
        'gin': 2 * SHOTS,
        'vermouth': 0.5 * SHOTS
    },
    'mojito': {
        'rum': 1.5 * SHOTS,
        'soda': 3 * SHOTS,
        # 'mint': 10,
        # 'lime': 0.5,
    },
}


def serve_drink(title, quantity):
    served = 0
    drink = RECIPES.get(title, {})
    while served < quantity:
        try:
            for ingredient, amount in drink.items():
                use_item(ingredient, amount)
            served += 1
        except StockLevelError as e:
            print(e, ingredient, 'for', title)
            break
    return served


