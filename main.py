import csv
from location import Location
from linearprobinghashtable import LinearProbingHashTable
from distancesgraph import DistancesGraph
from dataloader import DataLoader
from app import App

data_loader = DataLoader()


def create_distances_graph():
    distances_data = data_loader.load_distances_csv('./data/distances.csv')
    distances_graph = DistancesGraph(distances_data)
    return distances_graph

def create_locations_hash_table():
    locations_data = data_loader.load_locations_csv('./data/locations.csv')
    locations_hash_table = LinearProbingHashTable(len(locations_data))
    for element in locations_data:
        name = element['name']
        street = element['street']
        city = element['city']
        state = element['state']
        zip_code = element['zip_code']
        index = element['index']
        location = Location(name, street, city, state, zip_code, index)
        locations_hash_table.insert(location)
    return locations_hash_table


def add_packages(app):
    packages_data = data_loader.load_packages_csv('./data/packages.csv')
    for element in packages_data:
        package_id = element['package_id']
        delivery_address = element['delivery_address']
        city = element['city']
        zip_code = element['zip_code']
        weight = element['weight']
        deadline = element['deadline']
        app.add_package(package_id, delivery_address, deadline, city, zip_code, weight)

# Main program
def main():
    # create data structures
    distances_graph = create_distances_graph()
    locations_hash_table = create_locations_hash_table()

    app = App(distances_graph, locations_hash_table)

    add_packages(app)

    packages = app.find_packages('1', '195 W Oakland Ave', '10:30 AM', 'Salt Lake City', '84115', '21', 'AVAILABLE_AT_HUB')
    for package in packages:
        print('Found package: {}'.format(package))

    app.run()

if __name__ == '__main__':
    main()
