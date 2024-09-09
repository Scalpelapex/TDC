import serial
import binascii
#import RPI.GPIO as GPIO
import time
import RPi.GPIO as GPIO


#global usart_rx_sta ##数据暂存
usart_rx_sta=[2,0,0]
    
    #def ser_init(self):
ser=serial.Serial("/dev/ttyAMA0",9600,timeout=0.5) #使用树莓派的GPIO口连接串行口

GPIO.setwarnings(False)

################################
#读取数据函数
#主机发送0x57
#传感器返回三个数据，主机进行读取
#返回一个turple（正负号，数值）
################################
def Data_read():  #返回值（正负号，数值）
    global usart_rx_sta
    if ser.isOpen() == False:
        ser.open()
    d=bytes.fromhex('57')
    ser.write(d)  ##这里需要改动，因为这并不是发送的16进制数据(已改)
    time.sleep(0.015)
    count = ser.inWaiting()
    if count != 0:
        for i in range(3):       
            time.sleep(0.001)
            data_r = str(binascii.b2a_hex(ser.read(1)))[2:-1]
            temp=int(data_r,16)
            usart_rx_sta[i]=temp     # 这儿怎么写需要测试 测试内容见草纸
            #Num += 1
    
        signal_0=int(usart_rx_sta[0])
        data_1=int(usart_rx_sta[1])
        data_2=int(usart_rx_sta[2])
        Receive=(data_1<<8)|data_2
    
        ser.flushInput()
        usart_rx_sta = [0,0,0]
        ser.close()
        return (signal_0,Receive)

#def motor_init() :
# 定义两个6612驱动模块的两个个PWM引脚
pin1,pin2,AIN1_L,AIN2_L,BIN1_L,BIN2_L,AIN2_R,AIN1_R,BIN2_R,BIN1_R= 12,16,17,4,27,22,6,5,13,9
#pin2 = 16
#AIN1_L = 17
#AIN2_L = 4
#BIN1_L = 27
#BIN2_L = 22
#AIN1_R = 6
#AIN2_R = 5
#BIN1_R = 13
#BIN2_R = 9
# 设置GPIO口为BCM编号规范
GPIO.setmode(GPIO.BCM)

    # 设置GPIO口为输出
GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)
GPIO.setup(AIN1_L, GPIO.OUT)
GPIO.setup(AIN2_L, GPIO.OUT)
GPIO.setup(BIN1_L, GPIO.OUT)
GPIO.setup(BIN2_L, GPIO.OUT)
GPIO.setup(AIN1_R, GPIO.OUT)
GPIO.setup(AIN2_R, GPIO.OUT)
GPIO.setup(BIN1_R, GPIO.OUT)
GPIO.setup(BIN2_R, GPIO.OUT)


    # 设置PWM波,频率为500Hz
pwm1 = GPIO.PWM(pin1, 100)    ####打算只用两个，和电路一样，左侧两个pwm短接
pwm2 = GPIO.PWM(pin2, 100)


    # pwm波控制初始化
pwm1.start(0)
pwm2.start(0)

#motor_init()   #初始化电机

def stop():
    GPIO.output(AIN1_L,GPIO.LOW)   #左上（正转）
    GPIO.output(AIN2_L,GPIO.LOW)
    GPIO.output(BIN1_L,GPIO.LOW)   #左下（正转）
    GPIO.output(BIN2_L,GPIO.LOW)
    time.sleep(0.01)
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0)

def t_stop(t_time=0):
        pwm1.ChangeDutyCycle(0)
        GPIO.output(AIN2_L,False)#AIN2
        GPIO.output(AIN1_L,False) #AIN1
        GPIO.output(BIN2_L,False)#BIN2
        GPIO.output(BIN1_L,False) #BIN1

        R_Motor.ChangeDutyCycle(0)
        GPIO.output(BIN2_R,False)#BIN2
        GPIO.output(BIN1_R,False) #BIN1
        GPIO.output(AIN2_R,False)#AIN2
        GPIO.output(AIN1_R,False) #AIN1
        time.sleep(t_time)
    

#========================================================================
#// 函数: motor(char PWMA, char PWMB)
#// 描述: 左右电机速度控制
#// 参数: PWMA, 左电机PWM，取值范围-100至100
#//      PWMB, 右电机PWM，取值范围-100至100
#// 返回: none.
#//========================================================================
def motor_control(PWMA, PWMB):    ##   A：左电机    B： 右电机
      # 改变PWM占空比（百分制）
    time.sleep(0.001)
    if (PWMA > 0):
        GPIO.output(AIN1_L,GPIO.HIGH)   #左上（正转）
        #time.sleep(0.0001)
        GPIO.output(AIN2_L,GPIO.LOW)
        #time.sleep(0.0001)
        GPIO.output(BIN1_L,GPIO.HIGH)   #左下（正转）
        #time.sleep(0.0001)
        GPIO.output(BIN2_L,GPIO.LOW)
        time.sleep(0.001)
        pwm1.ChangeDutyCycle(abs(PWMA))
    elif (PWMA < 0):
        GPIO.output(AIN1_L,GPIO.LOW)   ##左上（倒转）
        #time.sleep(0.0001)
        GPIO.output(AIN2_L,GPIO.HIGH)
        #time.sleep(0.0001)
        GPIO.output(BIN1_L,GPIO.LOW)   ##左下（倒转）
        #time.sleep(0.0001)
        GPIO.output(BIN2_L,GPIO.HIGH)           
        time.sleep(0.001)
        pwm1.ChangeDutyCycle(abs(PWMA))
    elif (PWMA == 0) :
        pwm1.ChangeDutyCycle(PWMA)
    
    if PWMB > 0 :   
        GPIO.output(AIN1_R,GPIO.HIGH)   ##右上（正转）
        #time.sleep(0.0001)
        GPIO.output(AIN2_R,GPIO.LOW)
        #time.sleep(0.0001)
        GPIO.output(BIN1_R,GPIO.HIGH)   ##右下（正转）
        #time.sleep(0.0001)
        GPIO.output(BIN2_R,GPIO.LOW)    
        time.sleep(0.001)
        pwm2.ChangeDutyCycle(PWMB)  # 改变PWM占空比
    elif PWMB < 0 :
        GPIO.output(AIN1_R,GPIO.LOW)   ##右上（倒转）
        #time.sleep(0.0001)
        GPIO.output(AIN2_R,GPIO.HIGH)
        #time.sleep(0.0001)
        GPIO.output(BIN1_R,GPIO.LOW)   ##右下（倒转）
        time.sleep(0.001)
        GPIO.output(BIN2_R,GPIO.HIGH)
        pwm2.ChangeDutyCycle(abs(PWMB)) 
    elif PWMB == 0 :
        pwm2.ChangeDutyCycle(0)



def track_PID(pwm,P):
    if not hasattr(track_PID,'Integral_error'):
        track_PID.Integral_error=0
    if not hasattr(track_PID,'Last_error'):
        track_PID.Last_error=0
    if not hasattr(track_PID,'L_Pwm'):
        track_PID.L_Pwm=0
    if not hasattr(track_PID,'R_Pwm'):
        track_PID.R_Pwm=0
    
    P=float(P)
    temp_data = [0,0]       ##数据缓存区
    error = 0               ##偏差值
    I,D=0,0                 ##积分系数，微分系数
    
    temp_data = Data_read()
    if temp_data[0]==0 :
        error = -temp_data[1]
    elif temp_data[0]==1 :
        error = temp_data[1]
    error=error
    #print('error:',error)
    track_PID.Integral_error += error
    
    #print(track_PID.Integral_error)
    
    track_PID.R_Pwm = (pwm-(error*P+track_PID.Integral_error*I+(error-track_PID.Last_error)*D));
    track_PID.L_Pwm = (pwm+(error*P+track_PID.Integral_error*I+(error-track_PID.Last_error)*D));
    #print('error:',error,'last error:',track_PID.Last_error)
    track_PID.Last_error = error;
   
    if pwm > 0 :
        if track_PID.L_Pwm > (pwm+10) :
            track_PID.L_Pwm = (pwm+10)
        if track_PID.R_Pwm > (pwm+10) :
            track_PID.R_Pwm = (pwm+10)
        if track_PID.L_Pwm <= 15 :
            track_PID.L_Pwm = 15
        if track_PID.R_Pwm <= 15 :
            track_PID.R_Pwm = 15
    print(track_PID.L_Pwm,track_PID.R_Pwm)
    #motor_control(track_PID.L_Pwm,track_PID.R_Pwm)
    motor_control(track_PID.L_Pwm,track_PID.R_Pwm)

#while True:
    #track_PID(50,0.1)
if __name__ == '__main__' :
    track_PID(50,0.1)
    time.sleep(3)
    stop()
    #t_stop()