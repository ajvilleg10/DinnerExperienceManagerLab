from abc import ABC, abstractmethod

class SpecialMeal(ABC):
    @abstractmethod
    def get_surcharge(self):
        pass

class ChineseFood(SpecialMeal):
    SURCHARGE = 0.05

    def get_surcharge(self):
        return self.SURCHARGE

class ItalianFood(SpecialMeal):
    SURCHARGE = 0.05

    def get_surcharge(self):
        return self.SURCHARGE

class Pastries(SpecialMeal):
    SURCHARGE = 0.05

    def get_surcharge(self):
        return self.SURCHARGE

class ChefsSpecials(SpecialMeal):
    SURCHARGE = 0.1

    def get_surcharge(self):
        return self.SURCHARGE
