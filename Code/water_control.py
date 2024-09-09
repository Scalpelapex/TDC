import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
water_con = 21
GPIO.setup(water_con, GPIO.OUT)
def water(num):
    if num == 1:
        GPIO.output(water_con,GPIO.HIGH)
    else :
        GPIO.output(water_con,GPIO.LOW)
        
if __name__ == '__main__':
    water(1)
    time.sleep(2)
    water(0)
    time.sleep(1)