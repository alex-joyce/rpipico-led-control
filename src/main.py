import json
import duty_cycle_calculator as dcs
from machine import Pin, PWM
from time import sleep


pin_pwms = dict()
pin_nos = []


def main():
    frequency = 5000
    duty_cycles = dict()
    with open('config/test.json') as file:
        config = json.load(file)
        print('Configuration loaded')

    for pin_config in config:
        pin_no = pin_config['pinNo']
        pin_nos.append(pin_no)
        pin_pwms[pin_no] = PWM(machine.Pin(pin_no))
        pin_pwms[pin_no].freq(frequency)
        duty_cycles[pin_no] = dcs.duty_cycle_calculator(pin_config)
        print('Finished generating duty cycles for pin {}'.format(pin_no))

    tick = 0
    while True:
        for pin_no in pin_nos:
            pin_pwms[pin_no].duty_u16(
                duty_cycles[pin_no][tick % len(duty_cycles[pin_no])]
            )
        sleep(0.02)
        tick += 1

    return


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        for pin_no in pin_nos:
            pin_pwms[pin_no].duty_u16(0)
            print(pin_pwms[pin_no])
            pin_pwms[pin_no].deinit()
    except Exception as e:
        print(e)
        for pin_no in pin_nos:
            pin_pwms[pin_no].duty_u16(0)
            print(pin_pwms[pin_no])
            pin_pwms[pin_no].deinit()