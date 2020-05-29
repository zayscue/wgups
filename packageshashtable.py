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
        # look up package's address using the locations hash table
        location = self.locations.search((delivery_address, city, zip_code))
        # construct new package object
        package = Package(package_id, location, deadline,
                          weight, delivery_status)
        # insert into the hash table
        return super().insert(package)

    # search for package by package id
    def search(self, package_id):
        # find using the package id
        package = super().search(package_id)
        return package

    # use set operations to filter the packages in the hash table
    def find(self, predicate):
        # define a get key function for the packages set
        def get_key(el):
            return el.package_id
        # construct a pacakges set instance
        packages_set = Set(get_key)
        # copy all of the elements from the hash table into
        # a list
        table = list(self.table)
        # iterate over the list and any sub lists to copy
        # the pacakge values into the package set
        for bucket in table:
            for package in bucket:
                packages_set.add(package)
        # Apply predicate to set and return result as a list
        return list(packages_set.filter(predicate))
