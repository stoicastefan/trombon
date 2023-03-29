from flask import Flask, render_template, session, copy_current_request_context
from flask_socketio import SocketIO, emit, disconnect, send
from threading import Lock
from flask_socketio import join_room, leave_room

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket_ = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


@app.route('/')
def index():
    return render_template('index.html', async_mode=socket_.async_mode)


# TODO Create input form for username and room and try to separate them

@socket_.on('join', namespace='/test')
def on_join(message):
    username = message['username']
    room = message['room']
    join_room(room)
    print("Welcome to room: " + room + " with user " + username)
    send(username + ' has entered the room.', to=room)


@socket_.on('leave', namespace='/test')
def on_leave(message):
    username = message['username']
    room = message['room']
    leave_room(room)
    send(username + ' has left the room.', to=room)


@socket_.on('my_event', namespace='/test')
def test_message(message):
    print(message)
    session['receive_count'] = session.get('receive_count', 0) + 1
    session['number_of_cards'] = {'r11': 1, 'n11': 1}

    emit('my_response',
         {'data': message['data'], 'count': session['receive_count'], 'number_of_cards': session['number_of_cards']})


@socket_.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    aux_var = session.get('number_of_cards')
    aux_var['r11'] = 0
    print(aux_var)
    session['number_of_cards'] = aux_var
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count'], 'number_of_cards': session['number_of_cards']},
         broadcast=True, to="stefan")


@socket_.on('disconnect_request', namespace='/test')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    session['number_of_cards'] = session.get('number_of_cards', 600) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count'], 'number_of_cards': session['number_of_cards']},
         callback=can_disconnect)


if __name__ == '__main__':
    socket_.run(app, debug=True)
