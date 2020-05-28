# Zackery Ayscue 000901676
from chaininghashtable import ChainingHashTable
from package import Package
from deliverystatus import AVAILABLE_AT_HUB
from set import Set

class PackagesHashTable(ChainingHashTable):
  def __init__(self, locations, initial_capacity=40):
    self.locations = locations
    super().__init__(initial_capacity)

  # add new package to hash table
  def insert(self, package_id, delivery_address, deadline, city, zip_code, weight, delivery_status=AVAILABLE_AT_HUB):
    location = self.locations.search((delivery_address, city, zip_code))
    package = Package(package_id, location, deadline, weight, delivery_status)
    return super().insert(package)

  # search for package by package id
  def search(self, package_id):
    package = super().search(package_id)
    return package

  # use a set operations to filter the packages in the hash table
  def find(self, predicate):
    def get_key(el):
      return el.package_id
    packages_set = Set(get_key)
    table = list(self.table)
    for bucket in table:
      for package in bucket:
        packages_set.add(package)
    return list(packages_set.filter(predicate))

