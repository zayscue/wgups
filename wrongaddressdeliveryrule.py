from deliveryrule import DeliveryRule

class WrongAddressDeliveryRule(DeliveryRule):
  def __init__(self, description, package_id, corrected_at,
              new_street_address, new_city, new_state, 
              new_zip_code):
    self.description = description
    self.package_id = package_id
    self.corrected_at = corrected_at
    self.new_street_address = new_street_address
    self.new_city = new_city
    self.new_state = new_state
    self.new_zip_code = new_zip_code
    self.type = 'WRONG_ADDRESS'

