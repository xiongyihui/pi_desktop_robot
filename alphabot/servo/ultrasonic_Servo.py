#!/usr/bin/env python
from Adafruit_PWM_Servo_Driver import PWM
import RPi.GPIO as GPIO
import time
import sys

PWMA   = 18
AIN1   = 22
AIN2   = 27

PWMB   = 23
BIN1   = 25
BIN2   = 24

BtnPin  = 19
Gpin    = 5
Rpin    = 6

TRIG = 20
ECHO = 21
# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
pwm = PWM(0x40,debug = False)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

def setServoPulse(channel, pulse):
  pulseLength = 1000000.0                   # 1,000,000 us per second
  pulseLength /= 50.0                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096.0                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000.0
  pulse /= (pulseLength*1.0)
# pwmV=int(pluse)
  print "pluse: %f  " % (pulse)
  pwm.setPWM(channel, 0, int(pulse))

#Angle to PWM
def write(servonum,x):
  y=x/90.0+0.5
  y=max(y,0.5)
  y=min(y,2.5)
  setServoPulse(servonum,y)
  
def t_up(speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,True) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,True) #BIN1
        time.sleep(t_time)
        
def t_stop(t_time):
        L_Motor.ChangeDutyCycle(0)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,False) #AIN1

        R_Motor.ChangeDutyCycle(0)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,False) #BIN1
        time.sleep(t_time)
        
def t_down(speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,True)#AIN2
        GPIO.output(AIN1,False) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,True)#BIN2
        GPIO.output(BIN1,False) #BIN1
        time.sleep(t_time)

def t_left(speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,True)#AIN2
        GPIO.output(AIN1,False) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,True) #BIN1
        time.sleep(t_time)

def t_right(speed,t_time):
        L_Motor.ChangeDutyCycle(speed)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,True) #AIN1

        R_Motor.ChangeDutyCycle(speed)
        GPIO.output(BIN2,True)#BIN2
        GPIO.output(BIN1,False) #BIN1
        time.sleep(t_time)
        
def keysacn():
    val = GPIO.input(BtnPin)
    while GPIO.input(BtnPin) == False:
        val = GPIO.input(BtnPin)
    while GPIO.input(BtnPin) == True:
        time.sleep(0.01)
        val = GPIO.input(BtnPin)
        if val == True:
            GPIO.output(Rpin,1)
            while GPIO.input(BtnPin) == False:
                GPIO.output(Rpin,0)
        else:
            GPIO.output(Rpin,0)
            
def setup():
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)
        
        GPIO.setup(Gpin, GPIO.OUT)     # Set Green Led Pin mode to output
        GPIO.setup(Rpin, GPIO.OUT)     # Set Red Led Pin mode to output
        GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)

        GPIO.setup(AIN2,GPIO.OUT)
        GPIO.setup(AIN1,GPIO.OUT)
        GPIO.setup(PWMA,GPIO.OUT)
        
        GPIO.setup(BIN1,GPIO.OUT)
        GPIO.setup(BIN2,GPIO.OUT)
        GPIO.setup(PWMB,GPIO.OUT)
        pwm.setPWMFreq(50)                        # Set frequency to 60 Hz
        
def distance():
	GPIO.output(TRIG, 0)
	time.sleep(0.000002)

	GPIO.output(TRIG, 1)
	time.sleep(0.00001)
	GPIO.output(TRIG, 0)

	
	while GPIO.input(ECHO) == 0:
		a = 0
	time1 = time.time()
	while GPIO.input(ECHO) == 1:
		a = 1
	time2 = time.time()

	during = time2 - time1
	return during * 340 / 2 * 100

def front_detection():
        write(0,90)
        time.sleep(0.5)
        dis_f = distance()
        return dis_f

def left_detection():
         write(0, 175)
         time.sleep(0.5)
         dis_l = distance()
         return dis_l
        
def right_detection():
        write(0,5)
        time.sleep(0.5)
        dis_r = distance()
        return dis_r
     
def loop():
        while True:
                dis1 = front_detection()
                if (dis1 < 40) == True:
                        t_stop(0.2)
                        t_down(50,0.5)
                        t_stop(0.2)
                        dis2 = left_detection()
                        dis3 = right_detection()
                        if (dis2 < 40) == True and (dis3 < 40) == True:
                                t_left(50,1)
                        elif (dis2 > dis3) == True:
                                t_left(50,0.3)
                                t_stop(0.1)
                        else:
                                t_right(50,0.3)
                                t_stop(0.1)
                else:
                        t_up(60,0)
              #  print dis1, 'cm'
               # print ''

def destroy():
	GPIO.cleanup()

if __name__ == "__main__":
        setup()
        L_Motor= GPIO.PWM(PWMA,100)
        L_Motor.start(0)
        R_Motor = GPIO.PWM(PWMB,100)
        R_Motor.start(0)
        keysacn()
        try:
                loop()
        except KeyboardInterrupt:
                destroy()
