from deliveryrule import DeliveryRule

class DelayedDeliveryRule(DeliveryRule):
  def __init__(self, description, package_id, delayed_until):
    self.description = description
    self.package_id = package_id
    self.delayed_until = delayed_until
    self.type = 'DELAYED'