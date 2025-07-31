pin_pwms_used = []
pins = dict()

def duty_cycle_calculator(pin_config):
    print('Starting duty cycle calculation for pin {}'.format(pin_config['pinNo']))
    pin_duty_cycles = []
    action_count = 0
    for led_action in pin_config['ledActions']:
        print('Pin {} Action {}: {}'.format(pin_config['pinNo'], action_count, led_action['mode']))

        if led_action['mode'] == 'breathe':
            pin_duty_cycles.extend(led_breathe(led_action))
        elif led_action['mode'] == 'blink':
            pin_duty_cycles.extend(led_blink(led_action))
        elif led_action['mode'] == 'static':
            pin_duty_cycles.extend(led_static(led_action))

        action_count += 1
    return pin_duty_cycles

def led_breathe(led_action):
    step_duty_cycles = []

    min_brightness = int(led_action['breatheOptions']['minBrightness']*65536.)
    max_brightness = int(led_action['breatheOptions']['maxBrightness']*65536.)
    up_speed = int((max_brightness-min_brightness)/led_action['breatheOptions']['upTicks'])
    down_speed = int((min_brightness-max_brightness)/led_action['breatheOptions']['downTicks'])
    cycles = int(led_action['cycles'])

    step_duty_cycles.append(0)
    for cycle in range(0,cycles):
        step_duty_cycles.extend(range(min_brightness, max_brightness, up_speed))
        step_duty_cycles.extend(range(max_brightness, min_brightness, down_speed))
    step_duty_cycles.append(0)

    return step_duty_cycles

def led_blink(led_action):
    step_duty_cycles = []

    brightness_high = int(led_action['blinkOptions']['brightnessHigh']*65536.)
    brightness_low = int(led_action['blinkOptions']['brightnessLow']*65536.)
    ticks_on = int(led_action['blinkOptions']['ticksOn'])
    ticks_off = int(led_action['blinkOptions']['ticksOff'])
    cycles = int(led_action['cycles'])

    step_duty_cycles.append(brightness_low)
    for cycle in range(0,cycles):
        for ticks in range(ticks_on):
            step_duty_cycles.append(brightness_high)
        for ticks in range(ticks_off):
            step_duty_cycles.append(brightness_low)
    step_duty_cycles.append(brightness_low)

    return step_duty_cycles

def led_static(led_action):
    step_duty_cycles = []

    brightness = int(led_action['staticOptions']['brightness']*65536.)
    ticks = int(led_action['staticOptions']['ticks'])

    for ticks in range(ticks):
        step_duty_cycles.append(brightness)

    return step_duty_cycles

def led_fade(led_action):
    step_duty_cycles = []
    ## TODO implement
    return step_duty_cycles

def led_fluorescent(led_action):
    step_duty_cycles = []
    ## TODO implement
    return step_duty_cycles