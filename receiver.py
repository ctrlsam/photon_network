import config
from gpiozero import LightSensor
from time import sleep
import binascii

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    ''' returns a readable string from a bit'''
    n = int(bits, 2)
    return int_to_bytes(n).decode(encoding, errors)

def int_to_bytes(i):
    ''' convert series of bits to a byte '''
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def start():
    ''' initiate the receiver '''
    sensor = LightSensor(config.RECEIVER_PIN)
    chars = []
    received = ""
    running = True

    ''' Loop until detected laser (syncing) '''
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





