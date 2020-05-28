# Zackery Ayscue 000901676
from dataloader import DataLoader
from location import Location
from linearprobinghashtable import LinearProbingHashTable
from packageshashtable import PackagesHashTable
from completegraph import CompleteGraph
from wgups import WGUPS

data_loader = DataLoader()


def create_distances_graph():
    distances_data = data_loader.load_distances_csv('./data/distances.csv')
    graph = CompleteGraph(len(distances_data))
    for i in range(0, len(distances_data)):
        for j in range(0, len(distances_data[i])):
            graph.add_edge(i, j, distances_data[i][j])
    return graph

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


def create_packages_hash_table(locatons):
    packages = PackagesHashTable(locatons)
    packages_data = data_loader.load_packages_csv('./data/packages.csv')
    for element in packages_data:
        package_id = element['package_id']
        delivery_address = element['delivery_address']
        city = element['city']
        zip_code = element['zip_code']
        weight = element['weight']
        deadline = element['deadline']
        packages.insert(package_id, delivery_address, deadline, city, zip_code, weight)
    return packages

# Main program
def main():
    # create data structures
    distances_graph = create_distances_graph()
    locations = create_locations_hash_table()
    packages = create_packages_hash_table(locations)

    wgups = WGUPS(distances_graph, locations, packages)

    wgups.run()

if __name__ == '__main__':
    main()
