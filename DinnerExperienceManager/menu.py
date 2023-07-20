from meal import Meal

class Menu:
    @staticmethod
    def get_menu():
        # Create a list of Meal objects representing the menu
        menu = [
            Meal("Spaghetti", 8.0),
            Meal("Pizza", 10.0),
            Meal("Sweet and Sour Chicken", 9.0),
            Meal("Spring Rolls", 6.0),
            Meal("Tiramisu", 5.0),
            Meal("Cheesecake", 5.5),
            Meal("Chef's Special Soup", 7.5),
            Meal("Chef's Special Pasta", 12.0)
        ]
        return menu
