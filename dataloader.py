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

    # Open file
    with open(file, newline='', encoding='utf-8-sig') as distances_file:
      # Construct reader object
      reader = csv.reader(distances_file)
      # read each line in the file
      for row in reader:
        # map the string distance values into floating point number and
        # add them to a list which in turn is added to another list
        distances_row_data_list = list(map(convert_to_float, list(row)))
        distances_data.append(distances_row_data_list)
    return distances_data


  # read each line of the csv file, parse into dictionary of key value pairs, and append to list
  def load_locations_csv(self, file):
    locations_data = []
    row_index = 0
    # Open file
    with open(file, newline='', encoding='utf-8-sig') as locations_file:
      # construct reader object
      reader = csv.reader(locations_file)
      # read each line of the file
      for row in reader:
        # parse into a dictionary for easy data access later
        location_data = {
          'index': row_index,
          'name': row[0].strip(),
          'street': row[1].strip(),
          'city': row[2].strip(),
          'state': row[3].strip(),
          'zip_code': row[4].strip()
        }
        # append to list
        locations_data.append(location_data)
        row_index += 1
    return locations_data

  # read each line of the csv file, parse into dictionary of key value pairs, and append to list
  def load_packages_csv(self, file):
    packages_data = []
    # Open file
    with open(file, newline='', encoding='utf-8-sig') as packages_file:
      # create a reader object
      reader = csv.reader(packages_file)
      # read each line of the file
      for row in reader:
        # parse into a dictionary for easy data access later
        package_data = {
          'package_id': row[0].strip(),
          'delivery_address': row[1].strip(),
          'city': row[2].strip(),
          'zip_code': row[4].strip(),
          'weight': row[5].strip(),
          'deadline': row[6].strip()
        }
        # append to list
        packages_data.append(package_data)
    return packages_data

