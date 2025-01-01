# Class for packages
class Package:
    def __init__(self, ID, street, city, state, zipcode, Deadline_time, weight, status):
        self.ID = ID
        self.street = street
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.Deadline_time = Deadline_time
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.ID, self.street, self.city, self.state, self.zipcode, self.Deadline_time, self.weight, self.delivery_time, self.status)
    # Updates the status of package delivery
    def update_status(self, convert_timedelta):
        if self.delivery_time is None:
            self.status = "At WGUPS Hub"
        elif self.delivery_time < convert_timedelta:
            self.status = "Delivered"
        elif self.departure_time > convert_timedelta:
            self.status = "En route for Delivery"