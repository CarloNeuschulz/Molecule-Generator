#OOP Exercise 1: Create a Class with instance attributes:
class Vehicle:
    def __init__(self, max_speed, mileage):
        self.max_speed = max_speed
        self.mileage = mileage

Vehicle1=Vehicle(240, 1700)
print(Vehicle1.max_speed, Vehicle1.mileage)