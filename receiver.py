import config
from gpiozero import LightSensor
from time import sleep
import binascii

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def start():
    sensor = LightSensor(config.RECEIVER_PIN)
    chars = []
    received = ""
    running = True

    while True:
        if int(sensor.light_detected):
            break

    while running:

        # lets get the message
        bit = int(sensor.light_detected)
        received += str(bit)

        if len(received) >= 8:
            # end
            if received == config.START_END and len(chars) != 0:
                print('[Receiver] stopped recording')
                running = False

            # start
            elif received == config.START_END:
                print('[Receiver] recording...')
                received = ""

            # append
            else:
                chars.append(received)
                received = ""
        
        sleep(config.SEND_RATE)
    
    # message received, process it
    msg = ""
    for c in chars:
        try:
            msg += text_from_bits(c)
        except Exception:
            msg += ' unknown '

    print(msg)
    print(chars)
    chars = []
    received = ""





