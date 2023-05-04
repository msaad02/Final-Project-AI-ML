import tensorflow as tf
import chess

import runBotHelpers

model = tf.keras.models.load_model("C:\\Users\\Matthew Saad\\OneDrive\\College\\Spring 2023\\AI & ML\\Final-Project-AI-ML\\saved_models\\corrected_12mil_3epoch_64batch_0.0001learnRate")

board = chess.Board()
depth = 2

while not board.is_game_over():
    print(board)
    print()

    if board.turn == chess.WHITE:
        move = runBotHelpers.find_best_move(board, depth, True, model)
        print(move)
    else:
        print('Move: ')
        move = chess.Move.from_uci(input())
        

    board.push(move)

print("Game over")
print("Result:", board.result())