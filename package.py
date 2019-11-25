class Package:
    def __init__(self, id, delivery_location, deadline, weight, special_notes = None):
        self.id = id
        self.delivery_location = delivery_location
        self.deadline = deadline
        self.weight = weight
        self.special_notes = special_notes
    
    def __hash__(self):
        return self.id