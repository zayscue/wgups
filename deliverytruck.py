# Zackery Ayscue 000901676
from deliverystatus import AVAILABLE_AT_HUB, IN_ROUTE

class DeliveryTruck:
  def __init__(self, truck_id, current_location):
    self.truck_id = truck_id
    self.current_location = current_location
    self.packages = []
    self.priority_packages = {}
    self.normal_packages = []
    self.package_limit = 16
    self.route = None

  # add package to the package list and then add it's index
  # to the priority dictionary.
  # the dictionary is organized as <deadline_string, list<packages_index>>
  # O(n) = O(1)
  def add_priority_package(self, priority_package):
    deadline = priority_package.deadline
    index = len(self.packages)
    self.packages.append(priority_package)
    if deadline in self.priority_packages:
      self.priority_packages[deadline].append(index)
    else:
      self.priority_packages[deadline] = [index]

  # add package to the package list and then add it's index
  # to the normal_package list.
  # O(n) = O(1)
  def add_package(self, package):
    index = len(self.packages)
    self.packages.append(package)
    self.normal_packages.append(index)

  # Check if the truck can hold another package
  # O(n) = O(1)
  def can_hold_another_package(self):
    return len(self.packages) < self.package_limit

  # Returns a list of priority packages in sorted order
  # O(n) = O((n log n) + (n * m)), n = number of keys,
  # m = number of items in priority dict value 
  def get_priority_packages(self):
    priority_package_list = []
    keys = sorted(list(self.priority_packages.keys()), reverse=True)
    for key in keys:
      packages_indexes = self.priority_packages[key]
      for package_index in packages_indexes:
        priority_package_list.append(self.packages[package_index])
    return priority_package_list

  # Returns a list of normal packages
  # O(n) = O(n)
  def get_normal_packages(self):
    normal_package_list = []
    for package_index in self.normal_packages:
      normal_package_list.append(self.packages[package_index])
    return normal_package_list

  # Load package onto truck
  # O(n) = O(1)
  def load(self, package):
    if package.delivery_status != AVAILABLE_AT_HUB:
      print('Only packages at the hub can be loaded on the truck')
      return
    if package.deadline != '':
      self.add_priority_package(package)
    else:
      self.add_package(package)
    package.truck = self

  # Set route for truck
  # O(n) = O(1)
  def set_route(self, route):
    self.route = route

  # Get route for truck
  # O(n) = O(1)
  def get_route(self):
    return self.route

  # Mark the delivery_status of all packages on board
  # to IN_ROUTE
  # O(n) = O(n)
  def start_delivery_route(self):
    for package in self.route:
      package.delivery_status = IN_ROUTE
