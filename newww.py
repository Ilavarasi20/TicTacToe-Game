import random
import streamlit as st

# -------------------- Page Configuration --------------------
st.set_page_config(
    page_title="Tic-Tac-Toe with AI",
    page_icon="🎮",
    layout="centered"
)

# -------------------- Pastel UI --------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(
        135deg,
        #fce4ec,
        #e6ccff,
        #f8dfff
    );
    color: #32105f;
}

/* Main container */
.block-container {
    max-width: 1050px;
    padding-top: 1.5rem;
}

/* Header */
.hero {
    text-align: center;
    padding: 8px 0 18px;
}

.hero h1 {
    color: #5b16a6;
    font-size: clamp(2.2rem, 5vw, 3.8rem);
    font-weight: 900;
    margin: 0;
}

.hero p {
    color: #7628a9;
    font-size: 1.15rem;
    font-weight: 600;
    margin-top: 4px;
}

/* -------------------- Game Board -------------------- */

/* Keep board columns in a single row */
.st-key-gameboard [data-testid="stHorizontalBlock"] {
    flex-wrap: nowrap !important;
    gap: 8px !important;
}

/* Equal width for all 3 columns */
.st-key-gameboard [data-testid="column"] {
    min-width: 0 !important;
    flex: 1 1 0% !important;
    width: 33.33% !important;
}

/* Square XO boxes */
.st-key-gameboard div[data-testid="stButton"] button {
    width: 100% !important;
    aspect-ratio: 1 / 1 !important;
    min-height: 0 !important;
    height: auto !important;

    padding: 0 !important;

    border-radius: 18px !important;
    border: 2px solid #d5b4f5 !important;

    background: linear-gradient(
        145deg,
        #fffaff,
        #f5eaff
    ) !important;

    color: #6515a9 !important;

    font-size: clamp(2rem, 7vw, 3.2rem) !important;
    font-weight: 900 !important;

    box-shadow: 0 6px 14px
        rgba(118, 84, 169, 0.14);

    transition: transform .12s ease;
}

/* Hover effect */
.st-key-gameboard div[data-testid="stButton"] button:hover {
    border-color: #a855e8 !important;
    transform: translateY(-2px);
}

/* XO symbols */
.st-key-gameboard div[data-testid="stButton"] button p {
    font-size: clamp(2rem, 7vw, 3.2rem) !important;
    font-weight: 900 !important;
}


      
/* Hover */
div[data-testid="stButton"] button:hover {
    border-color: #a855e8;

    box-shadow: 0 8px 20px
        rgba(118, 84, 169, 0.22);

    transform: translateY(-2px);
}

/* Button text */
div[data-testid="stButton"] button p {
    font-size: 3.2rem !important;
    font-weight: 900 !important;
}

/* Disabled buttons */
div[data-testid="stButton"] button:disabled {
    opacity: 1;
    color: #6b21a8;
    background: #fffaff;
}

/* -------------------- Score Cards -------------------- */
.score-card {
    background: rgba(255, 255, 255, 0.85);
    border: 2px solid #d9baf6;
    border-radius: 18px;
    padding: 13px 8px;
    text-align: center;

    box-shadow: 0 6px 18px
        rgba(118, 84, 169, 0.10);
}

.score-card .label {
    font-weight: 800;
    font-size: 16px;
    color: #6b21a8;
}

.score-card .score {
    font-size: 30px;
    font-weight: 900;
    color: #38106d;
}

/* -------------------- Status -------------------- */
.status {
    text-align: center;

    background: #fff2ff;

    border: 2px solid #d5b4f5;

    color: #6b21a8;

    border-radius: 22px;

    padding: 15px;

    font-weight: 800;

    margin: 12px 0 18px;
}

/* Difficulty label */
div[data-testid="stSelectbox"] label {
    color: #5b218b;
    font-weight: 800;
}

/* Difficulty dropdown */
div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    border-radius: 14px;
}

/* Restart and reset buttons */
div[data-testid="stButton"] button[kind="secondary"] {
    min-height: 55px;
    font-size: 1rem !important;
    font-weight: 800;
    border-radius: 25px;
}

/* Hide Streamlit menu */
#MainMenu {
    visibility: hidden;
}

/* Hide footer */
footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# -------------------- Game Rules --------------------

WIN_LINES = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),

    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),

    (0, 4, 8),
    (2, 4, 6)
]


# -------------------- Winner Function --------------------

def winner(board):

    for a, b, c in WIN_LINES:

        if (
            board[a]
            and board[a] == board[b] == board[c]
        ):

            return board[a]

    return None


# -------------------- Available Moves --------------------

def available(board):

    return [
        i
        for i, cell in enumerate(board)
        if cell == ""
    ]


# -------------------- Minimax Algorithm --------------------

def minimax(board, is_ai_turn, depth=0):

    result = winner(board)

    if result == "O":
        return 10 - depth

    if result == "X":
        return depth - 10

    if not available(board):
        return 0

    # AI maximizes score
    if is_ai_turn:

        best = -100

        for spot in available(board):

            board[spot] = "O"

            score = minimax(
                board,
                False,
                depth + 1
            )

            board[spot] = ""

            best = max(best, score)

        return best

    # Player minimizes score
    else:

        best = 100

        for spot in available(board):

            board[spot] = "X"

            score = minimax(
                board,
                True,
                depth + 1
            )

            board[spot] = ""

            best = min(best, score)

        return best


# -------------------- AI Move --------------------

def ai_move(board, difficulty):

    moves = available(board)

    if not moves:
        return None

    # Easy: Random move
    if difficulty == "Easy":

        return random.choice(moves)

    # Check winning or blocking move
    for mark in ("O", "X"):

        for spot in moves:

            board[spot] = mark

            won = winner(board) == mark

            board[spot] = ""

            if won:

                return spot

    # Medium: Strategic moves
    if difficulty == "Medium":

        # Center
        if 4 in moves:

            return 4

        # Corners
        corners = [
            i
            for i in (0, 2, 6, 8)
            if i in moves
        ]

        if corners:

            return random.choice(corners)

        return random.choice(moves)

    # Hard: Minimax
    best_score = -100

    best_moves = []

    for spot in moves:

        board[spot] = "O"

        score = minimax(
            board,
            False,
            1
        )

        board[spot] = ""

        if score > best_score:

            best_score = score

            best_moves = [spot]

        elif score == best_score:

            best_moves.append(spot)

    return random.choice(best_moves)


# -------------------- Reset Round --------------------

def reset_round():

    st.session_state.board = [""] * 9

    st.session_state.game_over = False

    st.session_state.winner = None

    st.session_state.status = (
        "✨ Your turn! Tap an empty box."
    )


# -------------------- Reset Scores --------------------

def reset_scores():

    st.session_state.scores = {
        "X": 0,
        "O": 0,
        "Draw": 0
    }

    reset_round()


# -------------------- Session State --------------------

if "board" not in st.session_state:

    st.session_state.board = [""] * 9


if "game_over" not in st.session_state:

    st.session_state.game_over = False


if "winner" not in st.session_state:

    st.session_state.winner = None


if "scores" not in st.session_state:

    st.session_state.scores = {
        "X": 0,
        "O": 0,
        "Draw": 0
    }


if "status" not in st.session_state:

    st.session_state.status = (
        "✨ Your turn! Tap an empty box."
    )


if "celebrated" not in st.session_state:

    st.session_state.celebrated = False


# -------------------- Start-Up Snow Effect --------------------

if "snow_started" not in st.session_state:

    st.session_state.snow_started = True

    st.snow()


# -------------------- Header --------------------

st.markdown("""
<div class="hero">
<div style="font-size:3rem">X🏆O</div>
<h1>Tic-Tac-Toe with AI 🤖</h1>
<p>A little strategy, a little luck, and a lovely challenge ✨</p>
</div>
""", unsafe_allow_html=True)


# -------------------- Difficulty and Scores --------------------

left, you_col, ai_col, draw_col = st.columns(
    [1.7, 1, 1, 1]
)

with left:

    difficulty = st.selectbox(
        "🤖 Choose Computer Difficulty 🎯Start with Easy🤗",
        ["Easy", "Medium", "Hard"],
        index=1
    )


with you_col:

    st.markdown(
        f"""
<div class="score-card">
<div class="label">👤 You (X)</div>
<div class="score">{st.session_state.scores["X"]}</div>
</div>
""",
        unsafe_allow_html=True
    )


with ai_col:

    st.markdown(
        f"""
<div class="score-card">
<div class="label">🤖 AI (O)</div>
<div class="score">{st.session_state.scores["O"]}</div>
</div>
""",
        unsafe_allow_html=True
    )


with draw_col:

    st.markdown(
        f"""
<div class="score-card">
<div class="label">🤝 Draws</div>
<div class="score">{st.session_state.scores["Draw"]}</div>
</div>
""",
        unsafe_allow_html=True
    )


# -------------------- Game Status --------------------

st.markdown(
    f"""
<div class="status">
{st.session_state.status}
</div>
""",
    unsafe_allow_html=True
)


# -------------------- Board --------------------

with st.container(key="gameboard"):

    for row in range(3):

        cols = st.columns(3, gap="small")

        for col in range(3):

            idx = row * 3 + col

            value = st.session_state.board[idx]

        # Symbol
            if value == "X":

                label = "✕"

            elif value == "O":

                label = "◯"

            else:

                label = " "

            with cols[col]:

                clicked = st.button(
                label,
                key=f"cell_{idx}",
                use_container_width=True,
                disabled=(
                    st.session_state.game_over
                    or bool(value)
                )
            )

            if clicked:

            # -------------------- Human Move --------------------

                st.session_state.board[idx] = "X"

                human_won = winner(
                st.session_state.board
            )

            # Player wins
                if human_won:

                    st.session_state.game_over = True

                    st.session_state.winner = "X"

                    st.session_state.scores["X"] += 1

                    st.session_state.status = (
                    "🎉 You won! Amazing move!"
                )

                    st.session_state.celebrated = True

            # Draw
                elif not available(
                    st.session_state.board
            ):

                    st.session_state.game_over = True

                    st.session_state.winner = "Draw"

                    st.session_state.scores["Draw"] += 1

                    st.session_state.status = (
                    "🤝 It's a draw! Great game."
                )

            # -------------------- AI Move --------------------

                 else:

                     move = ai_move(
                     st.session_state.board,
                     difficulty
                )

                      if move is not None:

                          st.session_state.board[move] = "O"

                           ai_won = winner(
                           st.session_state.board
                )

                # AI wins
                        if ai_won:

                            st.session_state.game_over = True

                            st.session_state.winner = "O"
    
                            st.session_state.scores["O"] += 1

                            st.session_state.status = (
                        "🤖 AI won this round. Try again!"
                    )

                # Draw after AI move
                        elif not available(
                            st.session_state.board
                ):

                            st.session_state.game_over = True

                            st.session_state.winner = "Draw"

                            st.session_state.scores["Draw"] += 1

                            st.session_state.status = (
                        "🤝 It's a draw! Great game."
                    )

                # Continue
                        else:

                            st.session_state.status = (
                        "🤖 AI played. Your turn!"
                    )

            # Refresh board
                            st.rerun()


# -------------------- Winner Celebration --------------------

if (
    st.session_state.winner == "X"
    and st.session_state.celebrated
):

    st.balloons()

    st.session_state.celebrated = False


# -------------------- Controls --------------------

new_col, reset_col = st.columns(2)

with new_col:

    if st.button(
        "🔄 Start New Round",
        use_container_width=True
    ):

        reset_round()

        st.session_state.celebrated = False

        st.rerun()


with reset_col:

    if st.button(
        "🧹 Reset Scores",
        use_container_width=True
    ):

        reset_scores()

        st.session_state.celebrated = False

        st.rerun()


# -------------------- Footer --------------------

st.markdown("""
<div style="text-align:center;color:#8755b5;font-weight:600;margin-top:18px">
Made with Streamlit and a little minimax magic 💜
</div>
""", unsafe_allow_html=True)
