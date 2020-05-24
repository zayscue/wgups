from linearprobinghashtable import LinearProbingHashTable
from package import Package
from deliverystatus import AVAILABLE_AT_HUB
from set import Set

class PackagesHashTable(LinearProbingHashTable):
  def __init__(self, locations, initial_capacity=40):
    self.locations = locations
    super().__init__(initial_capacity)

  def insert(self, package_id, delivery_address, deadline, city, zip_code, weight, delivery_status=AVAILABLE_AT_HUB):
    location = self.locations.search((delivery_address, city, zip_code))
    package = Package(package_id, location, deadline, weight, delivery_status)
    return super().insert(package)

  def search(self, package_id):
    package = super().search(package_id)
    return package

  def get_packages_with_a_deadline(self):
    packages_with_deadline = filter(lambda x : x.deadline != '', self.table)
    def get_deadline(package):
      return package.deadline
    sorted_packages_by_deadline = sorted(packages_with_deadline, key=get_deadline, reverse=True)
    return sorted_packages_by_deadline

  def get_packages_available_at_hub(self):
    package_available_at_hub = list(filter(lambda x : x.delivery_status == AVAILABLE_AT_HUB, self.table))
    return package_available_at_hub

  def get_availabe_packages_by_location(self, location):
    def get_key(el):
      return el.package_id
    packages_set = Set(get_key)
    packages_list = list(self.table)
    for package in packages_list:
      packages_set.add(package)
    location_key = (location.street, location.city, location.zip_code)
    packages_subset = packages_set.filter(lambda p : p.delivery_address == location_key and p.truck == None)
    return list(packages_subset)

  def get_available_packages_by_zip_code(self, zip_code):
    def get_key(el):
      return el.package_id
    packages_set = Set(get_key)
    packages_list = list(self.table)
    for package in packages_list:
      packages_set.add(package)
    packages_subset = packages_set.filter(lambda p : p.delivery_address.zip_code == zip_code and p.truck == None)
    return list(packages_subset)

  def get_available_priority_packages(self):
    def get_key(el):
      return el.package_id
    packages_set = Set(get_key)
    packages_list = list(self.table)
    for package in packages_list:
      packages_set.add(package)
    def predicate(p):
      return p.deadline != '' and p.truck == None
    packages_subset = packages_set.filter(predicate)
    return list(packages_subset)

  def get_available_packages(self):
    def get_key(el):
      return el.package_id
    packages_set = Set(get_key)
    packages_list = list(self.table)
    for package in packages_list:
      packages_set.add(package)
    def predicate(p):
      return p.truck == None
    packages_subset = packages_set.filter(predicate)
    return list(packages_subset)
