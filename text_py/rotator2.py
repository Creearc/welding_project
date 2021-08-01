# Модуль крыльчатки
import sys
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


class Rotator:
  def __init__(self, STEP_PIN=21, DIR_PIN=20, ENABLE_PIN=16):
    ### Пины
    self.STEP_PIN = STEP_PIN
    self.DIR_PIN = DIR_PIN
    self.ENABLE_PIN = ENABLE_PIN
    GPIO.setup(self.STEP_PIN, GPIO.OUT)
    GPIO.setup(self.DIR_PIN, GPIO.OUT)
    GPIO.setup(self.ENABLE_PIN, GPIO.OUT)
    self.process = GPIO.PWM(STEP_PIN, 10)

    ### Переменные
    self.frequency = 1000
    self.left = True
    self.is_activate = False

  def change_dir(self):
    self.left = not self.left
    if self.left:
      GPIO.output(self.DIR_PIN, GPIO.LOW)
    else:
      GPIO.output(self.DIR_PIN, GPIO.HIGH)
      
  # Запуск крыльчатки
  def start(self, f=None, l=None):
    print('Запущен двигатель')
    if not (l is None):
      self.left = l
    if not (f is None):
      self.frequency = f
    if self.left:
      GPIO.output(self.DIR_PIN, GPIO.LOW)
    else:
      GPIO.output(self.DIR_PIN, GPIO.HIGH)
    self.process.start(50)
    self.process.ChangeFrequency(self.frequency)
    self.is_activate = True
    

  # Остановка крыльчатки
  def stop(self):
    self.process.stop()
    self.is_activate = False

if __name__ == '__main__':
  try:
    r = Rotator(13, 19, 26)
    while True:
      r.start()
      time.sleep(30.0)
      r.stop()
        
  except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()

