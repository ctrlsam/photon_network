from gpiozero import LED
import config
from time import sleep
import binascii

laser = LED(config.LASER_PIN)

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def sendStartFinish():
    laser.on()
    sleep(config.SEND_RATE * 8)    

def send(text):
    sendStartFinish()

    bits = list(text_to_bits(text))
    print('Sending: [{}] {} [{}]'.format(
        '1'*8, bits, '1'*8
    ))

    for bit in bits:
        if bit == '1':
            laser.on()
        else:
            laser.off()
        sleep(config.SEND_RATE)

    sendStartFinish()
    laser.off()
    print('Message sent!')

