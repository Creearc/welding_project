import time
import os

class Log():
  def __init__(self):
    self.log_path = 'logs'

    if not os.path.isdir(self.log_path):
      os.mkdir(self.log_path)

  def add(self, text):
    tmp = time.ctime().split()
    f = open('{}/{} {} {}.txt'.format(self.log_path, tmp[2], tmp[1], tmp[-1]), 'a')
    f.write('{}:  {}\n'.format(time.ctime(), text))
    f.close()


if __name__ == '__main__':
  l = Log()
  l.add(1)
  l.add('hello')
