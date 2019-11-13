class Package:
    def __init__(self, id, street_address, city, zip_code, weight, deadline, status):
        self.id = id
        self.street_address = street_address
        self.city = city
        self.zip_code = zip_code
        self.weight = weight
        self.deadline = deadline
        self.status = status
    
    def __hash__(self):
        return self.id