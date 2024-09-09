import threading
import time
from TFLite_detection_webcam_function import usb_camera_0
#from track_pid_1 import track_PID,stop
import signal_num_control as gl
from USB_UART_Distance import getTFLunaData
from water_control import water
from dj_shang import main001
from ctypes import *
libtrack = CDLL('./track_PID.so')
pwm_num = c_int(30)
P_num = c_float(0.15)

#class myThread_TFLuna (threading.Thread):  
    #def __init__(self, threadID, name):
        #threading.Thread.__init__(self)
        #self.threadID = threadID
        #self.name = name
        #self.counter = counter
    #def run(self):
        #print ("开始线程：" + self.name)
        #getTFLunaData()
        #print ("退出线程：" + self.name)
class myThread_camera (threading.Thread):  
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        #self.counter = counter
    def run(self):
        print ("开始线程：" + self.name)
        usb_camera_0()
        print ("退出线程：" + self.name)
class myThread_motor (threading.Thread):  
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()       # 设置为True
        self.__running = threading.Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True
        #self.counter = counter
    def run(self):
        print ("开始线程：" + self.name)
        while self.__running.isSet():
            self.__flag.wait()      # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            #track_PID(30,0.15)
            libtrack.track_p(30,0.15)
        print ("退出线程：" + self.name)
    def pause(self):
        self.__flag.clear()     # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()        # 设置为False    

class myThread_TFLuna (threading.Thread):  
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()       # 设置为True
        self.__running = threading.Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True
        #self.counter = counter
    def run(self):
        print ("开始线程：" + self.name)
        while self.__running.isSet():
            self.__flag.wait()      # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            getTFLunaData()
        print ("退出线程：" + self.name)
    def pause(self):
        self.__flag.clear()     # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()        # 设置为False    

#def camera_detection():
   # usb_camera_detection()
def main():
    #设置线程锁：
    lock = threading.Lock()
    
    #创建线程
    thread1_motor = myThread_motor(4, "motor")       #线程1，电机
    thread2_camera = myThread_camera(2, "camera")    #线程2，摄像头
    thread3_TFLuna = myThread_TFLuna(3, "TFLuna")    #线程3，红外测距
  
    #开启线程
    thread1_motor.start()
    thread2_camera.start()
    thread3_TFLuna.start()

    #循环体（判断）
    while True:
        #flag0 = gl.get_value('motor_Flag')
        #flag1 = gl.get_value('distance_Flag')
        #print('flag0_1:',gl.get_value('motor_Flag'))       
        if (gl.get_value('motor_Flag') == 1) and (gl.get_value('distance_Flag') == 1):
            #stop()
            stop()
            time.sleep(0.2)
            thread1_motor.pause()
            thread3_TFLuna.pause()
            #thread1_motor.stop()
            stop()
            stop()
            stop()
            time.sleep(1)
            #servo1(50,30)
            water(1)
            time.sleep(3)
            water(0)
            #servo1(30,50)
            lock.acquire()
            gl.set_value('distance_Flag',2)
            lock.release()

            time.sleep(0.03)
            #print('distance_Flag:',gl.get_value('distance_Flag')) 
        if (gl.get_value('distance_Flag')==2):
            #thread3_TFLuna.stop()
            thread1_motor.resume()
            #time.sleep(5)
            lock.acquire()
            gl.set_value('motor_Flag',0)
            gl.set_value('distance_Flag',0)
            lock.release()
            time.sleep(1)
            thread3_TFLuna.resume()
            time.sleep(2)

            #云台回复
        #else :
            #thread1_motor.resume()
        #if motor_stop_Flag == 1 :
            #thread1_motor.stop()
    print ("退出主线程")
    
if __name__ == '__main__':
    main()