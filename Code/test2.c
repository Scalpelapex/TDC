#include <stdio.h>
#include <wiringPi.h>
#include <wiringSerial.h>
//#include <unistd.h>
//size_t read(int fd,void * buf ,size_t count);
int main()
{
	int fd,signal,Receive_Date;
	unsigned char num,i;
	char USART[3]={0};
	if(wiringPiSetup()<0)
		return 1;
	if((fd=serialOpen("/dev/ttyAMA0",9600))<0)
		return 1;
	printf("serial test start ...\n");
	serialPutchar(fd,0x57);
	num = serialDataAvail (fd);
	printf("serial num = %d",num);
	if (num>0)
	{
		for(i=0;i<3;i++)
		{
			USART[i]=serialGetchar (fd);
		}

		//read(fd,USART,3);
		signal = USART[0];
		Receive_Date = USART[1];
   	 	Receive_Date <<= 8;
    	Receive_Date |= USART[2];

		serialFlush(fd);
		serialClose(fd);
		printf("signal = %d \n Receive Date = %d \n",signal,Receive_Date);
		return 0;

	}
	
}
