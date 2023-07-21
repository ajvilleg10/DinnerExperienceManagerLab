from order import Order


class NormalOrder(Order):
    def calculate_total_cost(self):
        total_cost = 0
        for meal, quantity in self.items.items():
            total_cost += meal.get_price() * quantity
        return total_cost
