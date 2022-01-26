import pygame
import sys
from pycomm3 import CIPDriver, Services, ClassCode, INT, Array, USINT, DINT, UDINT, SINT, UINT, ULINT

robot = '192.168.0.101'

def read_register(plc, number):
    response = plc.generic_message(
            service=b"\x0E", # single
            class_code= b"\x6B",
            instance=1,
            attribute=number,
            connected=False
        )
    if response:
        return 1, response.value
    else:
        return 0, response.error

def write_register(plc, number, data):
    plc._cfg['cip_path'] = b''
    response = plc.generic_message(
            service=b"\x10", # single
            class_code= b"\x6B",
            instance=1,
            attribute=number,
            request_data=DINT.encode(data),
            connected=False
        )
    if response:
        return 1, response.value
    else:
        return 0, response.error
 
FPS = 60
W = 500  # ширина экрана
H = 300  # высота экрана
WHITE = (255, 255, 255)
BLUE = (0, 70, 225)
 
sc = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
 
# координаты и радиус круга
X = 300 // 2
Y = H // 2
X1 = 400
Z = Y
step0 = 50
speed0 = 5
step1 = 50
speed1 = 5
r = 50

run = True
while run:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        run = False
    
  x0, y0, dx0, dy0 = X, Y, 0, 0
  x1, y1, d1 = X1, Z, 0
  
  keys = pygame.key.get_pressed()
  if keys[pygame.K_LEFT]:
    dx0 = -1
  elif keys[pygame.K_RIGHT]:
    dx0 = 1
  if keys[pygame.K_UP]:
    dy0 = -1
  elif keys[pygame.K_DOWN]:
    dy0 = 1
  if keys[pygame.K_SPACE]:
    d1 = -1
  elif keys[pygame.K_LCTRL]:
    d1 = 1

  x0 += dx0 * step0
  y0 += dy0 * step0
  y1 += d1 * step1

  with CIPDriver(robot) as plc:
    write_register(plc, 101, speed0*dx0)
    write_register(plc, 102, speed0*dy0)
    write_register(plc, 103, -speed1*d1)

    rx = read_register(plc, 111)[1]
    ry = read_register(plc, 112)[1]
    rz = read_register(plc, 113)[1]

    print('X={}, Y={}, Z={}'.format(rx, ry, rz))

  sc.fill(WHITE)
  pygame.draw.line(sc, (0, 0, 0), [X, Y-step0-r], [X, Y+step0+r], 3)
  pygame.draw.line(sc, (0, 0, 0), [X-step0-r, Y], [X+step0+r, Y], 3)
  pygame.draw.line(sc, (0, 0, 0), [X1, Y-step0-r], [X1, Y+step0+r], 3)
  
  pygame.draw.circle(sc, BLUE, (x0, y0), r)
  pygame.draw.circle(sc, BLUE, (x1, y1), r)
  pygame.display.update()
  
  clock.tick(FPS)
pygame.quit()
