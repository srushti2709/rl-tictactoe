import numpy as np
import random
import pickle

# Q-table
q_table = {}

# Parameters
alpha = 0.1
gamma = 0.9
epsilon = 0.2

# Convert board into state
def get_state(board):
    return str(board)

# Find empty positions
def available_moves(board):
    return [i for i in range(9) if board[i] == " "]

# Choose move
def choose_action(state, moves):

    # Exploration
    if random.uniform(0,1) < epsilon:
        return random.choice(moves)

    # Exploitation
    qs = [q_table.get((state,a),0) for a in moves]

    max_q = max(qs)

    return moves[qs.index(max_q)]

# Update Q-table
def update_q(state, action, reward,
             next_state, next_moves):

    old_q = q_table.get((state,action),0)

    future_q = 0

    if next_moves:
        future_q = max(
            [q_table.get((next_state,a),0)
             for a in next_moves]
        )

    q_table[(state,action)] = old_q + alpha * (
        reward + gamma * future_q - old_q
    )

# Check winner
def check_winner(board, player):

    wins = [
        [0,1,2],
        [3,4,5],
        [6,7,8],
        [0,3,6],
        [1,4,7],
        [2,5,8],
        [0,4,8],
        [2,4,6]
    ]

    for w in wins:
        if all(board[i] == player for i in w):
            return True

    return False

# Training Loop
for episode in range(10000):

    board = [" "] * 9

    while True:

        state = get_state(board)

        moves = available_moves(board)

        action = choose_action(state, moves)

        board[action] = "X"

        # AI wins
        if check_winner(board,"X"):

            update_q(state, action,
                     1, state, [])

            break

        # Draw
        if len(available_moves(board)) == 0:

            update_q(state, action,
                     0, state, [])

            break

        # Opponent move
        opponent = random.choice(
            available_moves(board)
        )

        board[opponent] = "O"

        # Opponent wins
        if check_winner(board,"O"):

            update_q(state, action,
                     -1, state, [])

            break

        next_state = get_state(board)

        update_q(
            state,
            action,
            0,
            next_state,
            available_moves(board)
        )

# Save AI memory
with open("qtable.npy","wb") as f:
    pickle.dump(q_table,f)

print("Training Complete")