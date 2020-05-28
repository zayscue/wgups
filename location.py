# Zackery Ayscue 000901676
class Location:
    def __init__(self, name, street, city, state, zip_code, graph_index):
        self.name = name
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.graph_index = graph_index

    def __hash__(self):
        return hash((self.street, self.city, self.zip_code))

    def __eq__(self, value):
        if value == None:
            return False
        if isinstance(value, Location) == True:
            return self.street == value.street and self.city == value.city and self.zip_code == value.zip_code
        else:
            return self.street == value[0] and self.city == value[1] and self.zip_code == value[2]

    def __str__(self):
        return '{}, {}, {} {}'.format(self.street, self.city, self.state, self.zip_code)