#OOP Exercise 3: Create a child class Bus that will inherit all of the variables and methods of the Vehicle class

#given vheicle class
class Vehicle:

    def __init__(self, name, max_speed, mileage):
        self.name = name
        self.max_speed = max_speed
        self.mileage = mileage
    #bus class with the same varible and methods
    class Bus:
        pass
Bus=Vehicle('School Volvo', 180, 12)

print(f"Vehicle Name: {Bus.name}, Speed: {Bus.max_speed}, Mileage: {Bus.mileage},")