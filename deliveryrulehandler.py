class DeliveryRuleHandler(object):

  def __init__(self, trucks_dict, package_hash_table):
    super().__init__()
    self.trucks_dict = trucks_dict
    self.package_hash_table = package_hash_table

  def handle(self, delivery_rule):
    delivery_rule_type = delivery_rule.type
    if delivery_rule_type == 'REQUIRED_TRUCK':
      truck_id = delivery_rule.truck_id
      truck = self.trucks_dict[truck_id]
      package_id = delivery_rule.package_id
      package = package_hash_table.search(package_id)
      if package.deadline == '':
        truck.add_package(package)
      else:
        truck.add_priority_package(package)
    elif delivery_rule_type == 'DELAYED':