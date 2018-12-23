from Adafruit_PWM_Servo_Driver import PWM
import time

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
pwm = PWM(0x40, debug=False)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096


def setServoPulse(channel, pulse):
    pulseLength = 1000000.0                   # 1,000,000 us per second
    pulseLength /= 50.0                       # 60 Hz
    print "%d us per period" % pulseLength
    pulseLength /= 4096.0                     # 12 bits of resolution
    print "%d us per bit" % pulseLength
    pulse *= 1000.0
    pulse /= (pulseLength * 1.0)
# pwmV=int(pluse)
    print "pluse: %f  " % (pulse)
    pwm.setPWM(channel, 0, int(pulse))


# Angle to PWM
def write(servonum, x):
    y = x / 90.0 + 0.5
    y = max(y, 0.5)
    y = min(y, 2.5)
    setServoPulse(servonum, y)


pwm.setPWMFreq(50)                        # Set frequency to 60 Hz
# pwm.setPWM(0,0,153)


def main():
    while True:
        write(0, 150)
        time.sleep(1)
        write(0, 120)
        time.sleep(1)
        write(0, 90)
        time.sleep(1)
    # while (True):
        # Change speed of continuous servo on channel O
    #  setServoPulse(0, 2)
    #  time.sleep(3)
    #  setServoPulse(0, servoMax)
    #  time.sleep(3000)

if __name__ == '__main__':
    main()