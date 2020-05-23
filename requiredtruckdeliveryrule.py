from deliveryrule import DeliveryRule

class RequiredTruckDeliveryRule(DeliveryRule):
  def __init__(self, description, package_id, truck_id):
    self.description = description
    self.package_id = package_id
    self.truck_id = truck_id
    self.type = 'REQUIRED_TRUCK'
