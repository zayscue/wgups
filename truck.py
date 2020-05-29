# Zackery Ayscue 000901676

from set import Set
from mytime import Time
from deliverystatus import IN_ROUTE, DELIVERED

# Calculate route using the nearest neighbor
# greedy algorithm
def caculate_route(graph, start_loc, locations):
    # create a new list with the starting location
    # in the first position
    route = [start_loc]
    # create a variable that represents the current
    # location and assign it the value of the
    # starting location
    current_loc = start_loc
    # using a while loop continue to iterate
    # until their are no more locations in
    # locations list parameter
    while len(locations) > 0:
        # This variable will hold the nearest location
        nearest = None
        # This variable will hold the shortest distance from
        # the current location
        nearest_dist = None
        # This variable holds the index value of the nearest
        # location so it can easily be removed from the
        # locations list
        nearest_loc_index = 0
        # This index value just holds the position information
        # of the nested loop
        index = 0
        # Loop over the rest of the locations in the
        # list in order to find a the nearest neighbor
        for loc in locations:
            u = current_loc.graph_index
            v = loc.graph_index
            dist = graph.get_distance(u, v)
            # if the nearest distance has yet to be defined
            # or the nearest dist is greater than the new dist
            # set the following variables to keep track of
            # current nearest neighbor
            if nearest_dist == None or nearest_dist > dist:
                nearest_dist = dist
                nearest = loc
                nearest_loc_index = index
            index += 1
        # Remove the nearest neighbor from the locations list
        # and append to the route
        route.append(locations.pop(nearest_loc_index))
        # change the current location to the nearest neighbor
        # so the process can repeat again
        current_loc = nearest
    # Because the trucks need to return the starting point
    # append the starting location to the end of the route
    route.append(start_loc)

    # Use the new route to caculate the overall cost or distance traveled.
    last_stop = None
    cost = 0.0
    for stop in route:
        if last_stop == None:
            last_stop = stop
            continue
        cost = round(
            cost + graph.get_distance(last_stop.graph_index, stop.graph_index), 2)
        last_stop = stop
    return (route, cost)


class Truck(object):
    def __init__(self, id, graph, start_loc, avg_mph=18.0, max_cap=16):
        super().__init__()
        self.id = id
        self.graph = graph
        self.avg_mph = avg_mph
        self.max_cap = max_cap
        self.packages = []
        self.start_loc = start_loc
        self.current_loc = start_loc
        self.loc_set = Set(lambda l: (l.street, l.city, l.zip_code))
        self.route = []
        self.route_cost = 0.0
        self.traveled = 0.0
        self.current_time = None

    # Load a package onto the truck.  Return True if successful and False if not
    def load(self, package):
        # Check to make sure the truck and handle another
        # package
        if len(self.packages) == self.max_cap:
            return False
        # Add package to the list of packages
        self.packages.append(package)
        # Try to add the packages delivery address to the
        # location set.
        if self.loc_set.add(package.delivery_address) != False:
            # If a new location was added to the set then
            # recalculate the route using nearest neighbor
            result = caculate_route(
                self.graph, self.start_loc, list(self.loc_set))
            # record the results
            self.route = result[0]
            self.route_cost = result[1]
        return True

    # Check if truck is full
    def is_full(self):
        return len(self.packages) == self.max_cap

    # Leave the hub and start deliverying the packages on the truck.
    def leave_hub(self, time):
        # set the current time for the truck to be
        # when it first leaves the hub
        self.current_time = Time(time)
        # Loop through the packages list and update
        # the status of each package
        for package in self.packages:
            package.left_hub_at = Time(time)
            package.delivery_status = IN_ROUTE
        # Print a message indicating to the user the truck is leaving
        print('Truck {} is leaving at {}'.format(self.id, time))
        # Loop through the route calculating the total time and distance
        # spent and printing it out to the user
        for i in range(1, len(self.route)):
            curr = self.route[i - 1]
            next = self.route[i]
            distance = self.graph.get_distance(
                curr.graph_index, next.graph_index)
            minutes = (distance/self.avg_mph) * 60.0
            print('Traveling from {} -> {}, it is {} miles away and should take {} minutes'.format(
                curr.name, next.name, distance, minutes))
            self.current_loc = next
            self.traveled = round(self.traveled + distance, 2)
            self.current_time.add_minutes(minutes)
            # At every stop loop through the list of packages and if the package's
            # delivery address matches record the current time and set the status
            # to DELIVERED
            for package in self.packages:
                if self.current_loc == package.delivery_address:
                    package.delivered_at = Time(
                        self.current_time.hours, self.current_time.minutes)
                    package.delivery_status = DELIVERED
                    deadline = package.deadline
                    if deadline != '':
                        deadline = ', the deadline was {}'.format(deadline)
                    print('Package {} was delivered to {} at {}{}'.format(
                        package.package_id, package.delivery_address, package.delivered_at, deadline))
        print('Total Distance: {} miles'.format(self.traveled))
        print('Final time: {}'.format(self.current_time))
        print()
