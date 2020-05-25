# Zackery Ayscue 000901676

from deliverytruck import DeliveryTruck
from mytime import Time
from packageshashtable import PackagesHashTable
from deliverystatus import DELIVERED

PACKAGES_REQUIRED_TO_BE_ON_TRUCK_TWO = ['3', '18', '36', '38']
PACKAGES_DELAYED_UNTIL_9_05_AM = ['6', '25', '28', '32']
PACKAGES_NEEDED_TO_BE_SHIPPED_TOGETHER = ['13', '14', '15', '16', '19', '20']
PACKAGES_WITH_WRONG_ADDRESS = ['9']

# load packages onto required trucks
def load_packages_required_to_be_on_truck_two(packages, truck_two):
  for package_id in PACKAGES_REQUIRED_TO_BE_ON_TRUCK_TWO:
    package = packages.search(package_id)
    if package != None:
      truck_two.load(package)

# load delayed packages on to truck
def load_delayed_packages(packages, truck):
  for package_id in PACKAGES_DELAYED_UNTIL_9_05_AM:
    package = packages.search(package_id)
    if package != None:
      truck.load(package)

# load packages needed to be shipped together
def load_packages_needed_to_be_shipped_together(packages, truck):
  for package_id in PACKAGES_NEEDED_TO_BE_SHIPPED_TOGETHER:
    package = packages.search(package_id)
    if package != None:
      truck.load(package)

# load packages with wrong address
def load_packages_with_wrong_address(packages, truck):
  for package_id in PACKAGES_WITH_WRONG_ADDRESS:
    package = packages.search(package_id)
    if package != None:
      truck.load(package)

# load priority packages
def load_priority_packages(packages, truck):
  priority_packages = packages.get_available_priority_packages()
  number_of_priority_packages = len(priority_packages)
  for priority_package in priority_packages:
      if truck.can_hold_another_package() == False:
          continue
      truck.load(priority_package)
      number_of_priority_packages -= 1
      packages_at_the_same_location = packages.find(
        delivery_address=priority_package.delivery_address.street,
        city=priority_package.delivery_address.city,
        zip_code=priority_package.delivery_address.zip_code
      )
      number_of_available_packages_at_same_location = len(
          packages_at_the_same_location)
      max_number = truck.package_limit - \
          len(truck.packages) - number_of_priority_packages
      upper_limit = min(
          number_of_available_packages_at_same_location, max_number)
      for i in range(0, upper_limit):
          truck.load(packages_at_the_same_location[i])

# load the rest of the packages
def round_robin_rest_of_packages(packages, trucks):
  availabe_packages = packages.get_available_packages()
  number_available_packages = len(availabe_packages)
  availabe_package_index = 0
  while number_available_packages > 0:
    availabe_package = availabe_packages[availabe_package_index]
    if availabe_package.truck != None:
      availabe_package_index += 1
      number_available_packages -= 1
      continue
    next_truck = min(trucks, key=lambda t : len(t.packages))
    next_truck.load(availabe_package)
    packages_at_the_same_location = packages.get_availabe_packages_by_location(availabe_package.delivery_address)
    number_of_available_packages_at_same_location = len(packages_at_the_same_location)
    max_number = next_truck.package_limit - len(next_truck.packages)
    upper_limit = min(number_of_available_packages_at_same_location, max_number)
    for i in range(0, upper_limit):
        next_truck.load(packages_at_the_same_location[i])
    availabe_package_index += 1
    number_available_packages -= 1

# Use a modified nearest neighbor algorithm prioritizing packages
# with deadlines first
def caculate_route(truck, distances):
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
              distance = distances.get_distance(
                  current_location.graph_index, package_location.graph_index)
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
              distance = distances.get_distance(
                  current_location.graph_index, package_location.graph_index)
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

def in_route(distances, starting_time, truck):
  starting_location = truck.current_location
  time = starting_time
  route = truck.get_route()
  total_distance = 0
  for package in route:
      package_location = package.delivery_address
      distance = distances.get_distance(
          truck.current_location.graph_index, package_location.graph_index)
      minutes = (distance/18.0) * 60
      if (truck.current_location != (package_location.street, package_location.city, package_location.zip_code)):
          print('Traveling from {} -> {}, it is {} miles away and should take {} minutes'.format(
              truck.current_location.name, package_location.name, distance, minutes))
      total_distance += distance
      time.add_minutes(minutes)
      truck.current_location = package_location
      package.delivery_status = DELIVERED
      deadline = package.deadline
      if deadline != '':
          deadline = ', the deadline was {}'.format(deadline)
      print('Package {} was delivered to {} at {}{}'.format(
          package.package_id, package.delivery_address, time, deadline))
  distance_back_to_hub = distances.get_distance(
      truck.current_location.graph_index, starting_location.graph_index)
  total_distance += distance_back_to_hub
  minutes_back_to_hub = (distance_back_to_hub/18.0) * 60
  time.add_minutes(minutes_back_to_hub)
  print('Total Distance: {} miles'.format(total_distance))
  print('Final time: {}'.format(time))
  return (time.hours, time.minutes, total_distance)

class App(object):
  def __init__(self, distances, locations, packages=None):
    super().__init__()
    if packages == None:
      self.packages = PackagesHashTable(locations)
    else: 
      self.packages = packages
    self.distances = distances
    self.locations = locations

    hub_location = self.locations.search(('4001 South 700 East', 'Salt Lake City', '84107'))

    self.truck_one = DeliveryTruck('1', hub_location)
    self.truck_two = DeliveryTruck('2', hub_location)
    self.truck_three = DeliveryTruck('3', hub_location)

  # Add another package to the simulation
  def add_package(self, package_id, delivery_address, deadline, city, zip_code, weight):
    self.packages.insert(package_id, delivery_address, deadline, city, zip_code, weight)

  # find packages from the packages
  def find_packages(self, package_id = None, delivery_address = None, deadline = None, city = None, zip_code = None, weight = None, delivery_status = None):
    return self.packages.find(package_id, delivery_address, deadline, city, zip_code, weight, delivery_status)

  # start running the simulation
  def run(self):
    # load packages onto required trucks
    load_packages_required_to_be_on_truck_two(self.packages, self.truck_two)

    # load delayed packages on to truck 2 which leave at 9:05 AM
    load_delayed_packages(self.packages, self.truck_two)

    # load packages that have to be shipped together on
    # truck 1 because most of them have deadlines
    # and should be loaded on truck 1 which leaves
    # at 8:00 AM
    load_packages_needed_to_be_shipped_together(self.packages, self.truck_one)

    # load package with wrong address onto truck 3 which leaves
    # when either truck 1 or truck 2 returns to the hub
    load_packages_with_wrong_address(self.packages, self.truck_three)

    # Next load all the rest of the priority packages on truck 1
    load_priority_packages(self.packages, self.truck_one)

    # If there are any more priority package load onto truck 2
    load_priority_packages(self.packages, self.truck_two)

    # Round robin load the rest of the packages
    round_robin_rest_of_packages(self.packages, [self.truck_one, self.truck_two, self.truck_three])

    # Calculate route for truck one
    self.truck_one.route = caculate_route(self.truck_one, self.distances)

    # Calculate route for truck two
    self.truck_two.route = caculate_route(self.truck_two, self.distances)

    # Calculate route for truck three
    self.truck_three.route = caculate_route(self.truck_three, self.distances)

    # Simulate truck one
    truck_one_time = Time(8, 0)
    print('Truck 1 leaving hub at {}'.format(truck_one_time))
    self.truck_one.start_delivery_route()
    truck_one_result = in_route(self.distances, truck_one_time, self.truck_one)
    print()

    # Simulate truck two
    truck_two_time = Time(9, 5)
    print('Truck 2 leaving hub at {}'.format(truck_two_time))
    self.truck_one.start_delivery_route()
    truck_two_result = in_route(self.distances, truck_two_time, self.truck_two)
    print()

    # Simulate truck three
    truck_three_time = min(Time(10, 20), truck_one_time, truck_two_time)
    print('Truck 3 leaving hub at {}'.format(truck_three_time))
    self.truck_one.start_delivery_route()
    truck_three_result = in_route(self.distances, truck_three_time,  self.truck_three)

    # Overall results
    total_traveled_miles_of_all_three_trucks = truck_one_result[2] + truck_two_result[2] + truck_three_result[2]
    print('Total Traveled miles of all three trucks: {}'.format(total_traveled_miles_of_all_three_trucks))



