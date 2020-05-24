import csv
import json

class DataLoader(object):
  def __init__(self):
    super().__init__()

  def load_distances_csv(self, file):
    distances_data = []

    def convert_to_float(distance_str):
      distance = float(distance_str.strip())
      return distance

    with open(file, newline='', encoding='utf-8-sig') as distances_file:
      reader = csv.reader(distances_file)
      for row in reader:
        distances_row_data_list = list(map(convert_to_float, list(row)))
        distances_data.append(distances_row_data_list)
    return distances_data

  def load_locations_csv(self, file):
    locations_data = []
    row_index = 0
    with open(file, newline='', encoding='utf-8-sig') as locations_file:
      reader = csv.reader(locations_file)
      for row in reader:
        location_data = {
          'index': row_index,
          'name': row[0].strip(),
          'street': row[1].strip(),
          'city': row[2].strip(),
          'state': row[3].strip(),
          'zip_code': row[4].strip()
        }
        locations_data.append(location_data)
        row_index += 1
    return locations_data

  def load_delivery_rules_csv(self, file):
    delivery_rules_data = []
    with open('./data/deliveryrules.csv', newline='', encoding='utf-8-sig') as delivery_rules_file:
      reader = csv.reader(delivery_rules_file)
      for row in reader:
        delivery_rule_data = {
          'description': row[0].strip(),
          'package_id': row[1].strip(),
          'type': row[2].strip(),
          'data': json.loads(row[3].strip())
        }
        delivery_rules_data.append(delivery_rule_data)
    return delivery_rules_data

  def load_packages_csv(self, file):
    packages_data = []
    with open(file, newline='', encoding='utf-8-sig') as packages_file:
      reader = csv.reader(packages_file)
      for row in reader:
        package_data = {
          'package_id': row[0].strip(),
          'delivery_address': row[1].strip(),
          'city': row[2].strip(),
          'zip_code': row[4].strip(),
          'weight': row[5].strip(),
          'deadline': row[6].strip()
        }
        packages_data.append(package_data)
    return packages_data

