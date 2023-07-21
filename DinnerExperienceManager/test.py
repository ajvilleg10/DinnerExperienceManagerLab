import pytest

from DinnerExperienceManager.normal_order import NormalOrder
from DinnerExperienceManager.special_meal import SpecialMeal
from dining_experience_manager import DiningExperienceManager
from meal import Meal
from menu import Menu


def test_get_order():
    # Simular entrada del usuario utilizando lista con valores ['1', '2', '2', '0']
    with pytest.raises(StopIteration):
        input_values = iter(['1', '2', '2', '0'])

        def mock_input(s):
            return next(input_values)

        # Asignar el mock de input() a builtins.input para simular la entrada del usuario
        import builtins
        builtins.input = mock_input

        manager = DiningExperienceManager()
        menu = Menu.get_menu()
        order = manager.get_order(menu)
        assert len(order.get_items()) == 2
        assert order.get_total_quantity() == 4

def test_validate_quantities_valid():
    manager = DiningExperienceManager()
    order = NormalOrder()
    order.add_item(Meal("Pizza", 10.0), 2)
    order.add_item(Meal("Sweet and Sour Chicken", 9.0), 3)
    assert manager.validate_quantities(order) == True

def test_validate_quantities_negative_values():
    manager = DiningExperienceManager()
    order = NormalOrder()
    order.add_item(Meal("Pizza", 10.0), -1)
    assert manager.validate_quantities(order) == False

def test_validate_quantities_zero_values():
    manager = DiningExperienceManager()
    order = NormalOrder()
    order.add_item(Meal("Sweet and Sour Chicken", 9.0), 0)
    assert manager.validate_quantities(order) == False

def test_validate_quantities_max_order_quantity():
    manager = DiningExperienceManager()
    order = NormalOrder()
    order.add_item(Meal("Pizza", 10.0), manager.MAX_ORDER_QUANTITY)
    assert manager.validate_quantities(order) == True

def test_validate_quantities_exceeded_max_order_quantity():
    manager = DiningExperienceManager()
    order = NormalOrder()
    order.add_item(Meal("Pizza", 10.0), manager.MAX_ORDER_QUANTITY + 1)
    assert manager.validate_quantities(order) == False

def test_apply_special_meal_surcharge():
    manager = DiningExperienceManager()
    order = NormalOrder()
    order.add_item(SpecialMeal("Chef's Special Soup", 7.5, 0.1), 1)
    order.add_item(SpecialMeal("Chef's Special Pasta", 12.0, 0.1), 2)
    assert manager.apply_special_meal_surcharge(0.0, order) == (1 * 7.5 + 2 * 12.0) * 1.05

def test_validate_meal_availability_valid():
    manager = DiningExperienceManager()
    order = NormalOrder()
    order.add_item(Meal("Pizza", 10.0), 1)
    order.add_item(Meal("Sweet and Sour Chicken", 9.0), 1)
    menu = Menu.get_menu()
    assert manager.validate_meal_availability(order, menu) == True

def test_validate_meal_availability_invalid():
    manager = DiningExperienceManager()
    order = NormalOrder()
    order.add_item(Meal("Pizza", 10.0), 1)
    order.add_item(Meal("Burger", 7.5), 1)  # Añadir una comida no disponible
    menu = Menu.get_menu()
    assert manager.validate_meal_availability(order, menu) == False

def test_handle_errors(capsys):
    manager = DiningExperienceManager()
    manager.handle_errors()
    captured = capsys.readouterr()
    assert "An error occurred. Please check your inputs and try again." in captured.out

def test_process_order_invalid_input():
    with pytest.raises(StopIteration):
        input_values = iter(['invalid', '1', '0'])

        def mock_input(s):
            return next(input_values)

        import builtins
        builtins.input = mock_input

        manager = DiningExperienceManager()
        assert manager.process_order() == -1

def test_process_order_special_offer_discount():
    with pytest.raises(StopIteration):
        input_values = iter(['1', '5', '2', '0'])

        def mock_input(s):
            return next(input_values)

        import builtins
        builtins.input = mock_input

        manager = DiningExperienceManager()
        assert manager.process_order() == 5 * 2 * 0.9  # 10% discount

