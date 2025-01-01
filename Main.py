# Jacob Wanner
# Student ID: 011977947

import csv
import datetime
import Truck
from Package import Package
from HashTable import CreateHashTable
from builtins import ValueError

# Read the CSV files
with open("CSV/WGUPS Address File.csv") as csvAddress:
    CSV_Address = csv.reader(csvAddress)
    CSV_Address = list(CSV_Address)

with open("CSV/WGUPS Distance Table.csv") as csvDistance:
    CSV_Distance = csv.reader(csvDistance)
    CSV_Distance = list(CSV_Distance)

with open("CSV/WGUPS Package File.csv") as csvPackage:
    CSV_Package = csv.reader(csvPackage)
    CSV_Package = list(CSV_Package)


# Load package objects into the hash table called package_hash_table
def load_package_data(filename, package_hash_table):
    with open(filename) as package_info:
        package_data = csv.reader(package_info)
        for package in package_data:
            pID = int(package[0])
            #print(pID)
            pAddress = package[1]
            # print(pAddress)
            pCity = package[2]
            # print(pCity)
            pState = package[3]
            # print(pState)
            pZipcode = package[4]
            # print(pZipcode)
            pDeadline_time = package[5]
            # print(pDeadline_time)
            pWeight = package[6]
            # print(pWeight)
            pStatus = "At WGUPS Hub"

            # boxes info into Package object
            p = Package(pID, pAddress, pCity, pState, pZipcode, pDeadline_time, pWeight, pStatus)
            #print(p)
            # Insert data into hash table
            package_hash_table.insert(pID, p)


# Initializes the hash table
package_hash_table = CreateHashTable()

# Load packages into hash table
load_package_data("CSV/WGUPS Package File.csv", package_hash_table)


# Gets address number
def get_address(address):
    for row in CSV_Address:
        if address in row[2]:
            return int(row[0])


#finds the distance between two addresses
def distance_between(x_value, y_value):
    distance = CSV_Distance[x_value][y_value]
    if distance == '':
        distance = CSV_Distance[y_value][x_value]
    return float(distance)

#Creates truck objects and loads packages on truck
truck1 = Truck.Truck( 16, 18, None, [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East", datetime.timedelta(hours=8))
truck2 = Truck.Truck( 16, 18, None, [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33, 39], 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))
truck3 = Truck.Truck( 16, 18, None, [3, 12, 17, 18, 21, 22, 23, 24, 26, 27, 35, 36, 38], 0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))


# Greedy Algorithm Big-O Time Complexity: O(n^2)
# Algorithm of delivering all packages on truck via nearest neighbor
def delivering_packages(truck):
    # All packages from truck into an array
    not_delivered = []
    for packageID in truck.packages:
        package = package_hash_table.search(packageID)
        not_delivered.append(package)
    # clear array of packages on truck object
    truck.packages.clear()

    # Cycle through the list of not_delivered packages adding the nearest delivery address from current address back onto the truck object
    while len(not_delivered) > 0:
        next_address = 5678
        next_package = None
        for package in not_delivered:
            if package.ID in [25, 6]:
                next_package = package
                next_address = distance_between(get_address(truck.street), get_address(package.street))
                break
            if distance_between(get_address(truck.street), get_address(package.street)) <= next_address:
                next_package = package
                next_address = distance_between(get_address(truck.street), get_address(package.street))
        # Appends next closest package to the truck object
        truck.packages.append(next_package.ID)
        # Removes package from the not_delivered array
        not_delivered.remove(next_package)
        # Adds delivery route miles to total truck mileage
        truck.miles += next_address
        # Updates truck address to delivery site
        truck.street = next_package.street
        # Adds the time it took the truck to drive to delivery site
        truck.time += datetime.timedelta(hours=next_address / 18)
        # Assigns package delivery time to current time
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.depart_time


# Calls trucks to deliver the packages
delivering_packages(truck1)
delivering_packages(truck2)
# The 3rd truck departure time is set to when either truck1 or truck2 finish their route
truck3.depart_time = min(truck1.time, truck2.time)
delivering_packages(truck3)


class Main:
    # User Interface
    print("Western Governors University Parcel Service (WGUPS)")
    print("The mileage for the route is: " + str(truck1.miles + truck2.miles + truck3.miles))
    # The user will be asked to enter a specific time to check packages
    user_time = input("Please enter a time to check status of package(s). Use the following format, HH:MM")
    (h, m) = user_time.split(":")
    convert_timedelta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(00))
    # The user will be asked if they want to see the status of all packages or only one
    second_input = input("To view the status of an individual package please type 'solo'. For a rundown of all packages please type 'all'.")
    # If the user enters "solo" the program will ask for one package ID
    if second_input == "solo":
        try:
            # The user will be asked to input a package ID.
            solo_input = input("Enter the numeric package ID")
            package = package_hash_table.search(int(solo_input))
            package.update_status(convert_timedelta)
            print(str(package))
        except ValueError:
            print("Entry invalid. Closing program.")
            exit()
    # If the user types "all" the program will display all package information at once
    elif second_input == "all":
        try:
            for packageID in range(1, 41):
                package = package_hash_table.search(packageID)
                package.update_status(convert_timedelta)
                print(str(package))
        except ValueError:
            print("Entry invalid. Closing program.")
            exit()
    else:
        exit()