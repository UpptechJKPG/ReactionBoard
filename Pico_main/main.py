from machine import Pin, Timer
import time

led_internal = Pin("LED", Pin.OUT)
grer_button = Pin(15, Pin.IN, Pin.PULL_UP)# S Pin.PULL_DOWN , Pin.PULL_UP
red_button = Pin(16, Pin.IN, Pin.PULL_UP) # R Pin.PULL_DOWN
is_finished = Pin(18, Pin.IN, Pin.PULL_DOWN)	# E 

score = 0
time_remaining = 60
#is_finished.value(1)
tim = Timer(-1)
timer_debounce = Timer()

time_last = 0
time_current = 0
have_sent_highscore = False

time_last_red = 0
time_current_red = 0

def timer_callback(t):
    global score, time_remaining, have_sent_highscore
#    print(is_finished.value())
    if time_remaining != 0:
        time_remaining -= 1
    if time_remaining == 0: #is_finished.value() == 1
        #is_finished.value(1)
        if have_sent_highscore == False:
            send_data ('-' + str(score), time_remaining)
            have_sent_highscore = True
    send_data (score, time_remaining)

def timer_init():
    tim.init(mode = Timer.PERIODIC, freq = 1000, callback = timer_callback)
    tim.init(period = 1000, callback = timer_callback)

def send_data(score, time_remaining):
    score_string = str(score)
    time_string = str(time_remaining)
    print(score_string + '|' + time_string)
    
def reset_game():
    global score, time_remaining, have_sent_highscore
    time_remaining = 60
    score = 0
    send_data(score, time_remaining)
    have_sent_highscore = False
    timer_init()
    #is_finished.value(0)
    
def grer_button_interrupt(grer_button): #kontaktstuds finns vid släpp av knapp, om knappen håller sig låg / brädet inte ändar knappen så får du cirka 8-9 poäng.....
    global score, time_remaining, time_last, time_current
    grer_button_r = grer_button.value()
    # Get the current time
    time_current = time.ticks_ms()
    # Calculate the time since the last button press
    if time_current >= time_last:
        time_since_last = time_current - time_last
    else:
        # Handle wraparound
        time_since_last = (time_current + (0xFFFFFFFF - time_last)) + 1
        #print("Handled Wraparound")
    # Update the time_last variable
    time_last = time_current
    #print("\33[91mTime since last:", time_since_last, "\033[0m")
    #    
    #print('In the interrupt')
    #print('Grer button buffer:', grer_button_buffer)
    #print('Grer button:', grer_button.value())
    ##print("Time Since last button press", time_since_last, "=",time_last, "-", time_last)
    #print('')

    # Check if the time since the last press is greater than the debounce delay (50ms)
    if time_since_last > 50:
        #print('Inside time loop:')
        #print('Grer button buffer:', grer_button_buffer)
        #print('Grer button:', grer_button.value())
        #print('')
        if time_remaining > 0:# and grer_button_buffer == 1 and grer_button.value() == 0
            #print('Inside and loop')
            #print('Grer button buffer:', grer_button_buffer)
            #print('Grer button:', grer_button.value())

            grer_button_buffer = grer_button.value()#grer_button.value()
            score += 1

            #print("\33[92mIncremented score\033[0m")
            send_data(score, time_remaining)
#        else:
#            print("Didnt meet and requirements")
#            print("")
#            print("Should be: Time > 0 grer_buffer == 1" ) # grer_button_value == 0
#            print("")
#            print("Was:")
#            print("Time Remaining:", time_remaining)
#            print('Grer button buffer:', grer_button_buffer)
#            print('Grer button:', grer_button.value())

def red_button_interrupt(red_button):
    global time_last_red, time_current_red
    # Get the current time
    time_current_red = time.ticks_ms()
    if time_current >= time_last:
        time_since_last_red = time_current_red - time_last_red
    else:
        # Handle wraparound
        time_since_last_red = (time_current + (0xFFFFFFFF - time_last)) + 1
        #print("Handled Wraparound")
    if time_since_last_red > 500:
        #print('Reseting Game')
        reset_game()

grer_button.irq(trigger = Pin.IRQ_FALLING, handler = grer_button_interrupt)
red_button.irq(trigger = Pin.IRQ_FALLING, handler = red_button_interrupt)

#Initialize Timer
timer_init()

while True:
    led_internal.toggle()
