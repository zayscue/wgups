# Zackery Ayscue 000901676

from set import Set
from mytime import Time
from deliverystatus import IN_ROUTE, DELIVERED

# Calculate route using the nearest neighbor
# greedy algorithm
def caculate_route(graph, start_loc, locations):
    route = [start_loc]
    current_loc = start_loc
    while len(locations) > 0:
        nearest = None
        nearest_dist = None
        nearest_loc_index = 0
        index = 0
        for loc in locations:
            u = current_loc.graph_index
            v = loc.graph_index
            dist = graph.get_distance(u, v)
            if nearest_dist == None or nearest_dist > dist:
                nearest_dist = dist
                nearest = loc
                nearest_loc_index = index
            index += 1
        route.append(locations.pop(nearest_loc_index))
        current_loc = nearest
    route.append(start_loc)

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

    def load(self, package):
        if len(self.packages) == self.max_cap:
            return False
        self.packages.append(package)
        if self.loc_set.add(package.delivery_address) != False:
            result = caculate_route(
                self.graph, self.start_loc, list(self.loc_set))
            self.route = result[0]
            self.route_cost = result[1]
        return True

    def is_full(self):
        return len(self.packages) == self.max_cap

    def leave_hub(self, time):
        self.current_time = Time(time)
        for package in self.packages:
            package.left_hub_at = Time(time)
            package.delivery_status = IN_ROUTE
        print('Truck {} is leaving at {}'.format(self.id, time))
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
