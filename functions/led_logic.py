import RPi.GPIO as GPIO
import time

from functions import global_variables

GPIO.setwarnings(False)

yellow_led = 23
green_led = 24
blue_led = 25


#setup

GPIO.setmode(GPIO.BCM) #use broadcom pin numbering
GPIO.setup(yellow_led, GPIO.OUT) #set ouput
GPIO.setup(green_led, GPIO.OUT) #set ouput
GPIO.setup(blue_led, GPIO.OUT) #set ouput

GPIO.output(yellow_led, GPIO.LOW)
GPIO.output(green_led, GPIO.LOW)
GPIO.output(blue_led, GPIO.LOW)

# try:
#     
#     GPIO.output(yellow_led, GPIO.HIGH) #turn on led
#     GPIO.output(green_led, GPIO.HIGH) #turn on led
#     GPIO.output(blue_led, GPIO.HIGH) #turn on led
# 
#     time.sleep(5)
#     
# finally:
#     GPIO.output(yellow_led, GPIO.LOW)
#     GPIO.output(green_led, GPIO.LOW)
#     GPIO.output(blue_led, GPIO.LOW)
# 
#     GPIO.cleanup()
#     print('LEds are off')

def gpio_cleanup():
#     GPIO.cleanup()
    
#     yellow_led = 23
#     green_led = 24
#     blue_led = 25
# 
# 
#     #setup
# 
#     GPIO.setmode(GPIO.BCM) #use broadcom pin numbering
#     GPIO.setup(yellow_led, GPIO.OUT) #set ouput
#     GPIO.setup(green_led, GPIO.OUT) #set ouput
#     GPIO.setup(blue_led, GPIO.OUT) #set ouput
#     
#         
    GPIO.output(yellow_led, GPIO.LOW)
    GPIO.output(green_led, GPIO.LOW)
    GPIO.output(blue_led, GPIO.LOW)
    

    
    
def user_connected_led():
#     yellow_led = 23
#     green_led = 24
#     blue_led = 25
# 
# 
#     #setup
# 
#     GPIO.setmode(GPIO.BCM) #use broadcom pin numbering
#     GPIO.setup(yellow_led, GPIO.OUT) #set ouput
#     GPIO.setup(green_led, GPIO.OUT) #set ouput
#     GPIO.setup(blue_led, GPIO.OUT) #set ouput

    
    #make the blue led blinking
    try:
        last_toggle_time = time.time()
        led_status = False
        #get connection status from db
        connection_status = global_variables.connection_status
        
        
        
        
        while connection_status is 1:
            current_time = time.time()
            if current_time - last_toggle_time >=0.5:
                blue_led = 25
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(blue_led, GPIO.OUT)
                led_status = not led_status
                GPIO.output(blue_led, led_status)
                last_toggle_time = current_time
                connection_status = global_variables.connection_status
                
                
    except KeyboardInterrupt:
        pass
    finally:
        blue_led = 25
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(blue_led, GPIO.OUT)
        GPIO.output(blue_led, GPIO.LOW)
        GPIO.cleanup()



def data_download_successfully():
#     yellow_led = 23
    green_led = 24
#     blue_led = 25


    #setup

    GPIO.setmode(GPIO.BCM) #use broadcom pin numbering
#     GPIO.setup(yellow_led, GPIO.OUT) #set ouput
    GPIO.setup(green_led, GPIO.OUT) #set ouput
#     GPIO.setup(blue_led, GPIO.OUT) #set ouput
    #turn the green led on for 3 seconds
    try:
        start_time = time.time()
        GPIO.output(green_led, GPIO.HIGH) #turn on led
        
        while time.time() - start_time <3:
            pass
        
        GPIO.output(green_led, GPIO.LOW)
        
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.output(green_led, GPIO.LOW)
        GPIO.cleanup()
        

def led_sniffer_mode():
    yellow_led = 23
#     green_led = 24
# 
# 
#     #setup
# 
    GPIO.setmode(GPIO.BCM) #use broadcom pin numbering
    GPIO.setup(yellow_led, GPIO.OUT) #set ouput
#     GPIO.setup(green_led, GPIO.OUT) #set ouput
    #yellow_led blink at 1 second rate
    try:
        last_toggle_time = time.time()
        led_status = False
        #get current mode
        current_mode = global_variables.current_mode
        sniffer_mode_condition = global_variables.sniffer_mode_condition
        
        while sniffer_mode_condition is True:
            current_time = time.time()
            if current_time - last_toggle_time >=1:
                led_status = not led_status
                GPIO.output(yellow_led, led_status)
                last_toggle_time = current_time
                sniffer_mode_condition = global_variables.sniffer_mode_condition
                
                
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.output(yellow_led, GPIO.LOW)
        GPIO.cleanup()


def led_test_mode():
    yellow_led = 23
#     green_led = 24
# 
# 
#     #setup
# 
    GPIO.setmode(GPIO.BCM) #use broadcom pin numbering
    GPIO.setup(yellow_led, GPIO.OUT) #set ouput
#     GPIO.setup(green_led, GPIO.OUT) #set ouput
    #yellow_led blink at 2 second rate
    try:
        last_toggle_time = time.time()
        led_status = False
        #get current mode
        current_mode = global_variables.current_mode
        test_mode_condition = global_variables.test_mode_condition

        
        while test_mode_condition is True:
            current_time = time.time()
            if current_time - last_toggle_time >=2:
                yellow_led = 23

                GPIO.setmode(GPIO.BCM) #use broadcom pin numbering
                GPIO.setup(yellow_led, GPIO.OUT) #set ouput
                led_status = not led_status
                GPIO.output(yellow_led, led_status)
                last_toggle_time = current_time
                test_mode_condition = global_variables.test_mode_condition
                
    except KeyboardInterrupt:
        pass
    finally:
        yellow_led = 23

        GPIO.setmode(GPIO.BCM) #use broadcom pin numbering
        GPIO.setup(yellow_led, GPIO.OUT) #set ouput
        GPIO.output(yellow_led, GPIO.LOW)
        GPIO.cleanup()
        

def message_sent():
#     yellow_led = 23
    green_led = 24


    #setup

    GPIO.setmode(GPIO.BCM) #use broadcom pin numbering
#     GPIO.setup(yellow_led, GPIO.OUT) #set ouput
    GPIO.setup(green_led, GPIO.OUT) #set ouput
    #turn the green led on for 0.5 seconds
    try:
        start_time = time.time()
        GPIO.output(green_led, GPIO.HIGH) #turn on led
        
        while time.time() - start_time <0.5:
            pass
        
        GPIO.output(green_led, GPIO.LOW)
        
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.output(green_led, GPIO.LOW)
        GPIO.cleanup()
        
        
def led_monitoring_mode():
    yellow_led = 23
    GPIO.setmode(GPIO.BCM) #use broadcom pin numbering
    GPIO.setup(yellow_led, GPIO.OUT) #set ouput
#     GPIO.setup(green_led, GPIO.OUT) #set ouput
    #yellow_led blink at 5 second rate
    try:
        last_toggle_time = time.time()
        led_status = False
        #get current mode
        current_mode = global_variables.current_mode
        monitoring_mode_condition = global_variables.monitoring_mode_condtition

        
        while monitoring_mode_condition is True:
            current_time = time.time()
            if current_time - last_toggle_time >=5:
                yellow_led = 23
                GPIO.setmode(GPIO.BCM) #use broadcom pin numbering
                GPIO.setup(yellow_led, GPIO.OUT) #set ouput
                led_status = not led_status
                GPIO.output(yellow_led, led_status)
                last_toggle_time = current_time
                monitoring_mode_condition = global_variables.monitoring_mode_condtition
                
    except KeyboardInterrupt:
        pass
    finally:
        yellow_led = 23
        GPIO.setmode(GPIO.BCM) #use broadcom pin numbering
        GPIO.setup(yellow_led, GPIO.OUT) #set ouput
        GPIO.output(yellow_led, GPIO.LOW)
        GPIO.cleanup()
        