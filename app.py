"""
Luncheon Quiz - A Streamlit quiz application for live university events.
Supports multiple concurrent users with Firebase Firestore backend.
"""

import streamlit as st
from questions import get_questions, get_question_count
from firebase import init_firebase, save_score, get_leaderboard

# Page configuration
st.set_page_config(
    page_title="Luncheon Quiz",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Outfit', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2.5rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .main-header h1 {
        color: #e94560;
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: #a2d2ff;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    .question-card {
        background: linear-gradient(145deg, #1e1e2f, #252540);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #e94560;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .question-number {
        color: #e94560;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .question-text {
        color: #ffffff;
        font-size: 1.15rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    
    .score-display {
        background: linear-gradient(135deg, #e94560 0%, #ff6b6b 100%);
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(233, 69, 96, 0.4);
    }
    
    .score-display h2 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .score-display p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    .leaderboard-container {
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        padding: 1.5rem;
        border-radius: 16px;
        margin-top: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .leaderboard-title {
        color: #ffd700;
        font-size: 1.5rem;
        font-weight: 600;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .leaderboard-entry {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
        transition: transform 0.2s;
    }
    
    .leaderboard-entry:hover {
        transform: translateX(5px);
        background: rgba(255,255,255,0.08);
    }
    
    .rank-1 { border-left: 3px solid #ffd700; }
    .rank-2 { border-left: 3px solid #c0c0c0; }
    .rank-3 { border-left: 3px solid #cd7f32; }
    
    .rank-badge {
        font-weight: 700;
        font-size: 1.1rem;
        min-width: 35px;
    }
    
    .rank-1 .rank-badge { color: #ffd700; }
    .rank-2 .rank-badge { color: #c0c0c0; }
    .rank-3 .rank-badge { color: #cd7f32; }
    
    .player-name {
        color: #ffffff;
        font-weight: 500;
        flex-grow: 1;
        margin-left: 1rem;
    }
    
    .player-score {
        color: #e94560;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #e94560 0%, #ff6b6b 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(233, 69, 96, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(233, 69, 96, 0.5);
    }
    
    .stTextInput > div > div > input {
        background: #1e1e2f;
        border: 2px solid #3a3a5c;
        color: white;
        border-radius: 8px;
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #e94560;
        box-shadow: 0 0 10px rgba(233, 69, 96, 0.3);
    }
    
    .stRadio > div {
        background: transparent;
    }
    
    .stRadio > div > label {
        color: #a0a0c0 !important;
        padding: 0.5rem;
        border-radius: 6px;
        transition: all 0.2s;
    }
    
    div[data-testid="stForm"] {
        background: transparent;
        border: none;
        padding: 0;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if "submitted" not in st.session_state:
        st.session_state.submitted = False
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "answers" not in st.session_state:
        st.session_state.answers = {}


def render_header():
    """Render the app header."""
    st.markdown("""
    <div class="main-header">
        <h1>🎓 Luncheon Quiz</h1>
        <p>Test your knowledge • Compete with peers • Win bragging rights!</p>
    </div>
    """, unsafe_allow_html=True)


def render_question(idx: int, question: dict) -> str:
    """Render a single question and return the selected answer."""
    st.markdown(f"""
    <div class="question-card">
        <div class="question-number">Question {idx + 1}</div>
        <div class="question-text">{question['text']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    answer = st.radio(
        label=f"Q{idx + 1}",
        options=question["options"],
        key=f"q_{idx}",
        label_visibility="collapsed"
    )
    return answer


def calculate_score(questions: list, answers: dict) -> int:
    """Calculate the quiz score based on answers."""
    score = 0
    for idx, question in enumerate(questions):
        user_answer = answers.get(f"q_{idx}")
        if user_answer and user_answer == question["options"][question["correct_answer"]]:
            score += 1
    return score


def render_score(score: int, total: int):
    """Render the score display."""
    percentage = (score / total) * 100
    
    if percentage == 100:
        message = "🏆 Perfect Score! You're a genius!"
    elif percentage >= 80:
        message = "🌟 Excellent work! Almost perfect!"
    elif percentage >= 60:
        message = "👍 Good job! Well done!"
    elif percentage >= 40:
        message = "📚 Not bad! Keep learning!"
    else:
        message = "💪 Better luck next time!"
    
    st.markdown(f"""
    <div class="score-display">
        <h2>{score} / {total}</h2>
        <p>{message}</p>
    </div>
    """, unsafe_allow_html=True)


def render_leaderboard(db):
    """Render the leaderboard section."""
    st.markdown('<div class="leaderboard-title">🏆 Leaderboard</div>', unsafe_allow_html=True)
    
    leaderboard = get_leaderboard(db)
    
    if not leaderboard:
        st.info("No scores yet. Be the first to complete the quiz!")
        return
    
    for rank, entry in enumerate(leaderboard, 1):
        rank_class = f"rank-{rank}" if rank <= 3 else ""
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
        
        st.markdown(f"""
        <div class="leaderboard-entry {rank_class}">
            <span class="rank-badge">{medal}</span>
            <span class="player-name">{entry['username']}</span>
            <span class="player-score">{entry['score']} pts</span>
        </div>
        """, unsafe_allow_html=True)


def main():
    """Main application entry point."""
    init_session_state()
    render_header()
    
    # Initialize Firebase
    db = init_firebase()
    
    # If already submitted, show results
    if st.session_state.submitted:
        st.success(f"✅ Quiz completed, {st.session_state.username}!")
        render_score(st.session_state.score, get_question_count())
        
        st.markdown("---")
        render_leaderboard(db)
        
        # Option to view leaderboard refresh
        if st.button("🔄 Refresh Leaderboard"):
            st.rerun()
        return
    
    # Username input
    st.markdown("### 👤 Enter Your Name")
    username = st.text_input(
        "Username",
        placeholder="Your display name for the leaderboard",
        label_visibility="collapsed",
        max_chars=30
    )
    
    if not username.strip():
        st.warning("Please enter your name to start the quiz.")
        st.stop()
    
    st.session_state.username = username.strip()
    
    st.markdown("---")
    st.markdown("### 📝 Quiz Questions")
    
    questions = get_questions()
    
    # Render all questions
    with st.form("quiz_form"):
        answers = {}
        for idx, question in enumerate(questions):
            answers[f"q_{idx}"] = render_question(idx, question)
            if idx < len(questions) - 1:
                st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("🚀 Submit Quiz", use_container_width=True)
    
    if submitted:
        # Calculate score
        score = calculate_score(questions, answers)
        
        # Save to Firestore
        if save_score(db, st.session_state.username, score):
            st.session_state.submitted = True
            st.session_state.score = score
            st.session_state.answers = answers
            st.rerun()
        else:
            st.error("Failed to submit quiz. Please try again.")


if __name__ == "__main__":
    main()
