import streamlit as st
import random

st.title("🟩🟨⬜ Simple Wordle Game")

# Small set of 5-letter words
WORD_LIST = ["apple", "grape", "light", "chair", "bread", "smile", "trace", "flame"]

# Initialize game state
if "secret" not in st.session_state:
    st.session_state.secret = random.choice(WORD_LIST)

if "guesses" not in st.session_state:
    st.session_state.guesses = []

if "finished" not in st.session_state:
    st.session_state.finished = False


def check_guess(guess, secret):
    """Return list of tile colors for the guess."""
    result = ["gray"] * 5
    secret_remaining = list(secret)

    # First pass: check green
    for i in range(5):
        if guess[i] == secret[i]:
            result[i] = "green"
            secret_remaining[i] = None  # remove matched letter

    # Second pass: check yellow
    for i in range(5):
        if result[i] == "gray" and guess[i] in secret_remaining:
            result[i] = "yellow"
            secret_remaining[secret_remaining.index(guess[i])] = None

    return result


# User input
guess = st.text_input("Enter a 5-letter word:", max_chars=5).lower()

if st.button("Submit Guess") and not st.session_state.finished:
    if len(guess) != 5 or not guess.isalpha():
        st.warning("Please enter a valid 5-letter word.")
    else:
        st.session_state.guesses.append(guess)

        # Check win/lose
        if guess == st.session_state.secret:
            st.success(f"🎉 Correct! The word was **{st.session_state.secret}**.")
            st.session_state.finished = True
        elif len(st.session_state.guesses) >= 6:
            st.error(f"❌ Out of guesses! The word was **{st.session_state.secret}**.")
            st.session_state.finished = True


# Display guesses with color-coded tiles
for guess in st.session_state.guesses:
    colors = check_guess(guess, st.session_state.secret)
    cols = st.columns(5)

    for i, col in enumerate(cols):
        col.markdown(
            f"""
            <div style="
                background-color:{'lightgreen' if colors[i]=='green' else
                                  'gold' if colors[i]=='yellow' else
                                  'lightgray'};
                border-radius:5px;
                padding:10px;
                text-align:center;
                font-size:24px;
                font-weight:bold;
                width:50px;">
                {guess[i].upper()}
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("---")

# Restart game
if st.button("🔄 Restart Game"):
    st.session_state.secret = random.choice(WORD_LIST)
    st.session_state.guesses = []
    st.session_state.finished = False
    st.info("New game started!")
