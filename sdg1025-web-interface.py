#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import usbtmc
from SDG1025 import SDG1025
from time import sleep

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

sdg1025 = SDG1025(debug=1)
if not sdg1025.isConnected:
    print('Couldn\'t connect to SDG1025!')
    quit()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('evt_response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')


@app.route('/')
def index():
    return render_template('sdg1025.html', async_mode=socketio.async_mode)


@socketio.on('evt_wtfru_req', namespace='/test')
def test_wtfru(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    resp = sdg1025.getIDN()
    emit('evt_response',
         {'data': resp, 'count': session['receive_count']})


@socketio.on('set_freq', namespace='/test')
def set_freq(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    # print('message data: %s' % message)
    ch = int(message['ch'])
    freq = message['freq']
    sdg1025.setChannelFreq(ch, freq)


@socketio.on('set_wave', namespace='/test')
def set_wave(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    ch = int(message['ch'])
    wave = message['wave']
    sdg1025.setChannelWave(ch, wave)


@socketio.on('set_amplitude', namespace='/test')
def set_amplitude(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    ch = int(message['ch'])
    ampl = message['ampl']
    sdg1025.setChannelAmplitude(ch, ampl)


@socketio.on('set_offset', namespace='/test')
def set_offset(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    ch = int(message['ch'])
    offset = message['offset']
    sdg1025.setChannelOffset(ch, offset)


@socketio.on('set_onoff', namespace='/test')
def set_onoff(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    ch = int(message['ch'])
    onoff = message['onoff']
    print('onoff: %d' % onoff)
    if onoff == 0:
        sdg1025.disableChannel(ch)
    else:
        sdg1025.enableChannel(ch)


@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    # for this emit we use a callback function
    # when the callback function is invoked we know that the message has been
    # received and it is safe to disconnect
    emit('evt_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)


@socketio.on('my_ping', namespace='/test')
def ping_pong():
    emit('my_pong')


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    # Send channel data
    sleep(1)
    ch1 = sdg1025.getChannel(1)
    ch2 = sdg1025.getChannel(2)
    emit('evt_connect', {'data': 'Connected', 'count': 0, 'ch1': ch1, 'ch2': ch2})
    # print("sending ch1: %s" % ch1)
    # print("sending ch2: %s" % ch2)


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)

if __name__ == '__main__':
    print('Starting Flask web server...')
    print('Open this link to your browser: http://127.0.0.1:5000/')
    # socketio.run(app, debug=True)
    socketio.run(app, host='0.0.0.0', debug=False)
