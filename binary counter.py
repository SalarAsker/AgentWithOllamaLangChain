
from machine import Pin, ADC
import utime

# Four binary LEDs
leds = [
    Pin(2, Pin.OUT),
    Pin(3, Pin.OUT),
    Pin(4, Pin.OUT),
    Pin(5, Pin.OUT)
]

# One button: Start / Pause
button = Pin(10, Pin.IN, Pin.PULL_UP)

# Potentiometer
speed_control = ADC(26)

# Counter state
counter = 0
running = False


# Display binary number

def display_binary(number):

    binary = ""

    for bit in range(3, -1, -1):

        value = (number >> bit) & 1

        leds[bit].value(value)

        binary += str(value)

    print("Decimal:", number, "| Binary:", binary)



# Button detection with debounce
def button_pressed():

    if button.value() == 0:

        utime.sleep_ms(30)

        if button.value() == 0:

            while button.value() == 0:
                utime.sleep_ms(5)

            return True

    return False


# Adjustable speed
def get_interval():

    value = speed_control.read_u16()

    return 1000 - (value * 900 // 65535)


# Initial state
display_binary(counter)

print("BINARY COUNTER READY")
print("Press button to START / PAUSE")


# Main program
last_tick = utime.ticks_ms()

while True:

    # Start / Pause
    if button_pressed():

        running = not running

        print("RUNNING" if running else "PAUSED")

        last_tick = utime.ticks_ms()


    # Automatic counting
    if running:

        current_time = utime.ticks_ms()

        interval = get_interval()

        if utime.ticks_diff(
            current_time, last_tick
        ) >= interval:

            counter = (counter + 1) % 16

            display_binary(counter)

            last_tick = current_time

    utime.sleep_ms(5)
    
    
    
    
    
    
