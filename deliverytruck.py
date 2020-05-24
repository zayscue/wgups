from deliverystatus import AVAILABLE_AT_HUB, IN_ROUTE

class DeliveryTruck:
  def __init__(self, truck_id, current_location):
    self.truck_id = truck_id
    self.current_location = current_location
    self.packages = []
    self.priority_packages = {}
    self.normal_packages = []
    self.package_limit = 16

  def add_priority_package(self, priority_package):
    deadline = priority_package.deadline
    index = len(self.packages)
    self.packages.append(priority_package)
    if deadline in self.priority_packages:
      self.priority_packages[deadline].append(index)
    else:
      self.priority_packages[deadline] = [index]

  def add_package(self, package):
    index = len(self.packages)
    self.packages.append(package)
    self.normal_packages.append(index)

  def can_hold_another_package(self):
    return len(self.packages) < self.package_limit

  def get_priority_packages(self):
    priority_package_list = []
    keys = sorted(list(self.priority_packages.keys()), reverse=True)
    for key in keys:
      packages_indexes = self.priority_packages[key]
      for package_index in packages_indexes:
        priority_package_list.append(self.packages[package_index])
    return priority_package_list

  def get_normal_packages(self):
    normal_package_list = []
    for package_index in self.normal_packages:
      normal_package_list.append(self.packages[package_index])
    return normal_package_list

  def load(self, package):
    if package.delivery_status != AVAILABLE_AT_HUB:
      print('Only packages at the hub can be loaded on the truck')
      return
    if package.deadline != '':
      self.add_priority_package(package)
    else:
      self.add_package(package)
    package.truck = self

  def set_route(self, route):
    self.route = route

  def get_route(self):
    return self.route

  def start_delivery_route(self):
    for package in self.route:
      package.delivery_status = IN_ROUTE
