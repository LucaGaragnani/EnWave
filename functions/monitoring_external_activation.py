import RPi.GPIO as GPIO
import gpiozero
from gpiozero import Button, LED
from signal import pause
import threading
import time

import global_variables

        
GPIO.setwarnings(False)

stop_event = threading.Event()



def monitoring_activation():
    print('waiting external input')
    button_pin = 17


    #setup
    button = Button(button_pin, pull_up=True)
    yellow_led = 23
    GPIO.setmode(GPIO.BCM) #use broadcom pin numbering
    GPIO.setup(yellow_led, GPIO.OUT) #set ouput
    
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
            
   
    
    def start_thread():

        
        while not stop_event.is_set():
            print('monitoring_started')
            global_variables.monitoring_mode_condtition = True
            led_monitoring_mode()
            
            #add function to read the messages and store in the db
            
                                
            
    def button_pressed():
        print('button pressed')
        stop_event.clear()
        threading.Thread(target=start_thread, daemon = True).start()
        
    def button_released():
        print('button released')
        global_variables.monitoring_mode_condtition = False
        stop_event.set()
        
    button.when_pressed = button_released
    button.when_released = button_pressed
    
    pause()


monitoring_activation()


    