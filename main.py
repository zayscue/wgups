import csv
import json
from linearprobinghashtable import LinearProbingHashTable
from package import Package
from location import Location
from graph import Graph, Vertex
from requiredtruckdeliveryrule import RequiredTruckDeliveryRule
from delayeddeliveryrule import DelayedDeliveryRule
from wrongaddressdeliveryrule import WrongAddressDeliveryRule
from deliveredtogetherdeliveryrule import DeliveredTogetherDeliveryRule
from linearprobinghashtable import LinearProbingHashTable
from packagesHashTable import PackagesHashTable
from deliverytruck import DeliveryTruck
from operator import itemgetter, attrgetter
from clock import Clock
from deliverystatus import DELIVERED
from dataloader import DataLoader
from distancesgraph import DistancesGraph

data_loader = DataLoader()


def create_delivery_rule_list():
    delivery_rules = []
    delivery_rules_data = data_loader.load_delivery_rules_csv(
        './data/deliveryrules.csv')
    for element in delivery_rules_data:
        description = element['description']
        package_id = element['package_id']
        type = element['type']
        rule_data = element['data']
        if type == 'REQUIRED_TRUCK':
            truck_id = rule_data['truck_id']
            delivery_rules.append(RequiredTruckDeliveryRule(
                description, package_id, truck_id))
        elif type == 'DELAYED':
            delayed_until = rule_data['delayed_until']
            delivery_rules.append(DelayedDeliveryRule(
                description, package_id, delayed_until))
        elif type == 'DELIVERED_TOGETHER':
            delivered_with = rule_data['delivered_with']
            delivery_rules.append(DeliveredTogetherDeliveryRule(
                description, package_id, delivered_with))
        elif type == 'WRONG_ADDRESS':
            corrected_at = rule_data['corrected_at']
            new_street_address = rule_data['new_street_address']
            new_city = rule_data['new_city']
            new_state = rule_data['new_state']
            new_zip_code = rule_data['new_zip_code']
            delivery_rules.append(WrongAddressDeliveryRule(
                description, package_id, corrected_at, new_street_address, new_city, new_state, new_zip_code))
    return delivery_rules


def create_distances_graph():
    distances_data = data_loader.load_distances_csv('./data/distances.csv')
    distances_graph = DistancesGraph(distances_data)
    return distances_graph


def create_packages_hash_table():
    locations_data = data_loader.load_locations_csv('./data/locations.csv')
    locations_hash_table = LinearProbingHashTable(len(locations_data))
    for element in locations_data:
        name = element['name']
        street = element['street']
        city = element['city']
        state = element['state']
        zip_code = element['zip_code']
        index = element['index']
        location = Location(name, street, city, state, zip_code, index)
        locations_hash_table.insert(location)
    packages_hash_table = PackagesHashTable(locations_hash_table)
    packages_data = data_loader.load_packages_csv('./data/packages.csv')
    for element in packages_data:
        package_id = element['package_id']
        delivery_address = element['delivery_address']
        city = element['city']
        zip_code = element['zip_code']
        weight = element['weight']
        deadline = element['deadline']
        packages_hash_table.insert(
            package_id, delivery_address, deadline, city, zip_code, weight)
    return packages_hash_table


def in_route(distances_graph, starting_time, truck):
    starting_location = truck.current_location
    time = starting_time
    route = truck.get_route()
    total_distance = 0
    for package in route:
        package_location = package.delivery_address
        distance = distances_graph.get_distance(
            truck.current_location.graph_index, package_location.graph_index)
        minutes = (distance/18.0) * 60
        if (truck.current_location != (package_location.street, package_location.city, package_location.zip_code)):
          print('Traveling from {} -> {}, it is {} miles away and should take {} minutes'.format(truck.current_location.name, package_location.name, distance, minutes))
        total_distance += distance
        time.add_minutes(minutes)
        truck.current_location = package_location
        package.delivery_status = DELIVERED
        deadline = package.deadline
        if deadline != '':
            deadline = ', the deadline was {}'.format(deadline)
        print('Package {} was delivered to {} at {}{}'.format(package.package_id, package.delivery_address, time, deadline))
    distance_back_to_hub = distances_graph.get_distance(
        truck.current_location.graph_index, starting_location.graph_index)
    total_distance += distance_back_to_hub
    minutes_back_to_hub = (distance_back_to_hub/18.0) * 60
    time.add_minutes(minutes_back_to_hub)
    print('Total Distance: {} miles'.format(total_distance))
    print('Final time: {}'.format(time))
    return (time.hours, time.minutes, total_distance)


# Main program
def main():
    # create data structures
    distances_graph = create_distances_graph()
    delivery_rules_list = create_delivery_rule_list()
    packages_hash_table = create_packages_hash_table()
    hub_location = packages_hash_table.locations.search(
        ('4001 South 700 East', 'Salt Lake City', '84107'))

    common_location = packages_hash_table.locations.search(
        ('4580 S 2300 E', 'Holladay', '84117'))

    truck_one = DeliveryTruck('1', hub_location)
    truck_two = DeliveryTruck('2', hub_location)
    truck_three = DeliveryTruck('3', hub_location)
    trucks_dict = {
      truck_one.truck_id: truck_one,
      truck_two.truck_id: truck_two,
      truck_three.truck_id: truck_three
    }

    # load packages onto required trucks
    truck_two.load(packages_hash_table.search('3'))
    truck_two.load(packages_hash_table.search('18'))
    truck_two.load(packages_hash_table.search('36'))
    truck_two.load(packages_hash_table.search('38'))

    # load delayed packages on to truck 2 which leave at 9:05 AM
    truck_two.load(packages_hash_table.search('6'))
    truck_two.load(packages_hash_table.search('25'))
    truck_two.load(packages_hash_table.search('28'))
    truck_two.load(packages_hash_table.search('32'))

    # load packages that have to be shipped together on
    # truck 1 because most of them have deadlines
    # and should be loaded on truck 1 which leaves
    # at 8:00 AM
    truck_one.load(packages_hash_table.search('13'))
    truck_one.load(packages_hash_table.search('14'))
    truck_one.load(packages_hash_table.search('15'))
    truck_one.load(packages_hash_table.search('16'))
    truck_one.load(packages_hash_table.search('19'))
    truck_one.load(packages_hash_table.search('20'))

    # load package with wrong address onto truck 3 which leaves
    # when either truck 1 or truck 2 returns to the hub
    truck_three.load(packages_hash_table.search('9'))

    def load_priority_packages_on_truck(truck):
      priority_packages = packages_hash_table.get_available_priority_packages()
      number_of_priority_packages = len(priority_packages)
      for priority_package in priority_packages:
        if truck.can_hold_another_package() == False:
          continue
        truck.load(priority_package)
        number_of_priority_packages -= 1
        packages_at_the_same_location = packages_hash_table.get_availabe_packages_by_location(priority_package.delivery_address)
        number_of_available_packages_at_same_location = len(packages_at_the_same_location)
        max_number = truck.package_limit - len(truck.packages) - number_of_priority_packages
        upper_limit = min(number_of_available_packages_at_same_location, max_number)
        for i in range(0, upper_limit):
          truck.load(packages_at_the_same_location[i])

    # Next load all the rest of the priority packages on truck 1
    load_priority_packages_on_truck(truck_one)

    # If there are any more priority package load onto truck 2
    load_priority_packages_on_truck(truck_two)

    availabe_packages = packages_hash_table.get_available_packages()
    number_available_packages = len(availabe_packages)
    availabe_package_index = 0
    while number_available_packages > 0:
      availabe_package = availabe_packages[availabe_package_index]
      if availabe_package.truck != None:
        availabe_package_index += 1
        number_available_packages -= 1
        continue
      next_truck = min([truck_one, truck_two, truck_three], key=lambda t : len(t.packages))
      next_truck.load(availabe_package)
      packages_at_the_same_location = packages_hash_table.get_availabe_packages_by_location(availabe_package.delivery_address)
      number_of_available_packages_at_same_location = len(packages_at_the_same_location)
      max_number = next_truck.package_limit - len(next_truck.packages)
      upper_limit = min(number_of_available_packages_at_same_location, max_number)
      for i in range(0, upper_limit):
          next_truck.load(packages_at_the_same_location[i])
      availabe_package_index += 1
      number_available_packages -= 1


    def caculate_route(truck):
        route = []
        priority = truck.get_priority_packages()
        current_location = None
        index = 0
        while len(priority) > 0:
            if index == 0:
                p = priority.pop(0)
                route.append(p)
                current_location = p.delivery_address
                index += 1
            else:
                nearest_distance = None
                nearest_location = None
                next_package_index = None
                counter = 0
                for package in priority:
                    package_location = package.delivery_address
                    distance = distances_graph.get_distance(current_location.graph_index, package_location.graph_index)
                    if nearest_distance == None:
                        nearest_distance = distance
                        nearest_location = package_location
                        next_package_index = counter
                    else:
                        if distance < nearest_distance:
                            nearest_distance = distance
                            nearest_location = package_location
                            next_package_index = counter
                    counter += 1
                route.append(priority.pop(next_package_index))
                current_location = nearest_location
                index += 1
        normal = truck.get_normal_packages()
        while len(normal) > 0:
            if index == 0:
                p = normal.pop(0)
                route.append(p)
                current_location = p.delivery_address
                index += 1
            else:
                nearest_distance = None
                nearest_location = None
                next_package_index = None
                counter = 0
                for package in normal:
                    package_location = package.delivery_address
                    distance = distances_graph.get_distance(current_location.graph_index, package_location.graph_index)
                    if nearest_distance == None:
                        nearest_distance = distance
                        nearest_location = package_location
                        next_package_index = counter
                    else:
                        if distance < nearest_distance:
                            nearest_distance = distance
                            nearest_location = package_location
                            next_package_index = counter
                    counter += 1
                route.append(normal.pop(next_package_index))
                current_location = nearest_location
                index += 1
        return route

    truck_one_route = caculate_route(truck_one)
    truck_one.set_route(truck_one_route)
    truck_one.start_delivery_route()
    truck_two_route = caculate_route(truck_two)
    truck_two.set_route(truck_two_route)
    truck_two.start_delivery_route()
    truck_three_route = caculate_route(truck_three)
    truck_three.set_route(truck_three_route)
    truck_three.start_delivery_route()

    truck_one_time = Clock(8, 0)
    print('Truck 1 leaving hub at {}'.format(truck_one_time))
    truck_one_result = in_route(distances_graph, truck_one_time, truck_one)
    print()

    truck_two_time = Clock(9, 5)
    print('Truck 2 leaving hub at {}'.format(truck_two_time))
    truck_two_result = in_route(distances_graph, truck_two_time, truck_two)
    print()

    truck_three_starting_hours = 10
    truck_three_starting_minutes = 20

    if truck_one_result[0] < truck_two_result[0]:
      if truck_one_result[0] >= truck_three_starting_hours and truck_one_result[1] >= truck_three_starting_minutes:
        truck_three_starting_hours = truck_one_result[0]
        truck_three_starting_minutes = truck_one_result[1]
    elif truck_one_result[0] > truck_two_result[0]:
      if truck_two_result[0] >= truck_three_starting_hours and truck_two_result[1] >= truck_three_starting_minutes:
        truck_three_starting_hours = truck_two_result[0]
        truck_three_starting_minutes = truck_two_result[1]
    else:
      if truck_one_result[1] < truck_two_result[1]:
        if truck_one_result[0] >= truck_three_starting_hours and truck_one_result[1] >= truck_three_starting_minutes:
          truck_three_starting_hours = truck_one_result[0]
          truck_three_starting_minutes = truck_one_result[1]
      elif truck_one_result[1] > truck_two_result[1]:
        if truck_two_result[0] >= truck_three_starting_hours and truck_two_result[1] >= truck_three_starting_minutes:
          truck_three_starting_hours = truck_two_result[0]
          truck_three_starting_minutes = truck_two_result[1]
      else:
        if truck_one_result[0] >= truck_three_starting_hours and truck_one_result[1] >= truck_three_starting_minutes:
          truck_three_starting_hours = truck_one_result[0]
          truck_three_starting_minutes = truck_one_result[1]


    truck_three_time = Clock(truck_three_starting_hours, truck_three_starting_minutes)
    print('Truck 3 leaving hub at {}'.format(truck_three_time))
    truck_three_result = in_route(distances_graph, truck_three_time,  truck_three)
    total_traveled_miles_of_all_three_trucks = truck_one_result[2] + truck_two_result[2] + truck_three_result[2]
    print('Total Traveled miles of all three trucks: {}'.format(total_traveled_miles_of_all_three_trucks))

if __name__ == '__main__':
    main()
