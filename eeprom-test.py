# from smbus import SMBus

# with SMBus(1) as bus:
    # # Write a block of 8 bytes to address 80 from offset 0
    # data = [0x00, 0x00]
    # bus.write_i2c_block_data(50, 0, data)
    
    
# !/usr/bin/python
# -*- coding:utf-8 -*-
import smbus2
import operator
import time
address = 0x50
bus = smbus2.SMBus(1)
string_device_id="700ac82b-4366-11eb-a3f8-00163e123f5"
#string_device_id= "222222222222222222222222222222222222"
def string_division_lists(string):
    device_id_list=list(string)
    first_part_data_list =device_id_list[0:32]
    second_part_data_list=device_id_list[32:]
    return first_part_data_list,second_part_data_list

def char_convert_int(register_addr_list,test_list):
    #print("Original list is: " + str(test_list))
    out_list=test_list
    for i in range(0,len(test_list)):
        out_list[i]=ord(test_list[i])
    result_list=register_addr_list
    result_list.extend(test_list)
    return result_list
def write_eeprom(string_device_id):
    #division data
    data1,data2=string_division_lists(string_device_id)
    data1=char_convert_int([0,0],data1)
    data2=char_convert_int([0,32],data2)
    #write data1 
    msg = smbus2.i2c_msg.write(address,data1)
    bus.i2c_rdwr(msg)
    time.sleep(0.1)
    #write data2
    msg = smbus2.i2c_msg.write(address,data2)
    bus.i2c_rdwr(msg) 
def verify_eeprom(string_device_id):
    #read data from eeprom
    device_id_list=list(string_device_id)
    read_data_list=[]
    write = smbus2.i2c_msg.write(address, [00, 00])
    bus.i2c_rdwr(write)
    for i in range(0,36):
        data=bus.read_byte(address)
        read_data_list.append(chr(data))
        print('%#x'%data)
    
   
   
    #compare data
    print(operator.eq(device_id_list,read_data_list))
    print("verify_eeprom")

verify_eeprom(string_device_id)


# first_part_data_list,second_part_data_list=list_division_lists(data)   
# print("data1"+str(first_part_data_list))
# print("data2"+str(second_part_data_list))
# test_list1=char_to_int([0,0],data)
# address = 0x50
# bus = smbus2.SMBus(1)
# # #write
# msg = smbus2.i2c_msg.write(address,test_list1 )
# bus.i2c_rdwr(msg)
# time.sleep(0.1)
# test_list1=char_to_int([0,32],data2)
# print("Out list is: " + str(test_list1))
# address = 0x50
# bus = smbus2.SMBus(1)
# msg = smbus2.i2c_msg.write(address,test_list1 )
# bus.i2c_rdwr(msg)



#read
# write = smbus2.i2c_msg.write(address, [00, 00])
# bus.i2c_rdwr(write)
# data=bus.read_byte(address)
# print(data)
# data=bus.read_byte(address)
# print(data)
# data=bus.read_byte(address)
# print(data)
# time.sleep(0.1)

# msg = smbus2.i2c_msg.read(address,0)
# bus.i2c_rdwr(msg)
# msg = smbus2.i2c_msg.read(address,0)
# bus.i2c_rdwr(msg)





# data = [0x00,0x03,0x02,0x01]
# bus.write_i2c_block_data(address,0x00,data)