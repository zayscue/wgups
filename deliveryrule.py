class DeliveryRule:
  def __init__(self, description, package_id):
    self.description = description
    self.package_id = package_id
  
  def __hash__(self):
    return hash(self.package_id)

  def __eq__(self, package_id):
    return self.package_id == package_id
