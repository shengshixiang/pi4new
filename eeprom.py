import smbus
import time
bus = smbus.SMBus(1)
for i in range(0,256):
    bus.write_byte_date(0x50,i,i)
    time.sleep(0,1)
for i in range(0,256):
    bus.read_byte_date(0x50,i)
    print('{0:3}'.format(rbuf),end=' ')
    if((i+1)%16==0 and i!=0):
        print("\t")
    