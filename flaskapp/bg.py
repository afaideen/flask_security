import time

# from run import socketio


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 1
    while True:
        # socketio.sleep(10)
        time.sleep(2)
        count += 1
        # print("time is %d second" %(count))
        # socketio.emit('my_response',
        #               {'data': 'Server generated event', 'count': count})