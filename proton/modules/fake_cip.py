
class Fanuc():
  def __init__(self, ip):
    self.r = [[0] for i in range(100)]
    self.s = [0 for i in range(100)]

  def read_r(self, number):
    return 1, self.r[number]

  def write_r(self, number, data):
    self.r[number][0] = data
    return 1, self.r[number]

  def read_sr(self, number):
    return 1, self.s[number]

  def write_sr(self, number, data):
    self.s[number] = data
    return 1, self.s[number]
    
    
    
