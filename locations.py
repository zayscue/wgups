from linearprobinghashtable import LinearProbingHashTable
from location import Location


class Locations:
    def __init__(self):
      self.locations = LinearProbingHashTable(40)
