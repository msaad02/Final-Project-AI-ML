import re
import numpy as np

def preprocess_scores(eval):
    score_dict = {
        '#+': 20,
        '#-': -20
    }

    try:
        eval = int(eval)
        eval = max(min(eval, 15), -15)
    except ValueError:
        eval = score_dict.get(eval[0:2], 0)

    return eval

def vectorize(fen):
    data = re.split(" ", fen)
    rows= re.split("/", data[0])
    turn = data[1]
    can_castle = data[2]
    passant = data[3]
    half_moves = data[4]
    full_moves = data[5]
    
    bit_vector = np.zeros((13, 8, 8), dtype=np.float32)
    #print(bit_vector.shape)
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
    
    return bit_vector.flatten()