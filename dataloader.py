# Zackery Ayscue 000901676
import csv
import json

class DataLoader(object):
  def __init__(self):
    super().__init__()

  # read each line of the csv file, parse into list of float values, and append to list
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


  # read each line of the csv file, parse into dictionary of key value pairs, and append to list
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

  # read each line of the csv file, parse into dictionary of key value pairs, and append to list
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

