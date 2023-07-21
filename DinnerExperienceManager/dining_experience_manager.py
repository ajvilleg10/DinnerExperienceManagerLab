from DinnerExperienceManager.normal_order import NormalOrder
from DinnerExperienceManager.special_meal import SpecialMeal
from menu import Menu
from order import Order


class DiningExperienceManager:
    MAX_ORDER_QUANTITY = 100

    def get_menu(self):
        return Menu.get_menu()

    def display_menu(self, menu):
        print("Menu:")
        for item in menu:
            print(f"{item.get_name()} - ${item.get_price()}")

    def get_order(self, menu):
        order = NormalOrder()
        print("Please select the meals you want to order and enter the quantity (0 to finish):")
        while True:
            for i, meal in enumerate(menu, 1):
                print(f"{i}. {meal.get_name()} (${meal.get_price()})")

            try:
                choice = int(input("Enter the meal number: "))
                if choice == 0:
                    break
                elif 1 <= choice <= len(menu):
                    meal = menu[choice - 1]
                    quantity = int(input("Enter the quantity: "))
                    if quantity > 0:
                        order.add_item(meal, quantity)
                    else:
                        print("Invalid quantity. Please enter a positive integer.")
                else:
                    print("Invalid choice. Please enter a valid meal number.")
            except ValueError:
                print("Invalid input. Please enter a valid meal number.")

        return order

    def validate_quantities(self, order):
        for item, quantity in order.get_items().items():
            if quantity <= 0:
                return False
            if quantity > self.MAX_ORDER_QUANTITY:
                return False
        return True

    def apply_special_meal_surcharge(self, total_cost, order):
        for item, quantity in order.get_items().items():
            if isinstance(item, SpecialMeal):
                total_cost += item.get_price() * quantity * item.get_surcharge()
        return total_cost

    def validate_meal_availability(self, order, menu):
        for item, quantity in order.get_items().items():
            if item not in menu:
                return False
        return True

    def handle_errors(self):
        print("An error occurred. Please check your inputs and try again.")

    def process_order(self):
        menu = self.get_menu()
        order = self.get_order(menu)
        if not self.validate_quantities(order):
            return -1
        total_cost = order.calculate_total_cost()
        total_cost = self.apply_special_meal_surcharge(total_cost, order)
        print(f"Total cost: ${total_cost:.2f}")
        return total_cost
