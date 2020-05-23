from deliveryrule import DeliveryRule

class DeliveredTogetherDeliveryRule(DeliveryRule):
  def __init__(self, description, package_id, delivered_with):
    self.description = description
    self.package_id = package_id
    self.delivered_with = delivered_with
    self.type = 'DELIVERED_TOGETHER'