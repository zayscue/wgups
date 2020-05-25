# Zackery Ayscue 000901676
class Package:
    def __init__(self, package_id, delivery_address, deadline, weight, delivery_status):
        self.package_id = package_id
        self.delivery_address = delivery_address
        self.deadline = deadline
        self.weight = weight
        self.delivery_status = delivery_status
        self.truck = None

    def __hash__(self):
        return hash(self.package_id)

    def __eq__(self, key):
        return self.package_id == key