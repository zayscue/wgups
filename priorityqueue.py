class QElement(object):
  def __init__(self, element, priority):
    super().__init__()
    self.element = element
    self.priority = priority

class PriorityQueue(object):
  def __init__(self):
    super().__init__()
    self.items = []

  # Check if the queue is empty
  def is_empty(self):
    return len(self.items) == 0

  # Enqueue new element
  def enqueue(self, element, priority):
    # Construct new queue element with the
    # element object and it's assigned priority
    q_element = QElement(element, priority)
    contain = False

    # Loop through all of the rest of the items in the
    # queue
    for i in range(0, len(self.items)):
      # If an item is found to have lower or equal priority
      # level insert the new element in it's position and
      # shift the rest of items one position back
      # and break out of the loop
      if self.items[i].priority <= q_element.priority:
        self.items.insert(i, q_element)
        contain = True
        break
    # If the new element has lower priority then everything
    # else in the list append it to the back
    if contain == False:
      self.items.append(q_element)

  # Pop the element from the front of the queue off and return it
  def dequeue(self):
    if self.is_empty():
      return 'Underflow'
    return self.items.pop(0).element

  # Peek at what element is at the front of the queue
  def front(self):
    if self.is_empty():
      return 'No elements in Queue'
    return self.items[0].element

  # Peek at what element is at the back of the queue
  def rear(self):
    if self.is_empty():
      return 'No elements in Queue'
    return self.items[len(self.items) - 1].element
