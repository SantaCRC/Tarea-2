import argparse
import time
import threading
import RPi.GPIO as gpio
gpio.setmode(gpio.BOARD)
gpio.setup(12, gpio.IN, pull_up_down=gpio.PUD_DOWN)

parser=argparse.ArgumentParser()
parser.add_argument("tamano",type=int)
tamano=parser.parse_args().tamano
suma_t=0

def loop(tamano):
    suma=0
    for i in range(0,tamano):
        suma+=i
        time.sleep(0.1)
    return suma

def loop_potencias(n,x):
    suma=0
    for i in range(n,x):
        suma+=i**2
        time.sleep(0.1)
    return suma

def helper(n,x):
    global suma_t
    suma_t=loop_potencias(n,x)+suma_t


def recorido1(tamano):
    return loop(tamano)


def recorido2(tamano):
    threads=[]
    for i in range(0,4):
        inicio=int((tamano*i)/(4))
        fin=int((tamano*(i+1))/(4))
        threads.append(threading.Thread(target=helper,args=(inicio,fin)))
    threads[0].start()
    threads[1].start()
    threads[2].start()
    threads[3].start()
    threads[0].join()
    threads[1].join()
    threads[2].join()
    threads[3].join()
    return suma_t

while True:
    if gpio.input(12):
        inicio=time.time()
        valor = recorido2(tamano+1)
        print("Tiempo de ejecucion threading: {} con suma {} ".format(time.time()-inicio,valor))
        inicio=time.time()
        valor=recorido1(tamano+1)
        print("Tiempo de ejecucion normal: {} con suma {} ".format(time.time()-inicio,valor))

    
        


