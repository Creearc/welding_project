import sys
import os

#filename.replace('.ls', '_cut.ls')

def cut_file(filename_path, output_file_path):
  f = open(filename_path, 'r')
  fw = open(output_file_path, 'w')
  for s in f:
    #if not('Arc Start' in s or 'Arc End' in s or 'CALL' in s):
    if not('CALL' in s):
      fw.write(s)
  f.close()
  fw.close()



path = []
if len(sys.argv) > 1:
  path = sys.argv[1]
else:
  path ='out_test_2_0.ls'

if os.path.isdir(path):
  otput_folder = path.split('\\')
  first = '\\'.join(otput_folder[:-1])
  last = '{}_cut'.format(otput_folder[-1])
  otput_folder  = '\\'.join([first, last])

  if not os.path.isdir(otput_folder):
    os.mkdir(otput_folder)

  for f in os.listdir(path):
    filename_path = '{}/{}'.format(path, f)
    output_file_path = '{}/{}'.format(otput_folder, f.replace('.ls', '_cut.ls'))
    cut_file(filename_path, output_file_path)
  
else:
  filename_path = path
  output_file_path =  path.replace('.ls', '_cut.ls')
  cut_file(filename_path, output_file_path)
