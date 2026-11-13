import machine
from machine import Pin
import time

led = Pin("LED", Pin.OUT)
#led.on()        # Tänd LED
led.off()

ledRed = machine.Pin(15, machine.Pin.OUT)
ledYellow = machine.Pin(14, machine.Pin.OUT)
ledGreen = machine.Pin(13, machine.Pin.OUT)

button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
buzzer = machine.Pin(12, machine.Pin.OUT)

button_pressed = False

def btn_handler(pin):
    global button_pressed
    if not button_pressed:
        button_pressed = True

button.irq(trigger=machine.Pin.IRQ_FALLING, handler=btn_handler)

while True:
    if button_pressed == True:
        ledRed.value(1)
        for i in range(40):
            buzzer.value(1)
            time.sleep(0.05)
            buzzer.value(0)
            time.sleep(0.2)
        button_pressed = False
    ledRed.value(1)
    time.sleep(5)
    ledYellow.value(1)
    time.sleep(2)
    ledRed.value(0)
    ledYellow.value(0)
    ledGreen.value(1)
    time.sleep(8)
    ledGreen.value(0)
    ledYellow.value(1)
    time.sleep(3)
    ledYellow.value(0)
    ledGreen.value(0)

