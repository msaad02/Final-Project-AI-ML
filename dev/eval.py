import re
import numpy as np

def vectorize(fen):
    data = re.split(" ", fen)
    rows= re.split("/", data[0])
    turn = data[1]
    can_castle = data[2]
    passant = data[3]
    half_moves = data[4]
    full_moves = data[5]
    
    bit_vector = np.zeros((13, 8, 8), dtype=np.uint8)
    #what layer each piece is found on
    piece_to_layer = {
            'R': 1,
            'N': 2,
            'B': 3,
            'Q': 4,
            'K': 5,
            'P': 6,
            'p': 7,
            'k': 8,
            'q': 9,
            'b': 10,
            'n': 11,
            'r': 12
        }
    #find each piece based on type
    for r,value in enumerate(rows):
        colum = 0
        for piece in value:
            if piece in piece_to_layer:
                bit_vector[piece_to_layer[piece],r,colum] =1
                colum += 1
            else:
                colum += int(piece)
    
    if turn.lower() == 'w':
        bit_vector [0,7,4] =1
    else:
        bit_vector [0,0,4] =1
        
    #where each castle bit is located
    castle ={
        'k': (0,0),
        'q': (0,7),
        'K': (7,0),
        'Q': (7,7),
        }

    for value in can_castle:
        if value in castle:
            bit_vector[0,castle[value][0],castle[value][1]] = 1
    
    #put en-passant square in the vector
    if passant != '-':
        bit_vector[0,  5 if (int(passant[1])-1 == 3) else 2 , ord(passant[0]) - 97,] = 1
        
    return bit_vector
    
print(vectorize(r'rnbqkb1r/ppp1pppp/3p4/3nP3/3P4/8/PPPK1PPP/RNBQ1BNR b kq - 1 4')[0])
print(vectorize(r'r3r1k1/pppq2bp/3pp1p1/3P4/2PpP3/6P1/PP1N2K1/R1BQR3 b - e3 0 19')[0])

import numpy as np
import tensorflow as tf

def train_neural_network(bit_vector):
    # Define the neural network architecture
    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(13, 8, 8)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    # Compile the model
    model.compile(optimizer='rmsprop',
                  loss='mean_squared_error',
                  metrics=['accuracy'])

    # Prepare the training data
    x_train = np.array([bit_vector])
    y_train = np.array([0])  # Replace 0 with the actual label of the position

    # Train the model
    model.fit(x_train, y_train, epochs=10, batch_size=1)
    x_test = np.array([bit_vector])
    y_test = np.array([0])  # Replace 0 with the actual label of the test position

    # Evaluate the model on the test data
    loss, accuracy = model.evaluate(x_test, y_test)

    # Print the evaluation metrics
    print(f"Test loss: {loss:.4f}")
    print(f"Test accuracy: {accuracy:.4f}")


import pandas as pd

names = ['PuzzleId','FEN','Moves','Rating','RatingDeviation','Popularity','NbPlays','Themes','GameUrl','OpeningTags']
df = pd.read_csv('../data/kaggleDataset/chessData.csv', names = names)

train_neural_network(vectorize(df.FEN))