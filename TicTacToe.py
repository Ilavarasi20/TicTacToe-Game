import random
import streamlit as st

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Tic Tac Toe",
    page_icon="🎮",
    layout="centered"
)

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
def initialize_state():
    defaults = {
        "board": [""] * 9,
        "game_over": False,
        "winner": None,
        "message": "Your turn! Choose a box.",
        "difficulty": "Easy",
        "previous_difficulty": "Easy",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def new_game():
    st.session_state.board = [""] * 9
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.message = "Your turn! Choose a box."


initialize_state()

# ==========================================
# PURPLE-PINK THEME
# ==========================================
st.html("""
<style>
.stApp {
    background: linear-gradient(135deg, #eadcff, #f9c9e9, #d9c5ff, #ffcce5);
    background-attachment: fixed;
}
.block-container {
    max-width: 620px;
    padding-top: 1.8rem;
    padding-bottom: 2rem;
}
h1, h2, h3, h4, p, label {
    color: #70258c;
}
div[data-testid="stButton"] button {
    min-height: 88px;
    height: 88px;
    border-radius: 14px;
    border: 3px solid #bb75d4;
    background: linear-gradient(135deg, #ffffff, #fce3f4);
    color: #852caa;
    font-size: 36px;
    font-weight: 900;
    box-shadow: 0 4px 8px rgba(100, 30, 130, 0.15);
}
div[data-testid="stButton"] button:hover {
    background: #f4c9ed;
    border-color: #ed78bb;
    color: #70258c;
}
div[data-testid="stButton"] button:disabled {
    opacity: 1;
    color: #852caa;
    background: linear-gradient(135deg, #ffffff, #fce3f4);
    border-color: #bb75d4;
}
div[data-testid="stButton"] button[kind="primary"] {
    min-height: 48px;
    height: 48px;
    background: linear-gradient(90deg, #9b45bd, #ec70b5);
    color: white;
    border: none;
    font-size: 17px;
}
div[data-testid="stSelectbox"] > label {
    color: #70258c;
    font-weight: 700;
}
@media (max-width: 600px) {
    .block-container {
        padding-left: 12px;
        padding-right: 12px;
    }
    div[data-testid="stButton"] button {
        min-height: 74px;
        height: 74px;
        font-size: 30px;
    }
}
</style>
""")

# ==========================================
# SNOWFALL ON APP OPEN / RERUN
# ==========================================
snow_html = """
<style>
.snow-container {
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
    overflow: hidden;
    z-index: 999999;
}
.snowflake {
    position: absolute;
    top: -30px;
    color: white;
    text-shadow: 0 0 8px #a94acb;
    animation-name: snowfall;
    animation-timing-function: linear;
    animation-iteration-count: infinite;
}
@keyframes snowfall {
    from { transform: translateY(-5vh) rotate(0deg); }
    to { transform: translateY(110vh) rotate(360deg); }
}
</style>
<div class="snow-container">
"""
for _ in range(35):
    left = random.randint(0, 100)
    duration = random.randint(6, 14)
    delay = random.randint(0, 12)
    size = random.randint(12, 24)
    snow_html += (
        f'<span class="snowflake" style="left:{left}%;'
        f'animation-duration:{duration}s;animation-delay:-{delay}s;'
        f'font-size:{size}px;">❄</span>'
    )
snow_html += "</div>"
st.html(snow_html)

# ==========================================
# GAME RULES
# ==========================================
WINNING_COMBINATIONS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]


def check_winner(board):
    """Return X, O, Draw, or None."""
    for a, b, c in WINNING_COMBINATIONS:
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a]

    if "" not in board:
        return "Draw"

    return None


# ==========================================
# MINIMAX ALGORITHM
# ==========================================
def minimax(board, depth, is_maximizing):
    result = check_winner(board)

    if result == "O":
        return 10 - depth
    if result == "X":
        return depth - 10
    if result == "Draw":
        return 0

    if is_maximizing:
        best_score = float("-inf")

        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, depth + 1, False)
                board[i] = ""
                best_score = max(best_score, score)

        return best_score

    best_score = float("inf")

    for i in range(9):
        if board[i] == "":
            board[i] = "X"
            score = minimax(board, depth + 1, True)
            board[i] = ""
            best_score = min(best_score, score)

    return best_score


# ==========================================
# FIND THE BEST MINIMAX MOVE
# ==========================================
def best_minimax_move(board):
    best_score = float("-inf")
    best_moves = []

    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, 0, False)
            board[i] = ""

            if score > best_score:
                best_score = score
                best_moves = [i]
            elif score == best_score:
                best_moves.append(i)

    return random.choice(best_moves) if best_moves else None


# ==========================================
# AI MOVE - EASY / MEDIUM / HARD
# ==========================================
def ai_move():
    board = st.session_state.board
    empty_positions = [i for i in range(9) if board[i] == ""]

    if not empty_positions:
        return

    difficulty = st.session_state.difficulty

    if difficulty == "Easy":
        # Easy: AI selects any available square randomly.
        move = random.choice(empty_positions)

    elif difficulty == "Medium":
        # Medium: AI uses Minimax 60% of the time,
        # and makes a random move 40% of the time.
        if random.random() < 0.40:
            move = random.choice(empty_positions)
        else:
            move = best_minimax_move(board)

    else:
        # Hard: AI always uses the complete Minimax algorithm.
        move = best_minimax_move(board)

    if move is not None:
        board[move] = "O"


# ==========================================
# HUMAN MOVE AND GAME RESULT
# ==========================================
def human_move(position):
    if st.session_state.game_over:
        return

    board = st.session_state.board

    if board[position] != "":
        return

    # Human plays X.
    board[position] = "X"

    result = check_winner(board)

    if result == "X":
        st.session_state.winner = "X"
        st.session_state.game_over = True
        st.session_state.message = "🎉 Congratulations! You won!"
        return

    if result == "Draw":
        st.session_state.winner = "Draw"
        st.session_state.game_over = True
        st.session_state.message = "🤝 It's a draw!"
        return

    # AI plays O after the human move.
    ai_move()

    result = check_winner(board)

    if result == "O":
        st.session_state.winner = "O"
        st.session_state.game_over = True
        st.session_state.message = "🤖 AI wins! Better luck next time!"
    elif result == "Draw":
        st.session_state.winner = "Draw"
        st.session_state.game_over = True
        st.session_state.message = "🤝 It's a draw!"
    else:
        st.session_state.message = "Your turn! Choose a box."


# ==========================================
# APPLICATION TITLE
# ==========================================
st.markdown(
    "<h1 style='text-align:center;color:black;'>🎮 X TIC TAC TOE O 🎮</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center;font-size:17px;'>"
    "✨ Challenge the AI and test your strategy! ✨"
    "</p>",
    unsafe_allow_html=True
)

# ==========================================
# DIFFICULTY SELECTION
# IMPORTANT: This appears BEFORE the board.
# When the selection changes, reset the game.
# ==========================================
st.markdown(
    "<h4 style='text-align:center;color:black;'>🎯 SELECT DIFFICULTY LEVEL</h4>",
    unsafe_allow_html=True
)

st.selectbox(
    "Choose your challenge:",
    ["Easy", "Medium", "Hard"],
    key="difficulty"
)

difficulty = st.session_state.difficulty

# This is the correct place for the difficulty-change check:
# immediately after the selectbox and before displaying the board.
if difficulty != st.session_state.previous_difficulty:
    st.session_state.previous_difficulty = difficulty
    new_game()
    st.rerun()

level_descriptions = {
    "Easy": "🟢 Easy: The AI makes random moves.",
    "Medium": "🟣 Medium: The AI mixes Minimax and random moves.",
    "Hard": "🔴 Hard: The AI uses optimal Minimax strategy."
}
st.caption(level_descriptions[difficulty])

# ==========================================
# GAME STATUS
# ==========================================
st.info(st.session_state.message)

st.markdown(
    "<h4 style='text-align:center;color:black;'>"
    "👤 YOU: X&nbsp;&nbsp;&nbsp;&nbsp;🤖 AI: O"
    "</h4>",
    unsafe_allow_html=True
)
st.markdown(
    "<h3 style='text-align:center;color:black;'>Choose Your Square</h3>",
    unsafe_allow_html=True
)

# ==========================================
# TIC TAC TOE BOARD - 3 x 3
# ==========================================
for row in range(3):
    columns = st.columns(3, gap="small")

    for col in range(3):
        position = row * 3 + col

        with columns[col]:
            value = st.session_state.board[position]
            label = value if value else " "

            if st.button(
                label,
                key=f"box_{position}",
                use_container_width=True,
                disabled=st.session_state.game_over or value != ""
            ):
                human_move(position)
                st.rerun()

# ==========================================
# WIN CELEBRATION
# ==========================================
if st.session_state.winner == "X":
    st.balloons()
    st.success("🏆 YOU WON! AMAZING PERFORMANCE!")

elif st.session_state.winner == "O":
    st.snow()
    st.warning("🤖 AI WON! TRY AGAIN!")

elif st.session_state.winner == "Draw":
    st.info("🤝 WELL PLAYED! IT'S A DRAW!")

# ==========================================
# NEW GAME BUTTON
# ==========================================
st.write("")
left, center, right = st.columns([1, 2, 1])

with center:
    if st.button(
        "🔄 NEW GAME",
        type="primary",
        use_container_width=True
    ):
        new_game()
        st.rerun()

# ==========================================
# FOOTER
# ==========================================
st.divider()
st.markdown(
    "<p style='text-align:center;font-weight:bold;'>"
    "💜 Made with Python & Streamlit 💗<br>"
    "Think Smart • Play Smart • Win Smart<br>"
    "Developed by Ilavarasi Devi"
    "</p>",
    unsafe_allow_html=True
)
