class Time(object):
  def __init__(self, *args):
    super().__init__()
    if len(args) == 1:
      time_str = args[0]
      time_str_parts = time_str.split(':')
      hours = float(time_str_parts[0].strip())
      time_str_parts = time_str_parts[1].split(' ')
      minutes = float(time_str_parts[0].strip())
      meridiem = time_str_parts[1].strip()
      if meridiem.upper() == 'AM':
        if hours == 12:
          self.hours = 0
        else:
          self.hours = hours
        self.minutes = minutes
      else:
        self.hours = hours + 12
        self.minutes = minutes
    elif len(args) == 2:
      self.hours = args[0]
      self.minutes = args[1]
    else:
      print('Unsupported')
  
  def add_minutes(self, minutes):
    combined_minutes = self.minutes + minutes
    if (combined_minutes >= 60):
      hours = (combined_minutes//60)
      self.hours += hours
      combined_minutes = (combined_minutes - (hours * 60))
    self.minutes = combined_minutes

  def __eq__(self, value):
    return self.hours == value.hours and self.minutes == value.minutes
  
  def __ne__(self, value):
    return not self.__eq__(value)

  def __lt__(self, value):
    if self.hours < value.hours:
      return True
    elif self.hours > value.hours:
      return False
    else:
      if self.minutes < value.minutes:
        return True
      else:
        return False
  
  def __le__(self, value):
    if self.hours < value.hours:
      return True
    elif self.hours > value.hours:
      return False
    else:
      if self.minutes <= value.minutes:
        return True
      else:
        return False
  
  def __gt__(self, value):
    if self.hours > value.hours:
      return True
    elif self.hours < value.hours:
      return False
    else:
      if self.minutes > value.minutes:
        return True
      else:
        return False
  
  def __ge__(self, value):
    if self.hours > value.hours:
      return True
    elif self.hours < value.hours:
      return False
    else:
      if self.minutes >= value.minutes:
        return True
      else:
        return False

  def __str__(self):
    meridiem = None
    if self.hours < 12:
      meridiem = 'AM'
    else:
      meridiem = 'PM'
    adjusted_hours = (self.hours % 12)
    if adjusted_hours == 0:
      adjusted_hours += 12
    return '{:02d}:{:02d} {}'.format(int(adjusted_hours), int(self.minutes), meridiem)