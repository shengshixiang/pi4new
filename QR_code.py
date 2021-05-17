import cv2
import pyzbar.pyzbar as pyzbar
import time
import _thread
Led_status=0
#'/home/pi/.local/lib/python3.7/site-packages/pyzbar/pyzbar.py'
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
 
def write_eeprom():
    print(write_eeprom)
    
    
def leds_on():
    print(leds_on)
    
    
def leds_off():
    print(leds_off)   
    
    
def leds_blink():
    print(leds_blink)  

    
def led_control_function(threadName, delay):
    global Led_status
    while(1):
        time.sleep(delay) 
        if(Led_status==1): #led on
            print("Led-on")
        elif(Led_status==0): #led off   
            print("led off")  
        elif(Led_status==2): #led blink 
            print("led blink")     
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
        ret, frame = camera.read()
        # 转为灰度图像
        try: 
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except:
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
                print(eeprom_value)
                break
    camera.release()
    cv2.destroyAllWindows()
if __name__ == '__main__':
    try:
        _thread.start_new_thread(led_control_function, ("Thread-led-control", 0.5, ))
    except:
        print("Error: 无法启动线程")
        exit
    #设置led为长灭
    #检测和等待识别出设备
    detect()
    time.sleep(3)  
    #识别成功，设置led为常亮
   
    
