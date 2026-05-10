import streamlit as st
import pickle

# Load trained AI
with open("qtable.npy","rb") as f:
    q_table = pickle.load(f)

# Empty cells
def available_moves(board):
    return [i for i in range(9) if board[i] == " "]

# Best AI move
def get_best_move(board):

    state = str(board)

    moves = available_moves(board)

    qs = [q_table.get((state,a),0)
          for a in moves]

    max_q = max(qs)

    return moves[qs.index(max_q)]

# Winner check
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
        if all(board[i]==player for i in w):
            return True

    return False

# Title
st.title("Tic Tac Toe RL AI")

# Create board
if "board" not in st.session_state:
    st.session_state.board = [" "] * 9

board = st.session_state.board

# Create buttons
cols = st.columns(3)

for i in range(9):

    if cols[i%3].button(board[i], key=i):

        if board[i] == " ":

            # User move
            board[i] = "X"

            # User wins
            if check_winner(board,"X"):
                st.success("You Win!")
                st.stop()

            # AI move
            if len(available_moves(board)) > 0:

                ai = get_best_move(board)

                board[ai] = "O"

                # AI wins
                if check_winner(board,"O"):
                    st.error("AI Wins!")

# Restart button
if st.button("Restart"):
    st.session_state.board = [" "] * 9