from datetime import timedelta

# Class for packages
class Package:
    def __init__(self, ID, street, city, state, zipcode, Deadline_time, weight, status, correction_time=None):
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
        self.which_truck = None
        self.correction_time = correction_time

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.ID, self.street, self.city, self.state, self.zipcode, self.Deadline_time, self.weight, self.delivery_time, self.status, self.which_truck)
    # Updates the status of package delivery
    def update_status(self, convert_timedelta):
        if self.delivery_time is None:
            self.status = "At WGUPS Hub"
        elif self.delivery_time < convert_timedelta:
            self.status = "Delivered"
        elif self.departure_time > convert_timedelta:
            self.status = "En route for Delivery"

    def get_package_info(self, user_entered_time):
        temp_status = "En route"
        if user_entered_time < self.departure_time:
            temp_status = "At WGUPS Hub"
        elif user_entered_time > self.delivery_time:
            temp_status = "Delivered"

        temp_street = self.street
        temp_zipcode = self.zipcode
        if self.ID == 9:
            if user_entered_time < timedelta(hours = 10, minutes = 20):
                temp_street = "300 State Street"
                temp_zipcode = "84103"
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.ID, temp_street, self.city, self.state, temp_zipcode, self.Deadline_time, self.weight, self.delivery_time, temp_status, self.which_truck)
