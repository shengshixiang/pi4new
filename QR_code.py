import cv2
import pyzbar.pyzbar as pyzbar
import time
import _thread
Led_status=0
import smbus2
import operator
import time
address = 0x50
bus = smbus2.SMBus(1)
string_device_id="700ac82b-4366-11eb-a3f8-00163e123ff5"
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
       # print('%#x'%data)
    #compare data
    result=operator.eq(device_id_list,read_data_list)
    return result
def decodeDisplay(image):
    barcodeData=""
    barcodes = pyzbar.decode(image)
    barcode_num = len(barcodes)
    #print(barcode_num)
    # if(barcode_num == 1):
        # print("barcode_num=1")  
    for barcode in barcodes:
        # 提取条形码的边界框的位置
        # 画出图像中条形码的边界框
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
 
        # 条形码数据为字节对象，所以如果我们想在输出图像上
        # 画出来，就需要先将它转换成字符串
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
 
        # 绘出图像上条形码的数据和条形码类型
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    .5, (0, 0, 125), 2)
 
        # 向终端打印条形码数据和条形码类型
        #print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
    return image,barcodeData,barcode_num    
def led_22(value):
    file = open("/sys/bus/platform/devices/leds/leds/gpio-22/brightness",'w')
    if(value):
        file.write("1")
    else:
        file.write("0")
    file.flush()
    file.close()
def led_26(value):
    file = open("/sys/bus/platform/devices/leds/leds/gpio-26/brightness",'w')
    if(value):
        file.write("1")
    else:
        file.write("0")
    file.flush()
    file.close()
def led_25(value):
    file = open("/sys/bus/platform/devices/leds/leds/gpio-25/brightness",'w')
    if(value):
        file.write("1")
    else:
        file.write("0")
    file.flush()
    file.close()
def led_27(value):
    file = open("/sys/bus/platform/devices/leds/leds/gpio-27/brightness",'w')
    if(value):
        file.write("1")
    else:
        file.write("0")
    file.flush()
    file.close()
def led_17(value):
    file = open("/sys/bus/platform/devices/leds/leds/gpio-17/brightness",'w')
    if(value):
        file.write("1")
    else:
        file.write("0")
    file.flush()
    file.close()
def leds_on():
   led_22(1)
   led_26(1)
   led_25(1)
   led_27(1)
   led_17(1)
def leds_off():
   led_22(0)
   led_26(0)
   led_25(0)
   led_27(0)
   led_17(0)   
def leds_blink():
#    print(leds_blink)
    leds_on()
    time.sleep(0.2)
    leds_off()
    time.sleep(0.2)  
def leds_flow():
     #22 26 25 27 17
    led_22(1)
    led_26(1)  
    led_25(0) 
    led_27(0)
    led_17(0)
    time.sleep(0.2)
    led_22(0)
    led_26(1)  
    led_25(1) 
    led_27(0)
    led_17(0)
    time.sleep(0.2)
    led_22(0)
    led_26(0)  
    led_25(1) 
    led_27(1)
    led_17(0)
    time.sleep(0.2)
    led_22(0)
    led_26(0)  
    led_25(0) 
    led_27(1)
    led_17(1)
    time.sleep(0.2)  
def check_eeprom():
    #读出eeprom的数据
    #判断第8 13 18
    ret=0
    read_data_list=[]
    write = smbus2.i2c_msg.write(address, [00, 00])
    bus.i2c_rdwr(write)
    for i in range(0,36):
        data=bus.read_byte(address)
        read_data_list.append(chr(data))
       # print('%#x'%data)
    #compare data
    print(read_data_list[8])
    print(read_data_list[13])
    print(read_data_list[18])
    if(read_data_list[8]=='-'):
        if(read_data_list[13]=='-'):
            if(read_data_list[18]=='-'):
                ret=1
    return ret
def led_control_function(threadName, delay):
    global Led_status
    while(1):
        time.sleep(delay) 
        if(Led_status==1): #led on
            leds_on()
        elif(Led_status==0): #led off   
            leds_off() 
        elif(Led_status==2): #led blink 
            leds_blink()  
        elif(Led_status==3):
            leds_flow()
def detect():
    global Led_status
    camera = cv2.VideoCapture(0)
    #ret=camera.set(3,320) 
    #ret=camera.set(4,240) 
    #ret=camera.get(3)
    #print(ret)
    #ret=camera.get(4) 
    #print(ret)  
    while True:
        # 读取当前帧
        eeprom_value=[]
        ret, frame = camera.read()
        # 转为灰度图像
        try: 
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except:
            camera.release()
            camera = cv2.VideoCapture(0)
            Led_status=0
            time.sleep(1)     
        else:       
            im,barcodeData,ret=decodeDisplay(gray)
            Led_status=2
            cv2.waitKey(5)#delay 5ms
            cv2.imshow("camera",im)
            if(ret == 1):
                Led_status=1
                eeprom_value=barcodeData[-36:]
                #print(eeprom_value)
                break    
    camera.release()
    #cv2.waitKey(0)
    cv2.destroyAllWindows()
    return eeprom_value
if __name__ == '__main__':
    try:
        _thread.start_new_thread(led_control_function, ("Thread-led-control", 0.5, ))
    except:
        print("Error: 无法启动线程")
        exit
    ret_value=check_eeprom()
    if(ret_value==1):#eeprom中已有数据
        Led_status=3
        camera = cv2.VideoCapture(0)
        ret, frame = camera.read()
        #等待插入摄像头代表想要重新写
        while True:
            ret, frame = camera.read()
            try:
                #print("a2a")
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)          
                #print("aa")
            except:
                camera.release()
                camera = cv2.VideoCapture(0)
                time.sleep(1)   
            else:
                #print("bb")
                break
        camera.release()
               #eeprom中没有数据
    #设置led为长灭
    #检测和等待识别出设备
    device_id_value=detect()
    print(device_id_value)
    write_eeprom(device_id_value)
    time.sleep(0.5)
    result=verify_eeprom(string_device_id)
    if(result):
        print("verify pass")
        Led_status=3
    else:
        print("verify fail")
   # time.sleep(1)
    input()   
    #识别成功，设置led为常亮
   
    
