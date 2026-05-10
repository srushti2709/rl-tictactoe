import streamlit as st
import pickle

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="RL Tic Tac Toe",
    page_icon="🎮",
    layout="centered"
)

# ---------------- LOAD Q TABLE ----------------
with open("qtable.npy", "rb") as f:
    q_table = pickle.load(f)

# ---------------- FUNCTIONS ----------------
def available_moves(board):
    return [i for i in range(9) if board[i] == " "]


def get_best_move(board):

    state = str(board)

    moves = available_moves(board)

    qs = [q_table.get((state, a), 0) for a in moves]

    max_q = max(qs)

    return moves[qs.index(max_q)]


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


# ---------------- SESSION STATES ----------------
if "board" not in st.session_state:
    st.session_state.board = [" "] * 9

if "player_score" not in st.session_state:
    st.session_state.player_score = 0

if "ai_score" not in st.session_state:
    st.session_state.ai_score = 0

if "draw_score" not in st.session_state:
    st.session_state.draw_score = 0

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "message" not in st.session_state:
    st.session_state.message = ""

board = st.session_state.board

# ---------------- TITLE ----------------
st.title("🎮 Tic Tac Toe RL AI")

# ---------------- SCOREBOARD ----------------
col1, col2, col3 = st.columns(3)

col1.metric("🧑 You", st.session_state.player_score)
col2.metric("🤖 AI", st.session_state.ai_score)
col3.metric("🤝 Draw", st.session_state.draw_score)

st.write("")

# ---------------- GAME BOARD ----------------
for row in range(3):

    cols = st.columns(3)

    for col in range(3):

        i = row * 3 + col

        if cols[col].button(board[i], key=i):

            if board[i] == " " and not st.session_state.game_over:

                # USER MOVE
                board[i] = "X"

                # USER WIN
                if check_winner(board, "X"):

                    st.session_state.player_score += 1
                    st.session_state.game_over = True
                    st.session_state.message = "🎉 You Win!"

                # DRAW
                elif len(available_moves(board)) == 0:

                    st.session_state.draw_score += 1
                    st.session_state.game_over = True
                    st.session_state.message = "🤝 Match Draw!"

                else:

                    # AI MOVE
                    ai_move = get_best_move(board)

                    board[ai_move] = "O"

                    # AI WIN
                    if check_winner(board, "O"):

                        st.session_state.ai_score += 1
                        st.session_state.game_over = True
                        st.session_state.message = "🤖 AI Wins!"

                    # DRAW
                    elif len(available_moves(board)) == 0:

                        st.session_state.draw_score += 1
                        st.session_state.game_over = True
                        st.session_state.message = "🤝 Match Draw!"

# ---------------- RESULT MESSAGE ----------------
if st.session_state.message:
    st.subheader(st.session_state.message)

st.write("")

# ---------------- RESTART BUTTON ----------------
if st.button("🔄 Restart Game"):

    st.session_state.board = [" "] * 9
    st.session_state.game_over = False
    st.session_state.message = ""

    st.rerun()

# ---------------- RESET SCOREBOARD ----------------
if st.button("🗑 Reset Scoreboard"):

    st.session_state.player_score = 0
    st.session_state.ai_score = 0
    st.session_state.draw_score = 0

    st.session_state.board = [" "] * 9
    st.session_state.game_over = False
    st.session_state.message = ""

    st.rerun()