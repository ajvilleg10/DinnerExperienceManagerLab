from order import Order


class Discount10OrMoreOrder(Order):
    def calculate_total_cost(self):
        total_cost = 0
        for meal, quantity in self.items.items():
            total_cost += meal.get_price() * quantity
        if self.get_total_quantity() >= 10:
            total_cost *= 0.8  # 20% discount
        return total_cost

    def get_total_quantity(self):
        return sum(self.items.values())
