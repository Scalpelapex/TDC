# -*- coding: utf-8 -*-
import serial.tools.list_ports
import time
import numpy as np
import signal_num_control as gl
from threading import Lock

ser = serial.Serial('/dev/ttyUSB0',115200)
#ser.port = 'COM3' #设置端口
#ser.baudrate = 115200 #设置雷达的波特率

def getTFLunaData():
    while (gl.get_value('distance_Flag')!=2):
        count = ser.in_waiting #获取接收到的数据长度
        if count>8 :
            recv = ser.read(9)#读取数据并将数据存入recv
            #print('get data from serial port:', recv)
            ser.reset_input_buffer()#清除输入缓冲区
            if recv[0] == 0x59 and recv[1] == 0x59:  # python3
                distance = np.int16(recv[2] + np.int16(recv[3] << 8))
                strength = recv[4] + recv[5] * 256
                #print('distance = %5d  strengh = %5d' % (distance, strength))
                ser.reset_input_buffer()
                Lock.acquire()
                try:
                    if (distance<=50):
                        gl.set_value('distance_Flag',1)
                    elif (distance>50):
                        gl.set_value('distance_Flag',0)
                finally:
                    Lock.release()
                #time.sleep(1)
                #print('distance = %5d  strengh = %5d' % (distance, strength))

            #if recv[0] == 'Y' and recv[1] == 'Y':  # python2 //此处标示出文件读取成功
                #lowD = int(recv[2].encode('hex'), 16)
                #highD = int(recv[3].encode('hex'), 16)
                #lowS = int(recv[4].encode('hex'), 16)
                #highS = int(recv[5].encode('hex'), 16)
                #distance = np.int16(lowD + np.int16(highD << 8))
                #strength = lowS + highS * 256
                #print('distance = %5d  strengh = %5d' % (distance, strength))
        else:
            time.sleep(0.005) #50ms
if __name__ == '__main__':
    try:
        if ser.is_open == False:
            try:
                ser.open()
            except:
                print('Open COM failed!')
        getTFLunaData()
    except KeyboardInterrupt:  # Ctrl+C
        if ser != None:
            ser.close()