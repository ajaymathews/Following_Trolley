import RPi.GPIO as GPIO
import time
import lcd as l
import serial
import thread
import zbar #sudo apt-get install zbar-tools,sudo apt-get install python-zbar,sudo apt-get install libzbar0
from PIL import Image #pip install Pillow
import cv2

dis = 0
qr_Data = ''
rfid_Data=''
# Ultrasonic Pin  Def
trigger_pin = 10
echo_pin = 8
GPIO.setup(trigger_pin,0)
GPIO.setup(echo_pin,1)

# Motor Init
r1 = 40
r2 = 38
l1 = 36
l2 = 32

GPIO.setup(l1, 0) 
GPIO.setup(l2, 0)
GPIO.setup(r1, 0) 
GPIO.setup(r2, 0)

l.lcd_init()


rfid_Raw = serial.Serial(port = "/dev/ttyUSB0",baudrate = 9600,timeout = 1)
capture = cv2.VideoCapture(0)

def send_trigger_pulse():
    GPIO.output(trigger_pin, True)
    time.sleep(0.0001)
    GPIO.output(trigger_pin, False)
def wait_for_echo(value, timeout):
    count = timeout
    while GPIO.input(echo_pin) != value and count > 0:
        count = count - 1

def get_distance():
    send_trigger_pulse()
    wait_for_echo(True, 10000)
    start = time.time()
    wait_for_echo(False, 10000)
    finish = time.time()
    pulse_len = finish - start
    distance_cm = pulse_len / 0.000058
    distance_in = distance_cm / 2.5
    return (distance_cm)

def qr_Reader():
    global qr_Data
    while(1):
        # To quit this program press q.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Breaks down the video into frames
        ret, frame = capture.read()

        # Displays the current frame
##        cv2.imshow('Current', frame)

        # Converts image to grayscale.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Uses PIL to convert the grayscale image into a ndary array that ZBar can understand.
        image = Image.fromarray(gray)
        width, height = image.size
        zbar_image = zbar.Image(width, height, 'Y800', image.tostring())

        # Scans the zbar image.
        scanner = zbar.ImageScanner()
        scanner.scan(zbar_image)

        #print zbar_image

        # Prints data from image.
        for decoded in zbar_image:

            qr_Data = decoded.data
            print(decoded.data)
        
def measure_Distance():
    global dis
    while(1):
        dis = get_distance()

def front():
    GPIO.output(l1, 0)
    GPIO.output(l2, 1)
    GPIO.output(r1, 0)
    GPIO.output(r2, 1)

def stop():
    GPIO.output(l1, 0)
    GPIO.output(l2, 0)
    GPIO.output(r1, 0)
    GPIO.output(r2, 0)
try:
    thread.start_new_thread(measure_Distance,())
    thread.start_new_thread(qr_Reader,())
except:
    print("Err starting thread")
while(1):
    global qr_Data
    print dis
    print(qr_Data)
    front()
    if(dis <= 10):
##        print("low dis")
        stop()
        l.lcd_string("Scan RFID",1,1)
        while(1):
            rfid_data = rfid_Raw.read(13)
##            print(rfid_data)
            l.lcd_string(str(qr_Data),2,1)
            if(str(rfid_data) == "45003C1DD0B4"):#fixed id for the customer
##                print("Found")
##                while(1):
                l.lcd_string(str(rfid_data),1,1)
            
            if (dis > 10):
                front()
                break
        

        
    pass

