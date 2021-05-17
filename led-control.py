import time
# file = open("/sys/bus/platform/devices/leds/leds/led0/brightness",'w')
# file.write("1")
# file.flush()
# time.sleep(2)
# file.write("0")
# file.flush()
# time.sleep(2)
# file.close()

file = open("/sys/bus/platform/devices/leds/leds/led0/trigger",'w')
file.write("none")
file.flush()
file.close()

# file = open("/sys/bus/platform/devices/leds/leds/led0/brightness",'w')
# file.write("0")
# file.close()