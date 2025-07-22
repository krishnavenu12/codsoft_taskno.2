import streamlit as st
import random
import math

st.set_page_config(page_title="Tic-Tac-Toe AI", layout="centered")
st.title("🎯 Tic-Tac-Toe: AI vs Human")

# --- Initialization ---
if "board" not in st.session_state:
    st.session_state.board = [[" "]*3 for _ in range(3)]
    st.session_state.symbol_user = "X"
    st.session_state.symbol_ai = "O"
    st.session_state.turn = "user"
    st.session_state.message = ""
    st.session_state.clicked = None
    st.session_state.difficulty = "Hard"
    st.session_state.scores = {"You": 0, "AI": 0, "Draws": 0}

# --- Sidebar Settings ---
with st.sidebar:
    st.header("⚙️ Settings")
    st.session_state.symbol_user = st.radio("Your Symbol", ["X", "O"], index=0)
    st.session_state.symbol_ai = "O" if st.session_state.symbol_user == "X" else "X"
    st.session_state.difficulty = st.selectbox("AI Difficulty", ["Easy", "Hard"])
    if st.button("🔁 Restart Game"):
        st.session_state.board = [[" "]*3 for _ in range(3)]
        st.session_state.message = ""
        st.session_state.turn = "user"
    if st.button("🧹 Reset All"):
        st.session_state.board = [[" "]*3 for _ in range(3)]
        st.session_state.message = ""
        st.session_state.turn = "user"
        st.session_state.scores = {"You": 0, "AI": 0, "Draws": 0}

# --- Game Logic ---
def is_winner(b, p):
    return any(
        all(cell == p for cell in row) or
        all(row[i] == p for row in b) or
        all(b[i][i] == p for i in range(3)) or
        all(b[i][2 - i] == p for i in range(3))
        for i, row in enumerate(b)
    )

def is_draw(b):
    return all(cell != " " for row in b for cell in row)

def get_moves(b):
    return [(i, j) for i in range(3) for j in range(3) if b[i][j] == " "]

def minimax(b, maximizing, ai, user):
    if is_winner(b, ai): return 1
    if is_winner(b, user): return -1
    if is_draw(b): return 0
    scores = []
    for i, j in get_moves(b):
        b[i][j] = ai if maximizing else user
        scores.append(minimax(b, not maximizing, ai, user))
        b[i][j] = " "
    return max(scores) if maximizing else min(scores)

def ai_move():
    board = st.session_state.board
    ai = st.session_state.symbol_ai
    user = st.session_state.symbol_user
    moves = get_moves(board)

    if st.session_state.difficulty == "Easy":
        move = random.choice(moves)
    else:
        best = -math.inf
        move = None
        for i, j in moves:
            board[i][j] = ai
            score = minimax(board, False, ai, user)
            board[i][j] = " "
            if score > best:
                best = score
                move = (i, j)

    if move:
        board[move[0]][move[1]] = ai

# --- Handle user move ---
if st.session_state.clicked:
    i, j = st.session_state.clicked
    if st.session_state.board[i][j] == " ":
        st.session_state.board[i][j] = st.session_state.symbol_user
        if is_winner(st.session_state.board, st.session_state.symbol_user):
            st.session_state.message = "🎉 You Win!"
            st.session_state.scores["You"] += 1
        elif is_draw(st.session_state.board):
            st.session_state.message = "🤝 Draw!"
            st.session_state.scores["Draws"] += 1
        else:
            ai_move()
            if is_winner(st.session_state.board, st.session_state.symbol_ai):
                st.session_state.message = "😈 AI Wins!"
                st.session_state.scores["AI"] += 1
            elif is_draw(st.session_state.board):
                st.session_state.message = "🤝 Draw!"
                st.session_state.scores["Draws"] += 1
    st.session_state.clicked = None

# --- Display Board (Styled) ---
st.subheader("Game Board")
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        value = st.session_state.board[i][j]
        if value == " " and st.session_state.message == "":
            if cols[j].button(" ", key=f"{i}-{j}", use_container_width=True):
                st.session_state.clicked = (i, j)
                st.rerun()
        else:
            cols[j].markdown(
                f"<div style='text-align:center; font-size:32px; font-weight:bold; color:#111;'>{value}</div>",
                unsafe_allow_html=True
            )

# --- Styled Result Display ---
if st.session_state.message:
    color = "green" if "Win" in st.session_state.message else "orange"
    st.markdown(
        f"<div style='text-align:center; font-size:28px; font-weight:bold; color:{color}; margin-top:20px'>{st.session_state.message}</div>",
        unsafe_allow_html=True
    )

# --- Scoreboard ---
st.markdown("### 📊 Scoreboard")
st.write(
    f"You: **{st.session_state.scores['You']}**  |  "
    f"AI: **{st.session_state.scores['AI']}**  |  "
    f"Draws: **{st.session_state.scores['Draws']}**"
)
