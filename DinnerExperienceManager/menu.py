from DinnerExperienceManager.special_meal import SpecialMeal
from meal import Meal


class Menu:
    @staticmethod
    def get_menu():
        return [
            Meal("Pizza", 10.0),
            Meal("Sweet and Sour Chicken", 9.0),
            Meal("Pasta", 12.0),
            Meal("Burger", 7.5),
            Meal("Salad", 6.0),
            Meal("Soup", 5.5),
            SpecialMeal("Chef's Special Soup", 7.5, 0.1),
            SpecialMeal("Chef's Special Pasta", 12.0, 0.1),
        ]
