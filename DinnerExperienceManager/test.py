
import pytest
from io import StringIO
import sys
from main import main
from meal import Meal
from order import NormalOrder, Discount5OrMoreOrder, Discount10OrMoreOrder
from menu import Menu
from special_meal import ChineseFood, ItalianFood, Pastries, ChefsSpecials
from dining_experience_manager import DiningExperienceManager, ErrorHandler

def test_main(monkeypatch):
    # Simulate user input for order selection
    monkeypatch.setattr('sys.stdin', StringIO('1\n2\n2\n2\n2\n2\n2\n2\n2\n2\n2\n2\n'))

    main()

    # Redirect output to check the confirmation message
    output = sys.stdout.getvalue()
    assert "Order confirmed. Total Cost: $136.00" in output

def test_main_cancel_order(monkeypatch):
    # Simulate user input for order selection
    monkeypatch.setattr('sys.stdin', StringIO('1\n0\n'))

    main()

    # Redirect output to check the cancel message
    output = sys.stdout.getvalue()
    assert "Order canceled." in output

def test_meal_getters():
    meal = Meal("Pizza", 10.0)
    assert meal.get_name() == "Pizza"
    assert meal.get_price() == 10.0

def test_normal_order_total_cost():
    order = NormalOrder()
    order.add_item(Meal("Pizza", 10.0), 2)
    order.add_item(Meal("Sweet and Sour Chicken", 9.0), 3)
    assert order.calculate_total_cost() == 2 * 10.0 + 3 * 9.0

def test_discount_5_or_more_order_total_cost():
    order = Discount5OrMoreOrder()
    order.add_item(Meal("Pastries", 6.0), 6)
    order.add_item(Meal("Spring Rolls", 6.0), 4)
    assert order.calculate_total_cost() == (6 * 6.0 + 4 * 6.0) * 0.9  # 10% discount

def test_discount_10_or_more_order_total_cost():
    order = Discount10OrMoreOrder()
    order.add_item(Meal("Pizza", 10.0), 12)
    order.add_item(Meal("Sweet and Sour Chicken", 9.0), 9)
    assert order.calculate_total_cost() == (12 * 10.0 + 9 * 9.0) * 0.8  # 20% discount

def test_discount_5_or_more_order_no_discount():
    order = Discount5OrMoreOrder()
    order.add_item(Meal("Pastries", 6.0), 4)
    order.add_item(Meal("Spring Rolls", 6.0), 2)
    assert order.calculate_total_cost() == 4 * 6.0 + 2 * 6.0

def test_discount_10_or_more_order_no_discount():
    order = Discount10OrMoreOrder()
    order.add_item(Meal("Pizza", 10.0), 8)
    order.add_item(Meal("Sweet and Sour Chicken", 9.0), 4)
    assert order.calculate_total_cost() == 8 * 10.0 + 4 * 9.0

def test_get_menu():
    menu = Menu.get_menu()
    assert len(menu) == 8

def test_chinese_food_surcharge():
    chinese_food = ChineseFood()
    assert chinese_food.get_surcharge() == 0.05

def test_italian_food_surcharge():
    italian_food = ItalianFood()
    assert italian_food.get_surcharge() == 0.05

def test_pastries_surcharge():
    pastries = Pastries()
    assert pastries.get_surcharge() == 0.05

def test_chefs_specials_surcharge():
    chefs_specials = ChefsSpecials()
    assert chefs_specials.get_surcharge() == 0.1

def test_get_order(monkeypatch):
    monkeypatch.setattr('sys.stdin', StringIO('1\n2\n2\n0\n'))
    manager = DiningExperienceManager()
    menu = manager.get_menu()
    order = manager.get_order(menu)
    assert len(order.get_items()) == 2
    assert order.get_total_quantity() == 4

def test_validate_quantities_valid():
    manager = DiningExperienceManager()
    order = NormalOrder()
    order.add_item(Meal("Pizza", 10.0), 2)
    order.add_item(Meal("Sweet and Sour Chicken", 9.0), 3)
    assert manager.validate_quantities(order) == True

def test_validate_quantities_zero_quantity():
    manager = DiningExperienceManager()
    order = NormalOrder()
    order.add_item(Meal("Pizza", 10.0), 2)
    order.add_item(Meal("Sweet and Sour Chicken", 9.0), 0)
    assert manager.validate_quantities(order) == False

def test_validate_quantities_negative_quantity():
    manager = DiningExperienceManager()
    order = NormalOrder()
    order.add_item(Meal("Pizza", 10.0), 2)
    order.add_item(Meal("Sweet and Sour Chicken", 9.0), -1)
    assert manager.validate_quantities(order) == False

def test_validate_quantities_max_order_quantity():
    manager = DiningExperienceManager()
    order = NormalOrder()
    order.add_item(Meal("Pizza", 10.0), manager.MAX_ORDER_QUANTITY)
    assert manager.validate_quantities(order) == True

def test_validate_quantities_exceed_max_order_quantity():
    manager = DiningExperienceManager()
    order = NormalOrder()
    order.add_item(Meal("Pizza", 10.0), manager.MAX_ORDER_QUANTITY + 1)
    assert manager.validate_quantities(order) == False

def test_process_order_with_discount():
    # Simulate user input for order selection
    order_input = '1\n2\n2\n2\n2\n2\n2\n2\n2\n2\n2\n2\n'
    with pytest.raises(SystemExit) as exit_info:
        with pytest.raises(ValueError) as value_error_info:
            with StringIO(order_input) as order_input_str:
                sys.stdin = order_input_str
                manager = DiningExperienceManager()
                manager.process_order()
    assert exit_info.type == SystemExit
    assert value_error_info.type == ValueError
    assert str(value_error_info.value) == "ValueError('I/O operation on closed file.')"

def test_process_order_cancel_order():
    # Simulate user input for order selection
    order_input = '1\n0\n'
    with StringIO(order_input) as order_input_str:
        sys.stdin = order_input_str
        manager = DiningExperienceManager()
        manager.process_order()

        # Redirect output to check the cancel message
        output = sys.stdout.getvalue()
        assert "Order canceled." in output

def test_process_order_with_unavailable_meal(monkeypatch):
    monkeypatch.setattr('sys.stdin', StringIO('1\n2\n10\n'))
    manager = DiningExperienceManager()
    manager.process_order()

    # Redirect output to check the error message
    output = sys.stdout.getvalue()
    assert "Chef's Special Soup is not available on the menu." in output

def test_process_order_with_invalid_quantities(monkeypatch):
    monkeypatch.setattr('sys.stdin', StringIO('1\n0\n-1\n'))
    manager = DiningExperienceManager()
    manager.process_order()

    # Redirect output to check the error message
    output = sys.stdout.getvalue()
    assert "Quantity must be a positive integer greater than zero." in output

def test_process_order_with_exceeded_max_quantity(monkeypatch):
    monkeypatch.setattr('sys.stdin', StringIO('1\n101\n'))
    manager = DiningExperienceManager()
    manager.process_order()

    # Redirect output to check the error message
    output = sys.stdout.getvalue()
    assert "Maximum order quantity for a meal is 100." in output

def test_apply_special_offer_discount():
    assert DiningExperienceManager.apply_special_offer_discount(120.0) == 120.0 - 25.0
    assert DiningExperienceManager.apply_special_offer_discount(70.0) == 70.0 - 10.0
    assert DiningExperienceManager.apply_special_offer_discount(40.0) == 40.0

def test_apply_special_meal_surcharge():
    order = NormalOrder()
    order.add_item(Meal("Chef's Special Soup", 7.5), 1)
    order.add_item(Meal("Chef's Special Pasta", 12.0), 2)
    assert DiningExperienceManager.apply_special_meal_surcharge(0.0, order) == (1 * 7.5 + 2 * 12.0) * 1.05

def test_validate_meal_availability_valid():
    manager = DiningExperienceManager()
    order = NormalOrder()
    order.add_item(Meal("Pizza", 10.0), 1)
    order.add_item(Meal("Sweet and Sour Chicken", 9.0), 1)
    menu = manager.get_menu()
    assert manager.validate_meal_availability(order, menu) == True

def test_validate_meal_availability_unavailable_meal():
    manager = DiningExperienceManager()
    order = NormalOrder()
    order.add_item(Meal("Spaghetti", 8.0), 1)
    order.add_item(Meal("Salad", 6.0), 1)
    menu = manager.get_menu()
    assert manager.validate_meal_availability(order, menu) == False

def test_validate_meal_availability_special_meal():
    manager = DiningExperienceManager()
    order = NormalOrder()
    order.add_item(Meal("Chef's Special Soup", 7.5), 1)
    order.add_item(Meal("Chef's Special Pasta", 12.0), 1)
    menu = manager.get_menu()
    assert manager.validate_meal_availability(order, menu) == True

def test_handle_errors(capsys):
    manager = DiningExperienceManager()
    manager.handle_errors()
    captured = capsys.readouterr()
    assert "An error occurred. Please check your inputs and try again." in captured.out
