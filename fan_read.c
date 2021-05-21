#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <linux/input.h>
#include <linux/i2c.h>
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>
int fd;													/*定义文件句柄*/
unsigned char i2c_read_data(unsigned int slave_addr,unsigned char reg_addr) //读取预设风扇转速
{
	unsigned char data;                                   /*定义转速保存变量*/
	int ret=-1;                                          /*定义返回值*/
	struct i2c_rdwr_ioctl_data i2c_read_emc2301;          /*定义i2cadapter传输结构体*/
	struct i2c_msg msg[2]={
		[0]={
			.addr = slave_addr,                          /*从机器件的地址*/
			.flags = 0,                                   /*write*/
			.buf = &reg_addr,                            /*寄存器的地址*/
			.len = sizeof(reg_addr)                
		},
		[1]={
			.addr = slave_addr,                       /*从机器件的地址*/
			.flags = 1,									 /*read*/
			.buf = &data,
			.len = sizeof(data)
		},
		
	};
	i2c_read_emc2301.msgs = msg;                         /*填充数据结构体*/
	i2c_read_emc2301.nmsgs = 2;                         
	
	ret = ioctl(fd,I2C_RDWR,&i2c_read_emc2301);
	if(ret<0)
	{
		perror("read function error\n");
		return ret;
	}
	return data;
}
//器件地址2fH，寄存器地址 30H（fan-setting）,寄存器数值0--255
int main(int argc,char **argv)
{
	unsigned char value,index;
	fd = open("/dev/i2c-10",I2C_RDWR);
	if(fd<0)
	{
		printf("open error\n");
		return fd;
	}
	value=i2c_read_data(0x2f,0x30);       /*读取转速值*/
	if(value < 0)
		printf("fan_read Error during I2C_RDWR ioctl with error code: %d\n", value);
	else
		printf("%d",  value);
    close(fd);
}
