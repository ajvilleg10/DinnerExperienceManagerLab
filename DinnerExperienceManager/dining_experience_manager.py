from order import NormalOrder, Discount5OrMoreOrder, Discount10OrMoreOrder
from menu import Menu
from special_meal import SpecialMeal
from error_handler import ErrorHandler

class DiningExperienceManager:
    SPECIAL_OFFER_DISCOUNT_50 = 10.0
    SPECIAL_OFFER_DISCOUNT_100 = 25.0

    def __init__(self):
        self.MAX_ORDER_QUANTITY = 100

    def display_menu(self, menu):
        print("Menu Options:")
        for i, meal in enumerate(menu, 1):
            print(f"{i}. {meal.get_name()} - ${meal.get_price()}")

    def get_order(self, menu):
        order = NormalOrder()  # Default order without any discounts

        self.display_menu(menu)

        print("Enter the quantity for each meal (0 to skip):")
        for i, meal in enumerate(menu, 1):
            quantity = int(input(f"{meal.get_name()}: "))
            if quantity > 0:
                order.add_item(meal, quantity)

        total_quantity = order.get_total_quantity()
        if total_quantity >= 10:
            order = Discount10OrMoreOrder()
        elif total_quantity >= 5:
            order = Discount5OrMoreOrder()

        return order

    @staticmethod
    def apply_special_offer_discount(total_cost):
        if total_cost > 100:
            total_cost -= DiningExperienceManager.SPECIAL_OFFER_DISCOUNT_100
        elif total_cost > 50:
            total_cost -= DiningExperienceManager.SPECIAL_OFFER_DISCOUNT_50
        return total_cost

    @staticmethod
    def apply_special_meal_surcharge(total_cost, order):
        for meal, quantity in order.get_items().items():
            if isinstance(meal, SpecialMeal):
                total_cost += meal.get_surcharge() * meal.get_price() * quantity
        return total_cost

    def validate_meal_availability(self, order, menu):
        for meal in order.get_items():
            if meal not in menu:
                ErrorHandler.handle_error(f"{meal.get_name()} is not available on the menu.")
                return False
        return True

    def validate_quantities(self, order):
        for quantity in order.get_items().values():
            if quantity <= 0:
                ErrorHandler.handle_error("Quantity must be a positive integer greater than zero.")
                return False
            if quantity > self.MAX_ORDER_QUANTITY:
                ErrorHandler.handle_error(f"Maximum order quantity for a meal is {self.MAX_ORDER_QUANTITY}.")
                return False
        return True

    def confirm_order(self, order, total_cost):
        print("Order Summary:")
        for meal, quantity in order.get_items().items():
            print(f"{meal.get_name()} x {quantity} - ${meal.get_price() * quantity:.2f}")
        print(f"Total Cost: ${total_cost:.2f}")

        choice = input("Do you want to confirm the order? (Y/N): ")
        return choice.upper() == "Y"

    def handle_errors(self):
        ErrorHandler.handle_error("An error occurred. Please check your inputs and try again.")

    def process_order(self):
        menu = Menu.get_menu()
        order = self.get_order(menu)

        if not self.validate_quantities(order):
            self.handle_errors()
            return

        total_cost = order.calculate_total_cost()
        total_cost = self.apply_special_offer_discount(total_cost)
        total_cost = self.apply_special_meal_surcharge(total_cost, order)

        if not self.validate_meal_availability(order, menu):
            self.handle_errors()
            return

        if total_cost == 0:
            print("Order canceled.")
            return

        if self.confirm_order(order, total_cost):
            print(f"Order confirmed. Total Cost: ${total_cost:.2f}")
        else:
            print("Order canceled.")
