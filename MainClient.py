import socket
import sys
import threading
import time
import utils
from settings import *
from ast import literal_eval as make_tuple

# TODO: import your minimax & board code, or you can overwrite the TODOs in @RobertoFigueroa lib module...
# from hoppers.game.board import Board
# from hoppers.game.minimax import Minimax
# from hoppers.game.node import Node
from pandas import *
import numpy as np
from Hoopers import Game, Coord

EXIT_CODES = {
    SERVER_FULL: "Server is full! Try again later",
    GAME_END : "Thank you for playing!"
}

ERROR_CODES = {
    ILLEGAL_MOVE: "Opponent sent an illegal move, change turn!",
}
GAME_OVER = False

if len(sys.argv) != 3:
    print("usage: client.py <server-ip> <port>")
    sys.exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_ip = sys.argv[1]
server_port = int(sys.argv[2])
if sys.argv[1] == "default":
    server_ip = SERVER_DEFAULT_IP

server_address = (server_ip, server_port)

# TODO: declare your board & your minimax bot
# board = Board()
# ai_bot = Minimax(TIME_LIMIT, True)
my_turn = None
game = Game()

def display_game():
    # TODO: show your board
    # board.pp_board()
    dataFrame = DataFrame(game.board)
    dataFrame.index = np.arange(1,len(dataFrame)+1)
    dataFrame.columns = np.arange(1,len(dataFrame)+1)
    print("-" * 42)
    print(dataFrame)
    print("-" * 42)

    # a = 1 # TODO: comment this line when you have done the above task...

def game_thread():
    # this function handles display
    global GAME_OVER
    global my_turn
    # global board
    global game
    while not GAME_OVER:
        response, _ = sock.recvfrom(BUFF_SIZE)

        # Parse bytes response to string
        response = response.decode()
        action, payload = response[0], response[1:]
        
        if action == REGISTER:
            # Payload: Player position, assigned by the server
            player_position = None
            if P1_POSITION == make_tuple(payload):
                player_position = P1_POSITION
            elif P2_POSITION == make_tuple(payload):
                player_position = P2_POSITION

            x, y = player_position
            print(f"Fui asignado a la posición: {x},{y}")

            # TODO: initialize your board, knowing which player (x,y) you were assigned by the server
            # board.set_turn(my_turn)
            my_turn = P1 if player_position == P1_POSITION else P2
            
            # TODO: start local game
            # board.init_pieces()  
            # board.pp_board()

        elif action == NEW_MOVE:
            dict_move = utils.from_xml(payload)

            initial_row, initial_col = int(dict_move['from']['@row']) +1, int(dict_move['from']['@col']) +1
            final_row, final_col = int(dict_move['to']['@row']) +1, int(dict_move['to']['@col']) +1

            # Finally, we need to move the piece placed at initial position
            # You can use a namedtuple as Position = (x, y) if you manage your pieces in this way
            new_move = (
                Coord(initial_row, initial_col), 
                Coord(final_row, final_col)
            )
            
            ##print(f"Move received: {initial_row},{initial_col} to {final_row},{final_col}")
            # TODO: process new move in your board & change turn
            # board.move_piece(new_move[0], new_move[1])
            # board.pp_board()
            # board.change_turn()
            print('Acción adversario:')
            print(new_move)
            game, path = game.result(new_move, calculatePath=True)
            #Cambia de turno
            game = game.changeTurn(game)
            print('Camino adversario:')
            print(path)

            display_game()


        elif action in EXIT_CODES:
            print(EXIT_CODES[response])
            GAME_OVER = True

        elif action in ERROR_CODES:
            print(ERROR_CODES[response])
            # TODO: change/omit opponent turn, and continue game
            # board.change_turn()
            game = game.changeTurn()

        else:
            print(action, payload)

def bot_thread():
    """
    This function handles bot response (moves)
    """
    # Server handshake
    #handshake_message = HANDSHAKE
    #sock.sendto(handshake_message.encode(), server_address)

    global GAME_OVER
    global my_turn
    # global board
    global game
    while not GAME_OVER:
        # print(board.turn)
        if game.state == my_turn:
            # Listen for Minimax or RL & MCTS Bot
            # copy_board = Board()
            # copy_board.set_board(board.get_board())
            # root_node = Node(board.turn, copy_board, 3)
            #print("AI thinking")

            # # TODO: await for Bot response to process its move
            # return_node, best_move = ai_bot.alpha_beta_minimax(root_node)
            # print("AI move  from {} to {}".format(best_move[0], best_move[1]))
            if(my_turn == P1):
                action = game.alphaBetaSearchPlayer1()
            else:
                action = game.alphaBetaSearchPlayer2()
            

            print('Mi Acción:')
            print(action)
            game, path = game.result(action, calculatePath=True)
            #Cambia de turno
            game = game.changeTurn(game)
            print('Mi Camino:')
            print(path)

            move_dict = {
                'from': (action[0].x -1, action[0].y -1),
                'to': (action[1].x - 1, action[1].y - 1)
            }
            move = utils.to_xml(move_dict)
            sock.send(f"{NEW_MOVE}{move}".encode())
            
            display_game()

            print("Enviando el movimiento al server...")
            # board.move_piece(best_move[0], best_move[1])
            # board.change_turn()

            # a = 1 # TODO: remove when you have done the above task...
        

def start_game():
    # this function launches the game
    bot = threading.Thread(target=bot_thread)
    game = threading.Thread(target=game_thread)
    bot.daemon = True
    game.daemon = True
    bot.start()
    game.start()
    while not GAME_OVER:
        time.sleep(1)

def initialize():
    print(f"Conectandose al server en el puerto: {server_ip}...")
    sock.connect(server_address)

initialize()
start_game()