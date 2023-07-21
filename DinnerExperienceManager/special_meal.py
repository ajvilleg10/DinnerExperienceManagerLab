from meal import Meal


class SpecialMeal(Meal):
    def __init__(self, name, price, surcharge):
        super().__init__(name, price)
        self.surcharge = surcharge

    def get_surcharge(self):
        return self.surcharge
