class QElement(object):
  def __init__(self, element, priority):
    super().__init__()
    self.element = element
    self.priority = priority

class PriorityQueue(object):
  def __init__(self):
    super().__init__()
    self.items = []

  def is_empty(self):
    return len(self.items) == 0
  
  def enqueue(self, element, priority):
    q_element = QElement(element, priority)
    contain = False

    for i in range(0, len(self.items)):
      if self.items[i].priority <= q_element.priority:
        self.items.insert(i, q_element)
        contain = True
        break
    
    if contain == False:
      self.items.append(q_element)
  

  def dequeue(self):
    if self.is_empty():
      return 'Underflow'
    return self.items.pop(0).element

  def front(self):
    if self.is_empty():
      return 'No elements in Queue'
    return self.items[0].element
  
  def rear(self):
    if self.is_empty():
      return 'No elements in Queue'
    return self.items[len(self.items) - 1].element
