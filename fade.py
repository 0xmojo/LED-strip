#!/usr/bin/env python
import Adafruit_BBIO.PWM as PWM
import time
import threading
import socket

red = "P8_13"
green = "P8_19"
blue  = "P9_14"

HOST = ''
PORT = 12345



def fade(colorA, colorB, ignore_color):
    PWM.set_duty_cycle(ignore_color, 100)
    for i in range(0, 100):
        PWM.set_duty_cycle(colorA, i)
        PWM.set_duty_cycle(colorB, 100 -i)
        time.sleep(0.005)


def set_color(r, g, b):
    PWM.set_duty_cycle(red,r)
    PWM.set_duty_cycle(green,g)
    PWM.set_duty_cycle(blue,b)


#animation thread for runtime
def animation_thread(thread_name):
    t = threading.currentThread()
    print("Starting animation thread: " + thread_name)
    while getattr(t, "do_run", True):   
        fade(green, blue, red)
        time.sleep(1)
        fade(blue, red, green)
        time.sleep(1)
        fade(red, blue, green)
        time.sleep(1)
    print "exeting Thread" 

def normalize(x):
    newval = 0.3921 * float(x)
    if newval > 100.0:
        return 100.0
    elif newval < 0:
        return 0
    else:
        return newval

def choose_color():
    input = raw_input(">>> ").lower().rstrip()
    list = input.split(',')
    
    r = normalize(list[0])
    g = normalize(list[1])
    b = normalize(list[2])

    set_color(r,g,b)

def fade(list):
    print "Fading"
    print list

def network_mode():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print "Connected by", addr
    
    while 1:
        data = conn.recv(1024)
        if not data:
            break
       
        list = data.split(",")
        print list

        if len(list) > 3:
            fade(list)
        else: 
            r = normalize(list[0])
            g = normalize(list[1])
            b = normalize(list[2])
            set_color(r,g,b)

    conn.close()


def main():

    PWM.start(red, 0)
    PWM.start(green, 0)
    PWM.start(blue, 0)

    while True:
        print("\n e = end\n c = continue\n n = network mode")
        choice = raw_input(">>> ").lower().rstrip()
        if choice == "e":
            break
        elif choice == "c":
            print "color"
            choose_color()

        elif choice == "n":
            print "network mode"
            network_mode()
        else:
            print("invalid choice\n")

if __name__ == "__main__":
    main()
