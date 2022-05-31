from ftplib import FTP

class Ftp_connection():
  def __init__(self, ip='192.168.0.101', port=21):
    self.ftp = FTP()
    self.ftp.connect(ip, port)
    self.ftp.login(user='', passwd='', timeout=2)
    
  def send(self, file_path, output_file):
##    try:
      print(file_path)
      with open(file_path, 'rb') as f:
        self.ftp.storbinary('STOR ' + output_file, f, 1024)
      return True
##    except:
##      return False

  def delete(self, file):
    self.ftp.delete(file)
