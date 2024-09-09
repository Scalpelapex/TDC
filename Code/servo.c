#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
 
#include <wiringPi.h>
#include <softPwm.h>
 
#define RANGE	   	200 //1 means 100 us , 200 means 20 ms 1等于100微妙，200等于20毫秒 
#define D1 23
 
 
void servo(angle)
{
  
  int i;
  int degree;
  if( !(angle>=0 && angle<=180))
  {  
    printf("degree is between 0 and 180\n");  
    exit(0);  
  }
  degree=5+angle/180.0*20.0;
  
  delay(1000);
  for (i = 0 ; i < degree ; i++)
  {
	softPwmWrite(D1,degree);//再次复写pwm输出
	delay(20);
    softPwmWrite(D1,0);
    delay(40)
  }
  //softPwmWrite (D1, 15) ;
  //exit(0);
 
}

int main()
{
    int begintime,endtime;
    wiringPiSetupGpio();  //wiringpi初始化
    softPwmCreate (D1, 15, RANGE) ;  //创建一个使舵机转到90的pwm输出信号
    servo(150);
    begintime=clock();
    delay(3000);
    endtime=clock();
    printf("runtime = %d",(double)(endtime-begintime)/CLOCKS_PER_SEC);
    servo(30);
    exit(0);
}