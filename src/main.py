import json
from machine import Pin, PWM
from time import sleep

pin_pwms_used = []

def led_action_executor(duration, led_action):
    if led_action['mode'] == 'breathe':
        print('Action mode: breathe')
        led_breathe(duration,led_action)

def led_breathe(duration,led_action):
    pin = machine.Pin(led_action['pin'])
    pin_pwm = PWM(pin)
    pin_pwms_used.append(pin_pwm)
    duty_step = 129  # Step size for changing the duty cycle
    # Set PWM frequency
    frequency = 5000
    pin_pwm.freq(frequency)

    up_delay = 1./led_action['upSpeed']
    down_delay = 1./led_action['downSpeed']

    min_brightness = 65536*led_action['minBrightness']
    max_brightness = max(65536*led_action['maxBrightness'],65536)

    if min_brightness > max_brightness:
        print('Invalid configuration: min brightness exceeds max brightness')
        exit()

    cycle_time = int((max_brightness-min_brightness)/duty_step)*(up_delay + down_delay)

    cycles = duration/cycle_time

    print('Cycles: {}'.format(int(cycles)))

    for cycle in range(cycles):
        print('Brightening...')
        for duty_cycle in range(min_brightness, max_brightness, duty_step):
            pin_pwm.duty_u16(duty_cycle)
            sleep(up_delay)

        print('Dimming...')
        for duty_cycle in range(max_brightness, min_brightness, -duty_step):
            pin_pwm.duty_u16(duty_cycle)
            sleep(down_delay)

def main():
    with open('config/test.json') as file:
        config = json.load(file)
        print('Configuration loaded')

    for step in config:
        duration = step['duration']
        for led_action in step['ledActions']:
            print('Executing action')
            print(json.dumps(led_action))
            led_action_executor(duration=duration, led_action=led_action)
            print('Finished executing action')
    return 0

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        for pin_pwm in pin_pwms_used:
            pin_pwm.duty_u16(0)
            print(pin_pwm)
            pin_pwm.deinit()
    except Exception as e:
        print(e)
        for pin_pwm in pin_pwms_used:
            pin_pwm.duty_u16(0)
            print(pin_pwm)
            pin_pwm.deinit()