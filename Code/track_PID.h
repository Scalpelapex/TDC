#ifndef __TRACK_PID_H__
#define __TRACK_PID_H__

#include <stdio.h>
#include <wiringSerial.h>
#include <wiringPi.h>
#include <softPwm.h>

int wiringPiSetupGpio (void);       //
int serialDataAvail (int fd);       //获取串口缓存中可用的字节数。fd:文件描述符（/dev/ttyAMA0）
int serialGetchar (int fd);        //从串口读取一个字节数据返回
void delay (unsigned int howLong); //延时函数单位ms
void serialFlush (int fd);         //刷新、清除缓存区数据
void serialClose (int fd);         //关闭串口
void serialPrintf (int fd, char *message);
void pinMode (int pin, int mode);
int softPwmCreate (int pin, int initialValue, int pwmRange);
void softPwmWrite (int pin, int value);
void digitalWrite (int pin, int value);


void serial_Init(void);
int *Data_read(void);
void setup_BCM(void);
void motor_contol(int PWMA,int PWMB);
void track_PID(int pwm,float P);
void track_p(int pwm,float P);

#endif