from order import Order


class Discount5OrMoreOrder(Order):
    def calculate_total_cost(self):
        total_cost = 0
        for meal, quantity in self.items.items():
            total_cost += meal.get_price() * quantity
        if self.get_total_quantity() >= 5:
            total_cost *= 0.9  # 10% discount
        return total_cost
