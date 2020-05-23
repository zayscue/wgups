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

import csv
import json

# Main program
distances = []

with open('./data/distances.csv', newline='', encoding='utf-8-sig') as distances_file:
  reader = csv.reader(distances_file)
  for row in reader:
    distances_row_list = list(row)
    distances.append(distances_row_list)

locations = []

with open('./data/locations.csv', newline='', encoding='utf-8-sig') as locations_file:
  reader = csv.reader(locations_file)
  for row in reader:
    location_row_tuple = tuple(row)
    location = Location(location_row_tuple[0].strip(), location_row_tuple[1].strip(), location_row_tuple[2].strip(), location_row_tuple[3].strip(), location_row_tuple[4].strip())
    locations.append(location)

locations_hash_table = LinearProbingHashTable(len(locations))

for location in locations:
  locations_hash_table.insert(location)

hub_location = locations_hash_table.search(('4001 South 700 East', 'Salt Lake City', 'UT', '84107'))

# loading delivery rules data from csv file
delivery_rules = []

with open('./data/deliveryrules.csv', newline='', encoding='utf-8-sig') as delivery_rules_file:
  reader = csv.reader(delivery_rules_file)
  for row in reader:
    delivery_rule_tuple = tuple(row)
    description = delivery_rule_tuple[0].strip()
    package_id = delivery_rule_tuple[1].strip()
    type = delivery_rule_tuple[2].strip()
    rule_data = json.loads(delivery_rule_tuple[3])
    if type == 'REQUIRED_TRUCK':
      truck_id = rule_data['truck_id']
      delivery_rules.append(RequiredTruckDeliveryRule(description, package_id, truck_id))
    elif type == 'DELAYED':
      delayed_until = rule_data['delayed_until']
      delivery_rules.append(DelayedDeliveryRule(description, package_id, delayed_until))
    elif type == 'DELIVERED_TOGETHER':
      delivered_with = rule_data['delivered_with']
      delivery_rules.append(DeliveredTogetherDeliveryRule(description, package_id, delivered_with))
    elif type == 'WRONG_ADDRESS':
      corrected_at = rule_data['corrected_at']
      new_street_address = rule_data['new_street_address']
      new_city = rule_data['new_city']
      new_state = rule_data['new_state']
      new_zip_code = rule_data['new_zip_code']
      delivery_rules.append(WrongAddressDeliveryRule(description, package_id, corrected_at, new_street_address, new_city, new_state, new_zip_code))

delivery_rules_dict = {}

for rule in delivery_rules:
  delivery_rules_dict[rule.package_id] = rule
  

# Load package data from csv file

packages = PackagesHashTable()

with open('./data/packages.csv', newline='', encoding='utf-8-sig') as packages_file:
  reader = csv.reader(packages_file)
  for row in reader:
    package_row_tuple = tuple(row)
    package_id = package_row_tuple[0].strip()
    delivery_address = package_row_tuple[1].strip()
    city = package_row_tuple[2].strip()
    zip_code = package_row_tuple[4].strip()
    weight = package_row_tuple[5].strip()
    deadline = package_row_tuple[6].strip()
    packages.insert(package_id, delivery_address, deadline, city, zip_code, weight)

temp = 'hello world'