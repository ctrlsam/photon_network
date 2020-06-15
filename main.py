import receiver, laser
from threading import Thread

text = input('\nMessage to send: ')
print('Sending message...')

# Start receiver thread
reciever_thread = Thread(
    target = receiver.start)
reciever_thread.start()

# Start laser thread
laser_thread = Thread(
    target = laser.send,
    args = (text,)
)
laser_thread.start()