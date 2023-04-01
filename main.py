from flask import Flask, render_template, session, copy_current_request_context
from flask_socketio import SocketIO, emit, disconnect, send
from threading import Lock
from flask_socketio import join_room, leave_room
import random
import sys
# async_mode = None
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# socket_ = SocketIO(app, async_mode=async_mode)
# thread = None
# thread_lock = Lock()
#
#
# @app.route('/')
# def index():
#     return render_template('index.html', async_mode=socket_.async_mode)
#
#
# # TODO Create input form for username and room and try to separate them
#
# @socket_.on('join', namespace='/test')
# def on_join(message):
#     username = message['username']
#     room = message['room']
#     join_room(room)
#     print("Welcome to room: " + room + " with user " + username)
#     send(username + ' has entered the room.', to=room)
#
#
# @socket_.on('leave', namespace='/test')
# def on_leave(message):
#     username = message['username']
#     room = message['room']
#     leave_room(room)
#     send(username + ' has left the room.', to=room)
#
#
# @socket_.on('my_event', namespace='/test')
# def test_message(message):
#     print(message)
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     session['number_of_cards'] = {'r11': 1, 'n11': 1}
#
#     emit('my_response',
#          {'data': message['data'], 'count': session['receive_count'], 'number_of_cards': session['number_of_cards']})
#
#
# @socket_.on('my_broadcast_event', namespace='/test')
# def test_broadcast_message(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     aux_var = session.get('number_of_cards')
#     aux_var['r11'] = 0
#     print(aux_var)
#     session['number_of_cards'] = aux_var
#     emit('my_response',
#          {'data': message['data'], 'count': session['receive_count'], 'number_of_cards': session['number_of_cards']},
#          broadcast=True, to="stefan")
#
#
# @socket_.on('disconnect_request', namespace='/test')
# def disconnect_request():
#     @copy_current_request_context
#     def can_disconnect():
#         disconnect()
#
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     session['number_of_cards'] = session.get('number_of_cards', 600) + 1
#     emit('my_response',
#          {'data': 'Disconnected!', 'count': session['receive_count'], 'number_of_cards': session['number_of_cards']},
#          callback=can_disconnect)
#
#
# if __name__ == '__main__':
#     socket_.run(app, debug=True, allow_unsafe_werkzeug=True)

# needed variable

players = [{'username': 'Radu', 'hand': []}, {'username': 'Stefan', 'hand': []}, {'username': 'Paul', 'hand': []}, {'username': 'Cristian', 'hand': []}]
num_players = len(players)
cards_on_table = []
selected_cards = []
current_player = 0
start_game = True
claimed_card = ''
turn_ended = False
game_over = False

def create_deck():
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['♥', '♦', '♣', '♠']
    deck = [(rank, suit) for rank in ranks for suit in suits]
    return deck

deck = create_deck()
num_cards = len(deck)

def shuffle_deck(deck):
    return random.shuffle(deck)

def deal_cards(deck, players):
    num_cards = len(deck) // num_players

    for i in range(num_players):
        hand = []
        for j in range(num_cards):
            if deck:
                hand.append(deck.pop())
        players[i]['hand'] = hand

    if deck:
        for card in deck:
            players[-1]['hand'].append(card)

def show_cards():
    for player in players:
        print(player['hand'])

def game_setup():
    shuffle_deck(deck)
    deal_cards(deck, players)

def check_quads():
    global players

    # create a dictionary how many times a certain element is in the list
    count_dict = {}

    for item in players[current_player]['hand']:
        if item[0] in count_dict:
            count_dict[item[0]] += 1
        else:
            count_dict[item[0]] = 1

    to_remove = []

    for key in count_dict:
        if count_dict[key] == 4:
            print('You have quad ' + key)
            to_remove += [item for item in players[current_player]['hand'] if item[0] == key]

    for item in to_remove:
        players[current_player]['hand'].remove(item)

def new_turn():
    global cards_on_table, current_player, players, selected_cards, cards_on_table, claimed_card

    print(players[current_player]['username'])
    print(players[current_player]['hand'])
    claimed_card = input("Claim a card value:")
    play = input("Select cards to play (comma-separated):")
    cards_to_play = [int(card) for card in play.split(",")]
    selected_cards = []
    for card in cards_to_play:
        selected_cards.append((players[current_player]['hand'][card]))
        if len(selected_cards) > 3:
            print('You can only place a maximum of 3 cards!')
            new_turn()
    for card in selected_cards:
        players[current_player]['hand'].remove(card)
        cards_on_table.append(card)
    current_player += 1
    return selected_cards, cards_on_table, current_player, claimed_card

def player_actions():
    global cards_on_table, current_player, players, selected_cards, claimed_card, turn_ended, game_over
    turn_ended = False
    if current_player > len(players) - 1:
        current_player = 0
    check_quads()
    print(players[current_player]['username'])
    print(players[current_player]['hand'])
    play = input("Select cards to play (comma-separated) or 't' to trombon: ")
    if play == 't':
        if all([card[0] == claimed_card for card in selected_cards]):
            print("Selected cards have the same value as the claimed card.")
            print(players[current_player]['username'] + " draws the cards on table.")
            players[current_player]['hand'].extend(cards_on_table)
            cards_on_table = []
            if len(players[current_player - 1]['hand']) == 0:
                print(players[current_player - 1]['username'] + " wins!")
                game_over = True
                return game_over
            current_player = (current_player + 1) % num_players
            turn_ended = True
            return current_player, turn_ended
        else:
            print("Selected cards do not have the same value as the claimed card.")
            previous_player = current_player - 1
            if previous_player < 0:
                previous_player = len(players) - 1
            players[previous_player]['hand'].extend(cards_on_table)
            print(players[previous_player]['username'] + " draws the cards on table.")
            cards_on_table = []
            turn_ended = True
            return current_player, turn_ended
    else:
        if len(players[current_player - 1]['hand']) == 0:
            print(players[current_player]['username'] + " wins!")
            game_over = True
            return game_over
        cards_to_play = [int(card) for card in play.split(",")]
        if len(cards_to_play) > 3:
            print('You can only place a maximum of 3 cards!')
            player_actions()
        selected_cards = []
        for card in cards_to_play:
            selected_cards.append((players[current_player]['hand'][card]))
        for card in selected_cards:
            players[current_player]['hand'].remove(card)
            cards_on_table.append(card)
        current_player += 1
        print('Cards on table are:' + '\n' + str(cards_on_table))
        player_actions()

    return selected_cards, cards_on_table, current_player

game_setup()
if game_over == True:
    current_player = 0
    start_game = True

if start_game == True :
    print("New game!")
    new_turn()
    player_actions()

while turn_ended == True:
    print('New turn!')
    new_turn()
    player_actions()
