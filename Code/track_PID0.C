#include <stdio.h>
#include <wiringSerial.h>
#include <wiringPi.h>
#include <iostream>
#include <softPwm.h>
#include "track_PID.h"
#include <time.h>
#include <stdlib.h>

char USART_RX_STA[3] = { 0 };       //接收状态标记	
unsigned int temp_data[2] = { 0 };       //数据缓存区
//unsigned char Num = 0;              //接收数据的当前位置
//int fd=serialOpen("/dev/ttyAMA0",9600);
unsigned char pin1 = 12 , pin2=16 , AIN1_L=17 , AIN2_L=4 , BIN1_L=27 , BIN2_L=22 , AIN2_R=6 , AIN1_R=5 , BIN2_R=13 , BIN1_R=9;
//bit busy = 0;				//串口状态标记位：1：忙		0：闲

//using namespace std;


int Data_read(void)  //返回2维数组，第一个值为正负号、第二个值为偏移量
{
    int fd,Receive_Date;
	unsigned char num,i;
		if(wiringPiSetup()<0)
            printf("serial open error");
            exit(-1);
		if((fd=serialOpen("/dev/ttyAMA0",9600))<0)
			printf("serial open error");
            exit(-1);
		printf("serial test start ...\n");
		serialPutchar(fd,0x57);
		delay(15);
		num = serialDataAvail (fd);
		printf("serial num = %d\n",num);
		if (num>0)
		{
			for(i=0;i<3;i++)
			{
				delay(2);
				USART_RX_STA[i]=serialGetchar (fd);
			}

			//read(fd,USART,3);
			temp_data[0] = USART_RX_STA[0];
			Receive_Date = USART_RX_STA[1];
			Receive_Date <<= 8;
			Receive_Date |= USART_RX_STA[2];
			temp_data[1]=Receive_Date;

			serialFlush(fd);
			serialClose(fd);
			printf("signal = %d \n Receive Date = %d \n",temp_data[0],temp_data[1]);

		}
}

void setup_BCM(void)
{
    if(-1==wiringPiSetupGpio())
    {
        printf("setup error\n");
	//cerr<<"setup error\n";
        exit(-1);
    }
    pinMode(pin1,OUTPUT);
    pinMode(pin2,OUTPUT);
    pinMode(AIN1_L,OUTPUT);
    pinMode(AIN2_L,OUTPUT);
    pinMode(BIN1_L,OUTPUT);
    pinMode(BIN2_L,OUTPUT);
    pinMode(AIN2_R,OUTPUT);
    pinMode(AIN1_R,OUTPUT);
    pinMode(BIN2_R,OUTPUT);
    pinMode(BIN1_R,OUTPUT);
}

void motor_contol(int PWMA,int PWMB) //A:左电机   B：右电机
{
    int A,B;
    setup_BCM();
    A=softPwmCreate (pin1, 0, 100);
    B=softPwmCreate (pin2, 0, 100);
    if(A==0 && B==0)
    {
        if(PWMA>0)
        {
            softPwmWrite (pin1, PWMA);      //left-up    +
            digitalWrite (AIN1_L,HIGH);
            digitalWrite (AIN2_L,LOW);
            digitalWrite (BIN1_L,HIGH);      //left-down  +
            digitalWrite (BIN2_L,LOW);
            delay(1);
        }
        else if(PWMA<0)
        {
            softPwmWrite (pin1, PWMA);      //left-up    -
            digitalWrite (AIN1_L,LOW);
            digitalWrite (AIN2_L,HIGH);
            digitalWrite (BIN1_L,LOW);      //left-down  -
            digitalWrite (BIN2_L,HIGH);
            delay(1);
        }
        else
        {
            softPwmWrite (pin1,0);
        }
///////////////////////////////////////////////////////////////
        if(PWMB>0)
        {
            softPwmWrite (pin2, PWMB);      //left-up    +
            digitalWrite (AIN1_R,HIGH);
            digitalWrite (AIN2_R,LOW);
            digitalWrite (BIN1_R,HIGH);      //left-down  +
            digitalWrite (BIN2_R,LOW);
            delay(1);
        }
        else if(PWMB<0)
        {
            softPwmWrite (pin2, PWMB);      //left-up    -
            digitalWrite (AIN1_R,LOW);
            digitalWrite (AIN2_R,HIGH);
            digitalWrite (BIN1_R,LOW);      //left-down  -
            digitalWrite (BIN2_R,HIGH);
            delay(1);
        }
        else
        {
            softPwmWrite (pin2,0);
        }
        
    }
}

void track_PID(int pwm,float P)
{
    static float Integral_error,Last_error;
    int error = 0;         //偏差值
    static int L_Pwm,R_Pwm;			 //左右轮速度
    float I = 0,D = 0;		 //积分系数，微分系数
    Data_read();

    if(temp_data[0]==0)
    {
	error = -temp_data[1];
    }
    else
    {
	error = temp_data[1];
    }
	printf("\n error: %d \n ",error);
    Integral_error += error;
	
    R_Pwm = (pwm-(error*P+Integral_error*I+(error-Last_error)*D));
    L_Pwm = (pwm+(error*P+Integral_error*I+(error-Last_error)*D));
	
    Last_error = error;
	
    if(pwm > 0)
    {
	if(L_Pwm > (pwm+10))
		L_Pwm = (pwm+10);
	if(R_Pwm > (pwm+10))
		R_Pwm = (pwm+10);
	if(L_Pwm <= 15)
		L_Pwm = 15;
	if(R_Pwm <= 15)
		R_Pwm = 15;
    }
    printf("R=%d , L=%d \n",R_Pwm,L_Pwm);
    motor_contol(L_Pwm,R_Pwm);
}

void track_p(int pwm,float P)
{
    int begintime,endtime;
    char i=0;
    serial_Init();
    delay(1);
    setup_BCM();
    delay(1);
    begintime=clock();
    while(i<200)
    {
        track_PID(pwm,P);
        delay(1);
        i++;
    }
    endtime=clock();
    printf("runtime: %f \n",(double)(endtime-begintime)/CLOCKS_PER_SEC);
}
int main()
{
    track_p(30,0.15);
    return 0; 
}
