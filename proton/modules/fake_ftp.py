class Ftp_connection():
  def __init__(self, ip='192.168.0.101', port=21, timeout=0):
    self.files = []
    
  def send(self, path, output_file):
      self.files.append((path, output_file))
      return True


  def delete(self, file):
    for i in range(len(self.files)):
      if self.files[i][1] == file:
        self.files.pop(i)
