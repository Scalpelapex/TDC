from ctypes import *

track = CDLL(./track_PID.so)
pwm_num=c_int(30)
P_num=c_float(0.15)

if __name__ == '__main__':
    track.track_p(pwm_num,P_num)