
INVENTORY = {
    'cognac': {
        'measurement': 'ml',
        'each_size': 700,
        'stock': 1400,
    }
}

ALLOWED_MEASUREMENTS = [
    'ml',
]

SHOTS = 30  # number of ml in a shot


class StockLevelError(Exception):
    pass


def add_item(item_name, quantity=1, measurement=None, each_size=None):
    """ add an item to the inventory """

    # validate the input
    if not isinstance(item_name, str):
        raise TypeError('item_name must be a string')
    if type(quantity) not in (int, float):
        raise TypeError('quantity must be a number')

    # need to get the original values from the inventory
    # to prevent functions from changing a value once set
    stock_item = INVENTORY.get(item_name, {})

    # check that measurement hasn't been changed
    if measurement and stock_item.get('measurement'):
        # if measurement was already set and is provided again
        if measurement != stock_item.get('measurement'):
            # if the measurement given is different to the existing one
            raise ValueError('can not redefine an existing measurement')

    # check the each size hasn't been adjusted
    if each_size and stock_item.get('each_size'):
        # if the each size was already set but provided again
        if each_size != stock_item.get('each_size'):
            # prevent the changing of an each size
            raise ValueError('can not redefine an existing each_size')

    # set the measurement if not already set
    if not measurement:
        measurement = stock_item.get('measurement')
    # set the each size if not already set
    if not each_size:
        each_size = stock_item.get('each_size')

    # validate measurement
    if measurement not in ALLOWED_MEASUREMENTS:
        raise ValueError(
            'measurement: %s not in allowed measurements:%s' % (
                measurement, ','.join(ALLOWED_MEASUREMENTS)
            )
        )

    # validate each_size
    if type(each_size) not in (int, float):
        raise TypeError('each_size must be an int or float.')

    # add item to total
    INVENTORY[item_name] = {
        'measurement': measurement,
        'each_size': each_size,
        'stock': stock_item.get('stock', 0) + (quantity * each_size),
    }
    return INVENTORY[item_name]


def add_bottle(item_name, quantity=1, each_size=700):
    """ short cut to add a bottle with bottle defaults """
    return add_item(item_name, quantity, 'ml', each_size)


def use_item(item_name, quantity):
    """ use an item from the inventory """

    # validate the input
    if type(quantity) not in (int, float):
        raise ValueError('quantity must be either int or float')
    if item_name not in INVENTORY.keys():
        raise ValueError('item_name:%s does not exist' % item_name)

    # validate there is enough stock
    if INVENTORY[item_name]['stock'] < quantity:
        raise StockLevelError('not enough stock')

    # reduce the amount
    INVENTORY[item_name]['stock'] = INVENTORY[item_name]['stock'] - quantity
    return INVENTORY[item_name]


def use_shot(item_name, quantity):
    """ take a shot of an item """
    return use_item(item_name, SHOTS * quantity)


def stock_take():
    stock = {}
    for item_name, item_props in INVENTORY.items():
        stock[item_name] = {}
        # number of full bottles
        stock[item_name]['full_stock'] = item_props['stock'] // item_props['each_size']
        # amount remaining in open bottles
        stock[item_name]['open_stock'] = item_props['stock'] % item_props['each_size']
        # percentage of bottles available
        stock[item_name]['percentage'] = item_props['stock'] / item_props['each_size'] * 100
    return stock

