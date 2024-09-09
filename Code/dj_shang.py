import RPi.GPIO as GPIO
import time
import atexit
atexit.register(GPIO.cleanup)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
Pin10 = 24
freq0 = 50                          # 存放PWM频率变量
dc0 = 2.5                           # 存放PWM占空比变量，这里初始值为0，可以根据实际需要修改

GPIO.setup(Pin10, GPIO.OUT)        # 将GPIO19设置为输出模式

pwm10 = GPIO.PWM(Pin10, freq0)        # 创建PWM对象，并指定初始频率

pwm10.start(dc0)                       # 启动PWM1，并指定初始占空比


def servo1(angle0,angle,speed=1):    
    if (angle0<=angle):
        for i in range(angle0,angle+1,speed):
            pwm10.ChangeDutyCycle(2.5+ 10 * i / 180) #设置转动角度
            print(2.5+10*i/180)
            time.sleep(0.02)                      #等该20ms周期结束
            pwm10.ChangeDutyCycle(0)                  #归零信号
            time.sleep(0.03)         #转动间隔时间
    #angle_now=angle_end
    if (angle0>angle):
        for i in range(angle0,angle,-speed):   #fanzhuan
            pwm10.ChangeDutyCycle(2.5 + 10 * i / 180)
            print(2.5+10*i/180)
            time.sleep(0.02)
            pwm10.ChangeDutyCycle(0)
            time.sleep(0.03)
    #pwm1.stop()
    

def main001():
    pass
        
if __name__ == '__main__':
    pass
    #main1()