from flask import Flask, render_template, session, copy_current_request_context
from flask_socketio import SocketIO, emit, disconnect, send
from threading import Lock
from flask_socketio import join_room, leave_room
import random

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



players = [{'username': 'Player 1', 'hand': []}, {'username': 'Player 2', 'hand': []}, {'username': 'Player 3', 'hand': []}]

def create_deck():
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    deck = [(rank, suit) for rank in ranks for suit in suits]
    return deck

def shuffle_deck(deck):
    random.shuffle(deck)

def play_game(deck, players):
    trombon = False
    num_players = len(players)
    num_cards = len(deck) // num_players  # integer division
    for i in range(num_players):
        hand = []
        for j in range(num_cards):
            hand.append(deck.pop())
        players[i]['hand'] = hand
    # Deal remaining cards to last player, if any
    if len(deck) > 0:
        for card in deck:
            players[-1]['hand'].append(deck.pop())
    turn = 0
    if turn == 0:
        claimed_card = input('Claim a card value:')
    cards_on_table = []
    while True:
        if trombon == True:
            if trombon == True:
                # Check if the selected cards have the same value as the claimed value of the card
                selected_card_values = [card[0] for card in selected_cards]
                if claimed_card in selected_card_values:
                    print("Selected cards have the same value as the claimed card.")
                    print("Player who pressed trombon draws the cards on table.")
                    players[turn]['hand'].extend(cards_on_table)
                    cards_on_table = []
                    # Reset turn to the player who pressed trombon
                    turn = (turn - 1) % num_players
                else:
                    print("Selected cards do not have the same value as the claimed card.")
                    print("Player who selected the cards draws the cards on table.")
                    players[turn]['hand'].extend(cards_on_table)
                    cards_on_table = []
                    turn = (turn + 1) % num_players
                trombon = False

            pass
            #Check if the selected cards have the same value as the claimed value of the card
            #If it is the same, the person who pressed trombon draws
            #If not, the person who selected the cards draws the cards_on_table
            #cards_on_table = []
            #turn = 0 to reset game
            #The next person after the one that drew the cards now starts
        player = players[turn]
        print(player['username'] + "'s turn")
        print("Current hand:")
        print(player['hand'])
        play = input("Select cards to play (comma-separated): ")
        cards_to_play = [int(card) for card in play.split(",")]
        selected_cards = []
        for card in cards_to_play:
            selected_cards.append(player['hand'][card])
        for card in selected_cards:
            player['hand'].remove(card)
            cards_on_table.append(card)
        print(player['username'] + " plays:")
        print(selected_cards)

        turn = (turn + 1) % num_players

        if len(deck) == 0 and all([len(player['hand']) == 0 for player in players]):
            print("Cards on table:")
            print(cards_on_table)
            break

deck = create_deck()
shuffle_deck(deck)
play_game(deck, players)
player_count = 0

# for player in players:
#     print(player['username'] + "'s hand:")
#     print(player['hand'])
#     print()




