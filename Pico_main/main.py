from machine import Pin, Timer
import time

led_internal = Pin("LED", Pin.OUT)
grer_button = Pin(15, Pin.IN, Pin.PULL_UP)# S Pin.PULL_DOWN
red_button = Pin(16, Pin.IN, Pin.PULL_UP) # R Pin.PULL_DOWN
is_finished = Pin(17, Pin.OUT)	# E

#For Simulation Purposes
E_from_board_simulation = Pin(14, Pin.OUT)

score = 0
time_remaining = 60
tim = Timer(-1)

time_last = 0
time_current = 0
have_sent_highscore = False

grer_button_buffer = grer_button.value()


def timer_callback(t):
    global score, time_remaining, have_sent_highscore
    if time_remaining != 0:
        time_remaining -= 1
    if time_remaining == 0:
        is_finished.value(1)
        if have_sent_highscore == False:
            send_data ('-' + str(score), time_remaining)
            have_sent_highscore = True
    send_data (score, time_remaining)

def timer_init():
    tim.init(mode = Timer.PERIODIC, freq = 1000, callback = timer_callback)
    tim.init(period = 1000, callback = timer_callback)

def timer_deinit():
    tim.deinit()

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
    is_finished.value(0)
    
def grer_button_interrupt(grer_button):
    global score, time_remaining, grer_button_buffer, time_last, time_current
    
    time_since_last = time.ticks_diff(time.ticks_ms(),time_last,) 
    time_last=time_since_last
    if time_since_last > 30:
        if time_remaining != 0 & grer_button_buffer != grer_button.value():
            grer_button_buffer = grer_button.value()
            score += 1
            send_data(score, time_remaining)
    
def red_button_interrupt(red_button):
    reset_game()

grer_button.irq(trigger = Pin.IRQ_FALLING, handler = grer_button_interrupt)
red_button.irq(trigger = Pin.IRQ_FALLING, handler = red_button_interrupt)

#Initialize Timer
timer_init()

while True:
    grer_button_buffer = grer_button.value()
    led_internal.toggle()


