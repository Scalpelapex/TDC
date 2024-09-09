import RPi.GPIO as GPIO
import time
import atexit
import signal_num_control as gl
atexit.register(GPIO.cleanup)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
Pink = 24
freq = 50                          # 存放PWM频率变量
dc = 2.5                           # 存放PWM占空比变量，这里初始值为0，可以根据实际需要修改

GPIO.setup(Pink, GPIO.OUT)        # 将GPIO19设置为输出模式

pwmdj = GPIO.PWM(Pink, freq)        # 创建PWM对象，并指定初始频率

#angle_now=75
#gl.set_value('angle_now',100)

pwmdj.start(gl.get_value0('angle_now'))                       # 启动PWM1，并指定初始占空比



def servo(angle,speed=3):
    #global angle_now
    angle_now0=gl.get_value('angle_now')
    if (angle>=0):
        for i in range(angle_now0,angle_now0+angle+1,speed):
            pwmdj.ChangeDutyCycle(2.5+ 10 * i / 180) #设置转动角度
            time.sleep(0.02)                      #等该20ms周期结束
            pwmdj.ChangeDutyCycle(0)                  #归零信号
            time.sleep(0.1)         #转动间隔时间
    #angle_now=angle_end
    if (angle<0):
        for i in range(angle_now0,angle_now0+angle,-speed):   #fanzhuan
            pwmdj.ChangeDutyCycle(2.5 + 10 * i / 180)
            time.sleep(0.02)
            pwmdj.ChangeDutyCycle(0)
            time.sleep(0.1)
    #pwm1.stop()
    #angle_now=angle_now+angle
    gl.set_value('angle_now',angle_now0+angle)
    print('angle_now=',angle_now0)
def duoji_init():
    time.sleep(1)
    pwmdj.ChangeDutyCycle(7.5)
    #servo(0)
    time.sleep(1)

def duoji_main(setpoint,point):
    #dd=int((Idle_PID_Calc(setpoint,point))*20.0/640.0)
    dd = point-setpoint
    print("chushihua:",dd)
    #print
    if dd>0 :
        servo(10)
    else :
        servo(-10)
    #else :
        #servo(dd)
        
if __name__ == '__main__':
    #servo(45)
    #servo(-45)
    
    pass
    