import requests
import threading

SERVER_IP = 'http://192.168.0.101/MD/CURPOS.DG'

pages = {'positions' : 'http://192.168.0.101/MD/CURPOS.DG',
         'safety_signals' : 'http://192.168.0.101/MD/SFTYSIG.DG',
         'current_program_states' : 'http://192.168.0.101/MD/PRGSTATE.DG'}

def ask(url):
  url = '{}'.format(url)
  response = requests.get(url=url)
  out = response.content
  return out


for key in pages.keys(): 
  print(ask(pages[key]))
  print()
