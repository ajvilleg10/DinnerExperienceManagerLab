class Order:
    def __init__(self):
        self.items = {}

    def add_item(self, meal, quantity):
        if meal in self.items:
            self.items[meal] += quantity
        else:
            self.items[meal] = quantity

    def get_items(self):
        return self.items

    def get_total_quantity(self):
        return sum(self.items.values())
