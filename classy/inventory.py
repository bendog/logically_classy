SHOTS = 30  # number of ml in a shot

INVENTORY = {}


class StockLevelError(Exception):
    pass


class Bottle(object):
    measurement = 'ml'

    def __init__(self, quantity=0, each_size=700):
        # validate the input
        if type(quantity) not in (int, float):
            raise TypeError('quantity must be a number')
        if type(each_size) not in (int, float):
            raise TypeError('each_size must be an int or float.')
        # set the values
        self.stock = quantity * each_size
        self.each_size = each_size

    def add(self, quantity=1):
        """ add an item to the inventory """
        # validate the input
        if type(quantity) not in (int, float):
            raise TypeError('quantity must be a number')
        # add the item to stock
        self.stock += quantity * self.each_size

    def use(self, quantity):
        """ use some stock """
        # validate the input
        if type(quantity) not in (int, float):
            raise TypeError('quantity must be a number')
        # validate enough stock to use
        if quantity > self.stock:
            raise StockLevelError("not enough stock")
        # add the item to stock
        self.stock -= quantity

    def use_shot(self, quantity):
        self.use(quantity * SHOTS)

    # properties for stock takes

    @property
    def full_stock(self):
        """ the number of full bottles """
        return self.stock // self.each_size

    @property
    def open_stock(self):
        """ the amount in open bottles """
        return self.stock % self.each_size

    @property
    def percentage(self):
        """ the amount of stock as percentages of bottles """
        return self.stock / self.each_size * 100


def add_bottle(item_name, quantity=1, each_size=700):
    """ short cut to add a bottle with bottle defaults """
    if item_name in INVENTORY.keys():
        INVENTORY[item_name].add(quantity)
    else:
        INVENTORY[item_name] = Bottle(quantity)


def use_shot(item_name, quantity):
    """ take a shot from the item """
    if item_name not in INVENTORY.keys():
        raise ValueError('item_name:%s does not exist' % item_name)
    INVENTORY[item_name].use_shot(quantity)


def stock_take():
    """ return stock take items """
    stock = {}
    for item_name, instance in INVENTORY.items():
        stock[item_name] = {
            'full_stock': instance.full_stock,
            'open_stock': instance.open_stock,
            'percentage': instance.percentage,

        }
    return stock
