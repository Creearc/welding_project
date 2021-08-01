# Модуль крыльчатки
import sys
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


class Rotator:
  def __init__(self, STEP_PIN=21, DIR_PIN=20, ENABLE_PIN=16):

    ### Пины
    # Шаговый двигатель
    self.STEP_PIN = STEP_PIN
    self.DIR_PIN = DIR_PIN
    self.ENABLE_PIN = ENABLE_PIN
    GPIO.setup(self.STEP_PIN, GPIO.OUT)
    GPIO.setup(self.DIR_PIN, GPIO.OUT)
    GPIO.setup(self.ENABLE_PIN, GPIO.OUT)

    ### Переменные
    # Шаговый двигатель
    self.delay = 0.01
    self.left = True

  def change_dir(self):
    self.left = not self.left
    if self.left:
      GPIO.output(self.DIR_PIN, GPIO.LOW)
    else:
      GPIO.output(self.DIR_PIN, GPIO.HIGH)
  
  # Вращение крыльчатки
  def rotate(self, steps=0):
    print('rotation')
    GPIO.output(self.DIR_PIN, GPIO.LOW)
    if self.left:
      GPIO.output(self.DIR_PIN, GPIO.LOW)
    else:
      GPIO.output(self.DIR_PIN, GPIO.HIGH)

    for i in range(steps):
      GPIO.output(self.STEP_PIN, GPIO.HIGH)
      time.sleep(self.delay)
      GPIO.output(self.STEP_PIN, GPIO.LOW)
      time.sleep(self.delay)


if __name__ == '__main__':
  try:
    r = Rotator()
    while True:
      time.sleep(1.0)
      r.rotate(30)
  except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()

