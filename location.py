class Location:
    def __init__(self, name, street_address, city, state, zip_code):
        self.name = name
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip_code = zip_code
    
    def __hash__(self):
        return hash((self.street_address, self.city, self.zip_code))

    def __eq__(self, key):
        return self.street_address == key[0] and self.city == key[1] and self.zip_code == key[2]