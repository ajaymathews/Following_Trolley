#import RPi.GPIO as GPIO
import numpy as np
import cv2
import thread
import telegram
import urllib2
from pyzbar.pyzbar import decode
from PIL import Image
#import time
from telegram.ext import Updater, CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

right=0
left=0
fwd=0
rev=0

face_cascade = cv2.CascadeClassifier('C:\\opencv\\build\\etc\\haarcascades\\haarcascade_frontalface_default.xml')
QR_data = ''

##GPIO.setmode(GPIO.BOARD)
##GPIO.setwarnings(False)
##GPIO.setup(40,0)    # Motor 1
##GPIO.setup(38,0)    # Motor 1
##GPIO.setup(36,0)    # Motor 2
##GPIO.setup(32,0)    # Motor 2

def QR_Reader(threadName, delay):
        global QR_data
##    try:
        QR_data=None
        capture = cv2.VideoCapture(1)
        while(1):
            ret, frame = capture.read()
            cv2.imshow('Current', frame)
            frame=cv2.resize(frame, (500,500))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            image = Image.fromarray(gray)
            width, height = image.size
            decode_Data=decode((gray.tobytes(), width, height))
            sta=0
            for Data in decode_Data:
                sta=1
                #print Data
                QR_data=str(Data)
                QR_data=QR_data[QR_data.index('data=')+6:QR_data.index(', type=')-1]
                
                print QR_data
                a =len(QR_data)
                print a
            try:
                if (len(QR_data) == 12):
                    qr_link = " http://ceravis.inbondsolutions.com/searchapp.php?query="+QR_data
                    print qr_link
                    time.sleep(3000)
                    bot.sendMessage(chat_id ="360286019",text = qr_link)
                    return stop
##            GPIO.output(40,0)
##            GPIO.output(38,0)
##            GPIO.output(36,0)
##            GPIO.output(32,0)
                    print"Entered_QR11111"
                    return Start_Check
                    print"Entered_QR"
                    time.sleep(300)
                    
            except:
                pass
            if sta==1:
                del(capture)
                cv2.destroyAllWindows()
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
##    except:
##        print 'Camera Err'
##        

def motor(threadName, delay):
    global ls
    global rot
    global s_run
    while(1):
        
        if(fwd==1):
##            GPIO.output(40,1)
##            GPIO.output(38,0)
##            GPIO.output(36,0)
##            GPIO.output(32,1)
##            s_run=0
##            rot=str(random.randrange(25,30,2))
            #print 'Fwd'
            print''
        elif(rev==1):
##            GPIO.output(40,0)
##            GPIO.output(38,1)
##            GPIO.output(36,1)
##            GPIO.output(32,0)
##            s_run=0
##            rot=str(random.randrange(25,30,2))
            #print 'Rev'
            print''
        elif(right==1):
##            GPIO.output(40,0)
##            GPIO.output(38,1)
##            GPIO.output(36,0)
##            GPIO.output(32,1)
##            s_run=0
##            rot=str(random.randrange(25,30,2))
            #print 'Right'
            print''
        elif(left==1):
##            GPIO.output(40,1)
##            GPIO.output(38,0)
##            GPIO.output(36,1)
##            GPIO.output(32,0)
##            s_run=0
##            rot=str(random.randrange(25,30,2))
            #print 'Left'
            print''
        else:
##            GPIO.output(40,0)
##            GPIO.output(38,0)
##            GPIO.output(36,0)
##            GPIO.output(32,0)
##            s_run=1
##            rot='0'
##            print"hi"
            #print 'stop'
            print''



def start(bot, update):
    #if(user_tele_id==str(update.message.chat_id)):
    update.message.reply_text('Welcome')
    custom_keyboard = [['/Start_Check']]
    
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    print update.message.chat_id
    bot.sendMessage(update.message.chat_id,text="Loading.....",reply_markup=reply_markup)
##    else:
##        update.message.reply_text('Permission Denied')

def Start_Check(bot, update):
    #if(user_tele_id==str(update.message.chat_id)):
    custom_keyboard = [['/Forward'],['/Left','/Stop','/Right'],['/Reverse']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.sendMessage(update.message.chat_id,text="Checking....",reply_markup=reply_markup)
##    else:
##        update.message.reply_text('Permission Denied')

def Forward(bot, update):
    global right
    global left
    global fwd
    global rev
    #if(user_tele_id==str(update.message.chat_id)):
    update.message.reply_text('Moving Fwd')
    fwd=1
    right=left=rev=0
##    else:
##        update.message.reply_text('Permission Denied')   

def Reverse(bot, update):
    global right
    global left
    global fwd
    global rev
##    if(user_tele_id==str(update.message.chat_id)):
    update.message.reply_text('Moving Rev')
    fwd=right=left=0
    rev=1
##    else:
##        update.message.reply_text('Permission Denied')      

def Left(bot, update):
    global right
    global left
    global fwd
    global rev
##    if(user_tele_id==str(update.message.chat_id)):
    update.message.reply_text('Moving Left')
    fwd=right=rev=0
    left=1
##    else:
##        update.message.reply_text('Permission Denied') 
    
    

def Right(bot, update):
    global right
    global left
    global fwd
    global rev
##    if(user_tele_id==str(update.message.chat_id)):
    update.message.reply_text('Moving Right')
    fwd=left=rev=0
    right=1
##    else:
##        update.message.reply_text('Permission Denied')
    
        

def Stop(bot, update):
    global right
    global left
    global fwd
    global rev
##    if(user_tele_id==str(update.message.chat_id)):
    update.message.reply_text('stop')
    fwd=right=left=rev=0
##    else:
##        update.message.reply_text('Permission Denied')
##

bot = telegram.Bot(token='552164920:AAGXddJXlzcD6hfv1p3nssWbGIO27CrwuSg')
updater = Updater('552164920:AAGXddJXlzcD6hfv1p3nssWbGIO27CrwuSg')

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('Stop', Stop))
updater.dispatcher.add_handler(CommandHandler('Forward', Forward))
updater.dispatcher.add_handler(CommandHandler('Reverse', Reverse))
updater.dispatcher.add_handler(CommandHandler('Left', Left))
updater.dispatcher.add_handler(CommandHandler('Right', Right))
updater.dispatcher.add_handler(CommandHandler('Start_Check', Start_Check))


try:    
   thread.start_new_thread(motor, ("Thread-1", 1, ) )
   thread.start_new_thread(QR_Reader, ("Thread-1", 1, ) )
##   thread.start_new_thread(position, ("Thread-1", 1, ) )
##   thread.start_new_thread(sensors, ("Thread-1", 1, ) )
##   thread.start_new_thread(ultra, ("Thread-1", 1, ) )
   updater.start_polling()
   updater.idle()
  
  
except:
   print "Error: unable to start thread"

while 1:
   pass

