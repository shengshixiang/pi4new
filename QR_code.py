import cv2
import pyzbar.pyzbar as pyzbar
import time
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
def led_control(led_on_off):
    print("led_on_off:")
    print(led_on_off)
def detect():
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
            time.sleep(1)           
        else:       
            im,barcodeData,ret=decodeDisplay(gray)
            cv2.waitKey(5)#delay 5ms
            cv2.imshow("camera",im)
            if(ret == 1):
                eeprom_value=barcodeData[-36:]
                print(eeprom_value)
                break
    camera.release()
    cv2.destroyAllWindows()
if __name__ == '__main__':
    #设置led为长灭
    led_control(0)
    #检测和等待识别出设备
    detect()
    #识别成功，设置led为常亮
    led_control(1)
    
