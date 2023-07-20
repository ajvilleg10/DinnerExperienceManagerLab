from abc import ABC, abstractmethod

class Order(ABC):
    def __init__(self):
        self.items = {}

    def add_item(self, meal, quantity):
        self.items[meal] = quantity

    def get_items(self):
        return self.items

    @abstractmethod
    def calculate_total_cost(self):
        pass

    def get_total_quantity(self):
        return sum(self.items.values())

class NormalOrder(Order):
    def calculate_total_cost(self):
        total_cost = 0.0
        for meal, quantity in self.items.items():
            total_cost += meal.get_price() * quantity
        return total_cost

class Discount5OrMoreOrder(Order):
    def calculate_total_cost(self):
        total_cost = 0.0
        for meal, quantity in self.items.items():
            total_cost += meal.get_price() * quantity

        total_quantity = self.get_total_quantity()
        if total_quantity >= 5:
            total_cost *= (1 - 0.1)  # 10% discount
        return total_cost

class Discount10OrMoreOrder(Order):
    def calculate_total_cost(self):
        total_cost = 0.0
        for meal, quantity in self.items.items():
            total_cost += meal.get_price() * quantity

        total_quantity = self.get_total_quantity()
        if total_quantity >= 10:
            total_cost *= (1 - 0.2)  # 20% discount
        return total_cost
