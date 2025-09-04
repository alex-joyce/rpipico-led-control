import random


def duty_cycle_calculator(pin_config):
    print('Starting duty cycle calculation for pin {}'.format(pin_config['pinNo']))

    pin_duty_cycles = []
    action_count = 0

    for led_action in pin_config['ledActions']:
        print('Pin {} Action {}: {}'.format(pin_config['pinNo'], action_count, led_action['mode']))
        pin_duty_cycles.extend(led_actions[led_action['mode']](led_action))
        action_count += 1

    return pin_duty_cycles


def led_breathe(led_action):
    step_duty_cycles = []

    start_brightness = int(led_action['options']['startBrightness']*65536.)
    end_brightness = int(led_action['options']['endBrightness']*65536.)
    up_speed = int((end_brightness-start_brightness)/led_action['options']['upTicks'])
    down_speed = int((start_brightness-end_brightness)/led_action['options']['downTicks'])
    cycles = int(led_action['options']['cycles'])

    for cycle in range(0,cycles):
        step_duty_cycles.extend(range(start_brightness, end_brightness, up_speed))
        step_duty_cycles.extend(range(end_brightness, start_brightness, down_speed))

    return step_duty_cycles


def led_blink(led_action):
    step_duty_cycles = []

    brightness_high = int(led_action['options']['brightnessHigh']*65536.)
    brightness_low = int(led_action['options']['brightnessLow']*65536.)
    ticks_high = int(led_action['options']['ticksHigh'])
    ticks_low = int(led_action['options']['ticksLow'])
    cycles = int(led_action['options']['cycles'])

    for cycle in range(0,cycles):
        step_duty_cycles.extend([brightness_high] * ticks_high)
        step_duty_cycles.extend([brightness_low] * ticks_low)

    return step_duty_cycles


def led_static(led_action):
    step_duty_cycles = []

    brightness = int(led_action['options']['brightness']*65536.)
    ticks = int(led_action['options']['ticks'])

    step_duty_cycles.extend([brightness] * ticks)

    return step_duty_cycles


def led_fade(led_action):
    step_duty_cycles = []

    start_brightness = int(led_action['options']['startBrightness'] * 65536.)
    end_brightness = int(led_action['options']['endBrightness'] * 65536.)
    speed = int((end_brightness - start_brightness) / led_action['options']['ticks'])
    step_duty_cycles.extend(range(start_brightness, end_brightness, speed))

    return step_duty_cycles


def led_flicker(led_action):
    step_duty_cycles = []
    ticks_used = 0

    brightness_high = int(led_action['options']['brightnessHigh'] * 65536.)
    brightness_low = int(led_action['options']['brightnessLow'] * 65536.)
    low_interval = int(led_action['options']['lowInterval'])
    high_interval = int(led_action['options']['highInterval'])
    ticks = int(led_action['options']['ticks'])

    while ticks_used < ticks:
        if ticks - ticks_used in range (1,low_interval+high_interval):
            flicker_ticks = ticks - ticks_used
            step_duty_cycles.extend([brightness_high] * (ticks - ticks_used))

            ticks_used += flicker_ticks
        else:
            flicker_ticks = random.randint(low_interval, high_interval)
            ticks_used += 2*flicker_ticks

            step_duty_cycles.extend([brightness_high] * flicker_ticks)
            step_duty_cycles.extend([brightness_low] * flicker_ticks)

    return step_duty_cycles


led_actions = {
    'breathe': led_breathe,
    'blink': led_blink,
    'static': led_static,
    'fade': led_fade,
    'flicker': led_flicker
}