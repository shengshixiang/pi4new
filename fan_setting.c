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
unsigned char i2c_write_data(unsigned int slave_addr,unsigned char reg_addr_H,unsigned char reg_addr_L,unsigned char val)
{
	
	int ret=-1;
	unsigned char buf[3];
	buf[0]=reg_addr_H;               /*寄存器的地址*/
	buf[1]=reg_addr_L;
	buf[2]=val;
	struct i2c_rdwr_ioctl_data i2c_write_emc2301;
	struct i2c_msg msg[1]={
		[0]={
			.addr = slave_addr,
			.flags = 0,             /*write*/
			.buf = buf,
			.len = sizeof(buf)
		},		
	};
	i2c_write_emc2301.msgs = msg;
	i2c_write_emc2301.nmsgs = 1;
	
	ret = ioctl(fd,I2C_RDWR,&i2c_write_emc2301);
	if(ret<0)
	{
		perror("write function error\n");
		return ret;
	}
	return val;
}
//器件地址2fH，寄存器地址 30H（fan-setting）,寄存器数值0--255
int main(int argc,char **argv)
{
	
	unsigned char value,index;
	unsigned char speed;
	sscanf(argv[1],"%d",&speed);
	fd = open("/dev/i2c-1",I2C_RDWR);
	if(fd<0)
	{
		printf("open error\n");
		return fd;
	}
	i2c_write_data(0x50,0x00,0x00,speed);      /*写入转速值*/
 	printf("write speed value: %d\n",speed);
	//value=i2c_read_data(0x2f,0x30);       /*读取转速值*/
/* 	if(value < 0)
		printf("Error during I2C_RDWR ioctl with error code: %d\n", value);
	else
		printf("read speed val: %d\n",  value); */ 
    close(fd);
}
