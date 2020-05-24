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

    def __eq__(self, key):
        result = self.street == key[0] and self.city == key[1] and self.zip_code == key[2]
        return result

    def __str__(self):
        return '{}, {}, {} {}'.format(self.street, self.city, self.state, self.zip_code)