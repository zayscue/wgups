class Package:
    def __init__(self, package_id, delivery_address, deadline, city, zip_code, weight, delivery_status):
        self.package_id = package_id
        self.delivery_address = delivery_address
        self.deadline = deadline
        self.city = city
        self.zip_code = zip_code
        self.weight = weight
        self.delivery_status = delivery_status
    
    def __hash__(self):
        return hash(self.package_id)
    
    def __eq__(self, key):
        return self.package_id == key