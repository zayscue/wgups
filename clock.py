class Clock:
  def __init__(self, hours, minutes):
    self.hours = hours
    self.minutes = minutes

  def add_minutes(self, minutes):
    combined_minutes = self.minutes + minutes
    if (combined_minutes >= 60):
      hours = (combined_minutes//60)
      self.hours += hours
      combined_minutes = (combined_minutes - (hours * 60))
    self.minutes = combined_minutes

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