# Class for delivery trucks
class Truck:
    def __init__(self, number, speed, load, packages, miles, street, depart_time):
        self.number = number
        self.speed = speed
        self.load = load
        self.packages = packages
        self.miles = miles
        self.street = street
        self.depart_time = depart_time
        self.time = depart_time

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.number, self.speed, self.load, self.packages, self.miles, self.street, self.depart_time)