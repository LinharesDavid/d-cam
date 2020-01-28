import RPi.GPIO as GPIO
import time
import sys

HORIZONTAL="HORIZONTAL"
VERTICAL="VERTICAL"

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setwarnings(False)

ajoutAngle = 5

def getEnv():
    file = open(".env", "r") 
    content = file.readlines()
    file.close()
    return content

def setEnv(content, angle_type, coef):
    currentAngle = getAngle(angle_type)

    file = open(".env", "w") 
    for line in content :
        if angle_type + "_ANGLE" in line:
            file.write(angle_type + "_ANGLE=" + str(currentAngle + (30 * coef)) + "\n")
        else :
            file.write(line)
    file.close()

def getAngle(angle_type):
    content = getEnv()

    if (angle_type == HORIZONTAL):    
        return int(content[4].split("=")[1])
    
    return int(content[5].split("=")[1])

def movHorizontally(coef): 
    currentAngle = getAngle(HORIZONTAL)
    if (currentAngle == 0 and coef == -1):
        return

    if (currentAngle == 180 and coef == 1):
        return

    pwm=GPIO.PWM(17,100)
    pwm.start(5)
    angleChoisi = (currentAngle + (30 * coef))/10 + ajoutAngle
    pwm.ChangeDutyCycle(angleChoisi)
    time.sleep(0.3)
    GPIO.cleanup()
    setEnv(getEnv(), HORIZONTAL, coef)

def movVertically(coef): 
    currentAngle = getAngle(VERTICAL)
    if (currentAngle == 0 and coef == -1):
        return

    if (currentAngle == 180 and coef == 1):
        return

    pwm=GPIO.PWM(27,100)
    pwm.start(5)
    angleChoisi = (currentAngle + (30 * coef))/10 + ajoutAngle
    pwm.ChangeDutyCycle(angleChoisi)
    time.sleep(0.3)
    GPIO.cleanup()
    setEnv(getEnv(), VERTICAL, coef)


if len(sys.argv) < 2 :
    exit() 

direction = sys.argv[1]

if direction == "UP" :
    movVertically(1)
if direction == "DOWN" :
    movVertically(-1)

if direction == "LEFT" :
    movHorizontally(-1)

if direction == "RIGHT" :
    movHorizontally(1)

exit()
