import csv
import datetime
from Truck import Truck
from Package import Package
from HashTable import CreateHashTable


# Read CSV Files
def read_csv(file_path, delimiter=","):
    with open(file_path) as file:
        return list(csv.reader(file, delimiter=delimiter))


# Load package data into hash table
def load_packages_to_hash_table(filename, hash_table):
    with open(filename) as file:
        package_data = csv.reader(file)
        for row in package_data:
            package_id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zipcode = row[4]
            deadline = row[5]
            weight = row[6]
            status = "At WGUPS Hub"

            # Define the correction time for package #9 (10:20 a.m.)
            correction_time = None
            if package_id == 9:
                correction_time = datetime.timedelta(hours=10, minutes=20)

            package = Package(package_id, address, city, state, zipcode, deadline, weight, status)
            hash_table.insert(package_id, package)


# Initialize hash table
package_hash_table = CreateHashTable()

# Read CSV files for addresses, distances, and packages
address_data = read_csv("CSV/WGUPS Address File.csv")
distance_data = read_csv("CSV/WGUPS Distance Table.csv")
package_data = read_csv("CSV/WGUPS Package File.csv")


# Find the address ID given an address
def find_address_id(address_string):
    for row in address_data:
        if address_string in row[2]:
            return int(row[0])


# Calculate the distance between two addresses
def get_distance(address1_id, address2_id):
    dist = distance_data[address1_id][address2_id]
    return float(dist) if dist else float(distance_data[address2_id][address1_id])


# Initialize truck objects
truck1 = Truck(1,18, None, [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East", datetime.timedelta(hours=8))
truck2 = Truck(2, 18, None, [3, 5, 6, 7, 8, 10, 11, 18, 25, 28, 32, 33, 36, 38], 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))
truck3 = Truck(3,18, None, [2, 4, 9, 12, 17, 21, 22, 23, 24, 26, 27, 35, 39], 0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))


# Delivery function to deliver packages using nearest neighbor algorithm
def deliver_packages(truck):
    remaining_packages = [package_hash_table.search(package_id) for package_id in truck.packages]
    truck.packages.clear()

    while remaining_packages:
        nearest_package = None
        nearest_distance = float("inf")

        for package in remaining_packages:
            distance = get_distance(find_address_id(truck.street), find_address_id(package.street))
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_package = package

        truck.packages.append(nearest_package.ID)
        remaining_packages.remove(nearest_package)
        truck.miles += nearest_distance
        truck.street = nearest_package.street
        truck.time += datetime.timedelta(hours=nearest_distance / 18)
        nearest_package.delivery_time = truck.time
        nearest_package.departure_time = truck.depart_time
        nearest_package.which_truck = f"truck{truck.number}"

# Load packages into the hash table
load_packages_to_hash_table("CSV/WGUPS Package File.csv", package_hash_table)

# Perform deliveries for each truck
deliver_packages(truck1)
deliver_packages(truck2)

# Ensure truck3 waits for either truck1 or truck2 to finish but also departs after 10:20 AM.
truck3_depart_time = min(truck1.time, truck2.time)

# Only deliver package 9
package9 = package_hash_table.search(9)
package9.street = "410 S State St"
package9.city = "Salt Lake City"
package9.state = "UT"
package9.zipcode = "84111"

deliver_packages(truck3)


class WGUPSInterface:
    def __init__(self, truck1, truck2, truck3, package_hash_table):
        # Initialize the interface with trucks and package hash table
        self.truck1 = truck1
        self.truck2 = truck2
        self.truck3 = truck3
        self.package_hash_table = package_hash_table

    def display_mileage(self):
        # Calculate and display the total mileage for all trucks
        total_miles = self.truck1.miles + self.truck2.miles + self.truck3.miles
        print(f"Western Governors University Parcel Service (WGUPS)")
        print(f"Total mileage for all routes: {total_miles:.2f} miles.")

    def get_package_status(self, convert_timedelta):
        # Prompt the user to check the status of a single package or all packages

            user_choice = input("Would you like to check the status of one package or all? (Enter 'solo' or 'all'): ").strip().lower()
            if user_choice == 'solo':
                # Call function to check the status of a single package
                self.check_single_package(convert_timedelta)
            elif user_choice == 'all':
                # Call function to check the status of all packages
                self.check_all_packages(convert_timedelta)
            elif user_choice == 'quit':
                return "quit"
            else:
                # Handle invalid input choice
                print("Invalid choice. Please enter 'solo' or 'all'.")

    def get_user_time(self):
        # Prompt the user to input the time in HH:MM format and return the timedelta object
            user_input = input("Enter a specific time to check the status of the packages (HH:MM): ")
            hours, minutes = user_input.split(":")
            return datetime.timedelta(hours=int(hours), minutes=int(minutes))

    def check_single_package(self, convert_timedelta):
        # Prompt user to input a package ID and display its status
            package_id = int(input("Enter the Package ID: "))
            package = self.package_hash_table.search(package_id)  # Find the package using hash table
            print(package.get_package_info(convert_timedelta))  # Print the package details

    def check_all_packages(self, convert_timedelta):
        # Display the status of all packages (1 through 40)
        for package_id in range(1, 41):
            package = self.package_hash_table.search(package_id)  # Find the package using hash table
            print(package.get_package_info(convert_timedelta))  # Print the package details

    def run(self):
        # Run the main interface for displaying mileage and getting user input for package status
        while True:
            self.display_mileage()
            convert_timedelta = self.get_user_time()  # Get user time input
            x = self.get_package_status(convert_timedelta)  # Get package status based on time
            if x == "quit":
                break

# Create the interface object and run it
interface = WGUPSInterface(truck1, truck2, truck3, package_hash_table)
interface.run()