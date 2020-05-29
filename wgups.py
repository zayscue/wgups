# Zackery Ayscue 000901676

from mytime import Time
from packageshashtable import PackagesHashTable
from completegraph import CompleteGraph
from truck import Truck
from priorityqueue import PriorityQueue


class WGUPS(object):
    def __init__(self, distances, locations, packages):
        super().__init__()
        self.packages = packages

        hub = locations.search(
            ('4001 South 700 East', 'Salt Lake City', '84107'))

        # construct the three truck instances
        truck_one = Truck('1', distances, hub)
        truck_two = Truck('2', distances, hub)
        truck_three = Truck('3', distances, hub)
        self.trucks = {
            '1': truck_one,
            '2': truck_two,
            '3': truck_three
        }
        # based on specific rules map certain packages to certain trucks
        self.package_map = {
            '1': ['13', '14', '15', '16', '19', '20'],
            '2': ['3', '18', '36', '38', '6', '25', '28', '32'],
            '3': ['9']
        }

    # start running the algorithm
    def run(self):

        # load package in the static map
        for key in self.package_map.keys():
            truck = self.trucks[key]
            packages_ids = self.package_map[key]
            for package_id in packages_ids:
                package = self.packages.search(package_id)
                if truck.load(package) == True:
                    package.truck = truck

        # find all of the packages that have not been loaded
        # on a truck yet and enqueue them in a self adjusting
        # priority queue
        packages = self.packages.find(lambda p: p.truck == None)
        loading_queue = PriorityQueue()
        for package in packages:
            if package.deadline == '9:00 AM':
                loading_queue.enqueue(package, 3)
            elif package.deadline == '10:30 AM':
                loading_queue.enqueue(package, 2)
            else:
                loading_queue.enqueue(package, 1)

        # prioritize loading truck one but afterwards just
        # round robin the rest of the packages into
        # truck two and truck three
        turns = 1
        while loading_queue.is_empty() == False:
            next = loading_queue.dequeue()
            if self.trucks['1'].is_full() == False:
                self.trucks['1'].load(next)
            else:
                truck_id = '{}'.format((turns % 2) + 2)
                self.trucks[truck_id].load(next)
                turns += 1

        # Run trucks
        self.trucks['1'].leave_hub('8:00 AM')
        self.trucks['2'].leave_hub('9:05 AM')
        self.trucks['3'].leave_hub('10:20 AM')

        print('Total miles traveled {}'.format(round(
            self.trucks['1'].traveled + self.trucks['2'].traveled + self.trucks['3'].traveled, 2)))

        # prompt user for input to query the results
        while True:
            query = input(
                'Enter time in HH:MM AM/PM format to query package statuses at a certain time: ')
            query_time = Time(query)
            self.print_package_statuses(query_time)

    # print package statuses at certain times
    def print_package_statuses(self, time):
        # load up a list of packages
        ls = []
        for i in range(0, len(self.packages.table)):
            for j in range(0, len(self.packages.table[i])):
                ls.append(self.packages.table[i][j])
        # define a get key function for the sort function
        def get_key(p):
            return int(p.package_id)

        # sort packages by the package id
        packages = sorted(ls, key=get_key)
        # loop through and print package statuses based on event time stamps
        for package in packages:
            if package.left_hub_at > time:
                print('At {} package {} was {}'.format(
                    time, package.package_id, 'AT HUB'))
            elif package.left_hub_at <= time and package.delivered_at > time:
                print('At {} package {} was {}'.format(
                    time, package.package_id, 'IN TRANSIT'))
            else:
                print('At {} package {} was {}'.format(
                    time, package.package_id, 'DELIVERED'))
