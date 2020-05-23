from linearprobinghashtable import LinearProbingHashTable
from package import Package
from deliverystatus import AT_HUB

class PackagesHashTable(LinearProbingHashTable):
  def __init__(self, initial_capacity=40):
    super().__init__(initial_capacity)
  
  def insert(self, package_id, delivery_address, deadline, city, zip_code, weight, delivery_status=AT_HUB):
    package = Package(package_id, delivery_address, deadline, city, zip_code, weight, delivery_status)
    return super().insert(package)
