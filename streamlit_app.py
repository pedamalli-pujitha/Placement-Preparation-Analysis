import streamlit as st
import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash
# ============================================================
# PASTEL ANIMATED UI THEME
# ============================================================

def apply_wave_background():

    st.markdown(
        """
        <style>

        /* =====================================================
           MAIN APPLICATION BACKGROUND
           ===================================================== */

        .stApp {

            background:

                radial-gradient(
                    ellipse at 15% 20%,
                    rgba(190, 215, 255, 0.85),
                    transparent 42%
                ),

                radial-gradient(
                    ellipse at 85% 25%,
                    rgba(220, 205, 255, 0.80),
                    transparent 42%
                ),

                radial-gradient(
                    ellipse at 25% 85%,
                    rgba(190, 240, 235, 0.85),
                    transparent 45%
                ),

                radial-gradient(
                    ellipse at 85% 80%,
                    rgba(205, 195, 255, 0.75),
                    transparent 45%
                ),

                linear-gradient(
                    135deg,
                    #eef5ff,
                    #f5f0ff,
                    #ecfbf8
                );

            background-size:
                180% 180%,
                200% 200%,
                180% 180%,
                200% 200%,
                400% 400%;

            animation:
                softBackground 35s ease-in-out infinite alternate;

            min-height: 100vh;
        }


        /* =====================================================
           SLOW SOFT WAVE 1
           ===================================================== */

        .stApp::before {

            content: "";

            position: fixed;

            width: 150%;
            height: 150%;

            top: -25%;
            left: -25%;

            background:

                radial-gradient(
                    ellipse at center,
                    rgba(150, 210, 255, 0.25),
                    transparent 48%
                );

            filter: blur(80px);

            pointer-events: none;

            animation:
                softWaveOne 40s ease-in-out infinite alternate;

            z-index: 0;
        }


        /* =====================================================
           SLOW SOFT WAVE 2
           ===================================================== */

        .stApp::after {

            content: "";

            position: fixed;

            width: 150%;
            height: 150%;

            top: -25%;
            left: -25%;

            background:

                radial-gradient(
                    ellipse at center,
                    rgba(200, 180, 255, 0.22),
                    transparent 48%
                );

            filter: blur(100px);

            pointer-events: none;

            animation:
                softWaveTwo 45s ease-in-out infinite alternate;

            z-index: 0;
        }


        /* =====================================================
           KEEP CONTENT ABOVE BACKGROUND
           ===================================================== */

        .main,
        section[data-testid="stSidebar"] {

            position: relative;

            z-index: 1;
        }


        /* =====================================================
           MAIN BACKGROUND ANIMATION
           ===================================================== */

        @keyframes softBackground {

            0% {

                background-position:
                    0% 20%,
                    100% 20%,
                    20% 100%,
                    100% 100%,
                    0% 50%;
            }

            50% {

                background-position:
                    45% 60%,
                    40% 80%,
                    80% 30%,
                    20% 40%,
                    50% 50%;
            }

            100% {

                background-position:
                    100% 80%,
                    0% 50%,
                    50% 0%,
                    0% 20%,
                    100% 50%;
            }
        }


        /* =====================================================
           WAVE ANIMATION 1
           ===================================================== */

        @keyframes softWaveOne {

            0% {

                transform:
                    translate(-8%, -5%)
                    scale(1);
            }

            50% {

                transform:
                    translate(8%, 5%)
                    rotate(2deg)
                    scale(1.08);
            }

            100% {

                transform:
                    translate(-3%, 8%)
                    rotate(-2deg)
                    scale(1.12);
            }
        }


        /* =====================================================
           WAVE ANIMATION 2
           ===================================================== */

        @keyframes softWaveTwo {

            0% {

                transform:
                    translate(8%, 5%)
                    scale(1.03);
            }

            50% {

                transform:
                    translate(-7%, -6%)
                    rotate(-2deg)
                    scale(1.10);
            }

            100% {

                transform:
                    translate(5%, 7%)
                    rotate(2deg)
                    scale(1.08);
            }
        }


        /* =====================================================
           PASTEL SIDEBAR
           ===================================================== */

        section[data-testid="stSidebar"] {

            background:

                linear-gradient(
                    180deg,
                    rgba(238, 246, 255, 0.96),
                    rgba(246, 240, 255, 0.96),
                    rgba(235, 250, 247, 0.96)
                ) !important;

            border-right:
                1px solid
                rgba(180, 195, 220, 0.35) !important;

            box-shadow:
                5px 0 25px
                rgba(100, 120, 160, 0.08);

            backdrop-filter:
                blur(20px);
        }


        /* Sidebar normal text */

        section[data-testid="stSidebar"] p {

            color:
                #536174 !important;

        }


        /* Sidebar headings */

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {

            color:
                #39465a !important;

        }


        /* Sidebar navigation */

        section[data-testid="stSidebar"]
        label {

            color:
                #4d596b !important;

            font-weight:
                500;

        }


        /* Sidebar navigation hover */

        section[data-testid="stSidebar"]
        label:hover {

            background:
                rgba(180, 205, 255, 0.25);

            border-radius:
                10px;

        }


        /* =====================================================
           HEADINGS
           ===================================================== */

        h1,
        h2,
        h3 {

            color:
                #344054 !important;

            text-shadow:
                none !important;

        }


        /* =====================================================
           NORMAL TEXT
           ===================================================== */

        p {

            color:
                #566273;

        }


        label {

            color:
                #566273 !important;

        }


        /* =====================================================
           GLASS METRIC CARDS
           ===================================================== */

        div[data-testid="stMetric"] {

            background:
                rgba(255, 255, 255, 0.70) !important;

            backdrop-filter:
                blur(18px);

            -webkit-backdrop-filter:
                blur(18px);

            border:
                1px solid
                rgba(255, 255, 255, 0.85) !important;

            border-radius:
                20px;

            padding:
                18px;

            box-shadow:
                0 8px 30px
                rgba(100, 120, 160, 0.10);

            transition:
                all 0.3s ease;

        }


        div[data-testid="stMetric"]:hover {

            transform:
                translateY(-3px);

            box-shadow:
                0 12px 35px
                rgba(100, 120, 160, 0.16);

        }


        /* Metric value */

        div[data-testid="stMetricValue"] {

            color:
                #344054 !important;

            text-shadow:
                none !important;

        }


        /* Metric label */

        div[data-testid="stMetricLabel"] {

            color:
                #667085 !important;

        }


        /* =====================================================
           BUTTONS
           ===================================================== */

        .stButton > button {

            background:

                linear-gradient(
                    90deg,
                    #91b9f7,
                    #9bcfc8
                ) !important;

            color:
                white !important;

            border:
                none !important;

            border-radius:
                12px !important;

            font-weight:
                600 !important;

            padding:
                8px 22px;

            box-shadow:
                0 6px 18px
                rgba(120, 160, 200, 0.18);

            transition:
                all 0.25s ease;

        }


        .stButton > button:hover {

            background:

                linear-gradient(
                    90deg,
                    #83adf3,
                    #89c6be
                ) !important;

            transform:
                translateY(-2px);

            box-shadow:
                0 10px 24px
                rgba(120, 160, 200, 0.25);

        }


        /* =====================================================
           TEXT INPUTS
           ===================================================== */

        div[data-baseweb="input"] {

            background:
                rgba(255, 255, 255, 0.78) !important;

            border:
                1px solid
                rgba(190, 200, 215, 0.65) !important;

            border-radius:
                12px !important;

        }


        div[data-baseweb="input"]:focus-within {

            border:
                1px solid
                #a7bfdc !important;

            box-shadow:
                0 0 12px
                rgba(150, 180, 220, 0.18) !important;

        }


        input {

            color:
                #344054 !important;

        }


        textarea {

            color:
                #344054 !important;

        }


        /* =====================================================
           PROGRESS BAR
           ===================================================== */

        div[data-testid="stProgress"] {

            background:
                rgba(220, 225, 235, 0.65) !important;

            border-radius:
                20px;

        }


        div[data-testid="stProgress"] > div > div {

            background:

                linear-gradient(
                    90deg,
                    #9dbcf0,
                    #9bd5cd
                ) !important;

            border-radius:
                20px;

        }


        /* =====================================================
           RADIO OPTIONS
           ===================================================== */

        div[role="radiogroup"] label {

            color:
                #4d5968 !important;

        }


        /* =====================================================
           SELECT BOX
           ===================================================== */

        div[data-baseweb="select"] {

            background:
                rgba(255, 255, 255, 0.75) !important;

            border-radius:
                12px !important;

        }


        /* =====================================================
           ALERTS
           ===================================================== */

        div[data-testid="stAlert"] {

            border-radius:
                14px;

            border:
                1px solid
                rgba(200, 210, 225, 0.65);

        }


        /* =====================================================
           DIVIDERS
           ===================================================== */

        hr {

            border-color:
                rgba(190, 200, 215, 0.45) !important;

        }


        /* =====================================================
           DATAFRAME / TABLE
           ===================================================== */

        div[data-testid="stDataFrame"] {

            border-radius:
                15px;

            overflow:
                hidden;

        }


        /* =====================================================
           EXPANDER
           ===================================================== */

        details {

            background:
                rgba(255, 255, 255, 0.55);

            border:
                1px solid
                rgba(210, 215, 225, 0.60);

            border-radius:
                14px;

        }


        </style>
        """,

        unsafe_allow_html=True
    )


# ============================================================
# APPLY THE THEME
# ============================================================

apply_wave_background()  
# ---------------- DATABASE ----------------

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "instance" / "placement.db"


def get_db():
    return sqlite3.connect(DB_PATH)
# ============================================================
# UPDATE STUDENT TABLE
# ============================================================

def update_student_table():

    conn = get_db()

    existing_columns = conn.execute(
        "PRAGMA table_info(student)"
    ).fetchall()

    existing_names = [
        column[1]
        for column in existing_columns
    ]

    new_columns = {
        "college_place": "TEXT",
        "pincode": "TEXT",
        "district": "TEXT",
        "joining_year": "INTEGER",
        "passedout_year": "INTEGER"
    }

    for column_name, column_type in new_columns.items():

        if column_name not in existing_names:

            conn.execute(
                f"""
                ALTER TABLE student
                ADD COLUMN {column_name} {column_type}
                """
            )

    conn.commit()
    conn.close()


update_student_table()

def get_student(email):
    conn = get_db()

    student = conn.execute(
        """
        SELECT id, name, email, college, branch, password,
               COALESCE(python_score, 0),
               COALESCE(aptitude_score, 0)
        FROM student
        WHERE email = ?
        """,
        (email,)
    ).fetchone()

    conn.close()
    return student

def save_assessment_result(student_id, assessment_type, score, total):

    percentage = int((score / total) * 100)

    conn = get_db()

    if assessment_type == "Python":

        conn.execute(
            """
            UPDATE student
            SET python_score = ?
            WHERE id = ?
            """,
            (percentage, student_id)
        )

    elif assessment_type == "Aptitude":

        conn.execute(
            """
            UPDATE student
            SET aptitude_score = ?
            WHERE id = ?
            """,
            (percentage, student_id)
        )

    conn.execute(
        """
        INSERT INTO assessment_attempt
        (
            student_id,
            assessment_type,
            score,
            total,
            percentage
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            student_id,
            assessment_type,
            score,
            total,
            percentage
        )
    )

    conn.commit()
    conn.close()

    return percentage
# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Smart Placement Preparation",
    page_icon="🎓",
    layout="wide"
)
# ---------------- SESSION ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "Login"


# ---------------- LOGIN ----------------

def login_page():

    st.title("🎓 Smart Placement Preparation Platform")

    st.subheader("Student Login")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if not email or not password:
            st.warning("Please enter email and password.")

        else:

            student = get_student(email)

            if student:

                if check_password_hash(
                    student[5],
                    password
                ):

                    st.session_state.logged_in = True
                    st.session_state.email = email
                    st.session_state.page = "Dashboard"

                    st.rerun()

                else:
                    st.error("Incorrect password.")

            else:
                st.error("User not found.")


# ---------------- REGISTER ----------------

def register_page():

    st.title("Student Registration")

    name = st.text_input("Full Name")

    email = st.text_input("Email")

    college = st.text_input("College")

    branch = st.text_input("Branch")

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("Register"):

        if not all([
            name,
            email,
            college,
            branch,
            password
        ]):

            st.warning("Please fill all fields.")

        elif password != confirm_password:

            st.error("Passwords do not match.")

        else:

            conn = get_db()

            existing = conn.execute(
                "SELECT id FROM student WHERE email=?",
                (email,)
            ).fetchone()

            if existing:

                st.error("Email already registered.")

            else:

                hashed_password = generate_password_hash(
                    password
                )

                conn.execute(
                    """
                    INSERT INTO student
                    (
                        name,
                        email,
                        college,
                        branch,
                        password,
                        python_score,
                        aptitude_score
                    )
                    VALUES (?, ?, ?, ?, ?, 0, 0)
                    """,
                    (
                        name,
                        email,
                        college,
                        branch,
                        hashed_password
                    )
                )

                conn.commit()
                conn.close()

                st.success(
                    "Registration successful. Please login."
                )
# ---------------- DASHBOARD ----------------

def dashboard():

    student = get_student(st.session_state.email)

    python_score = student[6]
    aptitude_score = student[7]

    overall = (python_score + aptitude_score) / 2

    # Test count
    completed = 0

    if python_score > 0:
        completed += 1

    if aptitude_score > 0:
        completed += 1

    # Career recommendation
    if python_score >= 80 and aptitude_score >= 70:
        role = "Python Developer"

    elif python_score >= 70 and aptitude_score >= 70:
        role = "Software Developer"

    elif aptitude_score >= 75:
        role = "Data Analyst"

    else:
        role = "Software Trainee"

    # Performance
    if overall >= 80:
        status = "Excellent 🎉"

    elif overall >= 60:
        status = "Good 👍"

    elif overall > 0:
        status = "Needs Improvement"

    else:
        status = "Not Started"

    # ---------------- PAGE TITLE ----------------

    st.title("Student Dashboard")

    st.write(
        f"### 👋 Welcome, {student[1]}!"
    )

    st.caption(
        "Smart Placement Preparation & Skill Assessment Platform"
    )

    st.divider()

    # ---------------- SCORE CARDS ----------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Python",
            f"{python_score}%"
        )

    with col2:

        st.metric(
            "Aptitude",
            f"{aptitude_score}%"
        )

    with col3:

        st.metric(
            "🎯 Overall",
            f"{overall:.0f}%"
        )

    with col4:

        st.metric(
            "📝 Tests",
            f"{completed}/2"
        )

    st.divider()

    # ---------------- SKILL OVERVIEW ----------------

    st.subheader("📈 Skill Overview")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"Python — **{python_score}%**"
        )

        st.progress(
            python_score / 100
        )

    with col2:

        st.write(
            f" Aptitude — **{aptitude_score}%**"
        )

        st.progress(
            aptitude_score / 100
        )

    st.divider()

    # ---------------- PERFORMANCE ----------------

    st.subheader("📊 Performance Status")

    if overall >= 80:

        st.success(
            f"{status} — Overall Score: {overall:.0f}%"
        )

    elif overall >= 60:

        st.info(
            f"{status} — Overall Score: {overall:.0f}%"
        )

    elif overall > 0:

        st.warning(
            f"{status} — Overall Score: {overall:.0f}%"
        )

    else:

        st.warning(
            "Please complete your assessments."
        )

    # ---------------- CAREER PATH ----------------

    st.subheader("🎯 Recommended Career Path")

    st.success(
        f"Recommended Role: **{role}**"
    )

    st.write(
        "This recommendation is based on your "
        "Python and Aptitude assessment performance."
    )

    st.divider()

    # ---------------- QUICK ACTIONS ----------------

    st.subheader("⚡ Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            "🐍 Python Assessment"
        )

    with col2:

        st.info(
            "🧠 Aptitude Assessment"
        )

    with col3:

        st.info(
            "📚 Preparation Plan"
        )
# ---------------- LOGOUT ----------------

def logout():

    st.session_state.logged_in = False

    st.session_state.email = None

    st.session_state.page = "Login"

    st.rerun()
# ---------------- PYTHON ASSESSMENT ----------------

def python_assessment():

    st.title("Python Assessment")

    questions = [
        {
            "question": "Which keyword is used to define a function in Python?",
            "options": ["function", "def", "define", "fun"],
            "answer": "def"
        },
        {
            "question": "Which data type stores True or False?",
            "options": ["int", "str", "bool", "float"],
            "answer": "bool"
        },
        {
            "question": "Which symbol is used for comments in Python?",
            "options": ["//", "#", "/*", "--"],
            "answer": "#"
        },
        {
            "question": "Which function finds the length of a list?",
            "options": ["size()", "length()", "len()", "count()"],
            "answer": "len()"
        },
        {
            "question": "Which one is a Python list?",
            "options": [
                "(1,2,3)",
                "[1,2,3]",
                "{1,2,3}",
                "<1,2,3>"
            ],
            "answer": "[1,2,3]"
        }
    ]

    score = 0

    answers = {}

    for i, q in enumerate(questions):

        st.write(
            f"### Q{i+1}. {q['question']}"
        )

        answers[i] = st.radio(
            "Select answer:",
            q["options"],
            key=f"python_{i}"
        )

    if st.button("Submit Python Assessment"):

        for i, q in enumerate(questions):

            if answers[i] == q["answer"]:
                score += 1

        percentage = int(
            (score / len(questions)) * 100
        )
        student = get_student(
            st.session_state.email
        )
        save_assessment_result(
            student[0],
            "Python",
            score,
            len(questions)
        )
        st.success(
            f"Python Score: {score}/{len(questions)}"
        )

        st.metric(
            "Percentage",
            f"{percentage}%"
        )    
# ---------------- APTITUDE ASSESSMENT ----------------

def aptitude_assessment():

    st.title("Aptitude Assessment")

    questions = [
        {
            "question": "What is 20% of 150?",
            "options": ["20", "25", "30", "35"],
            "answer": "30"
        },
        {
            "question": "If 5 pens cost ₹50, what is the cost of 1 pen?",
            "options": ["₹5", "₹10", "₹15", "₹20"],
            "answer": "₹10"
        },
        {
            "question": "What is the next number: 2, 4, 6, 8, ?",
            "options": ["9", "10", "11", "12"],
            "answer": "10"
        },
        {
            "question": "A train travels 60 km in 1 hour. How far in 3 hours?",
            "options": [
                "120 km",
                "150 km",
                "180 km",
                "200 km"
            ],
            "answer": "180 km"
        },
        {
            "question": "What is the average of 10, 20 and 30?",
            "options": ["15", "20", "25", "30"],
            "answer": "20"
        },
        {
            "question": "A number increases from 100 to 120. What is the percentage increase?",
            "options": ["10%", "15%", "20%", "25%"],
            "answer": "20%"
        },
        {
            "question": "Find the odd one out.",
            "options": [
                "Apple",
                "Mango",
                "Carrot",
                "Banana"
            ],
            "answer": "Carrot"
        },
        {
            "question": "If 3 workers complete a job in 6 days, how many worker-days are required?",
            "options": ["9", "18", "21", "24"],
            "answer": "18"
        },
        {
            "question": "Simple interest on ₹1000 at 10% per year for 2 years?",
            "options": ["₹100", "₹150", "₹200", "₹250"],
            "answer": "₹200"
        },
        {
            "question": "An item is bought for ₹500 and sold for ₹600. What is the profit?",
            "options": ["₹50", "₹75", "₹100", "₹150"],
            "answer": "₹100"
        }
    ]

    answers = {}

    for i, q in enumerate(questions):

        st.write(
            f"### Q{i+1}. {q['question']}"
        )

        answers[i] = st.radio(
            "Select your answer:",
            q["options"],
            key=f"aptitude_{i}"
        )

    if st.button("Submit Aptitude Assessment"):

        score = 0

        for i, q in enumerate(questions):

            if answers[i] == q["answer"]:
                score += 1

        percentage = int(
            (score / len(questions)) * 100
        )
         # Get logged-in student
        student = get_student(
        st.session_state.email
        )
        # Save score into database
        save_assessment_result(
        student[0],
        "Aptitude",
        score,
        len(questions)
        )
        st.success(
            f"Aptitude Score: {score}/{len(questions)}"
        )
        st.metric(
            "Percentage",
            f"{percentage}%"
        )
        if percentage >= 80:
            st.success(
                "Excellent Aptitude Performance! 🎉"
            )

        elif percentage >= 60:

            st.info(
                "Good performance. Keep practicing."
            )
        else:
            st.warning(
                "You need more aptitude practice."
            )
# ---------------- ASSESSMENT HISTORY ----------------

def assessment_history():

    st.title("🕒 Assessment History")

    student = get_student(
        st.session_state.email
    )

    conn = get_db()

    history = conn.execute(
        """
        SELECT assessment_type,
               score,
               total,
               percentage
        FROM assessment_attempt
        WHERE student_id = ?
        ORDER BY rowid DESC
        """,
        (student[0],)
    ).fetchall()

    conn.close()

    if not history:

        st.info(
            "No assessment attempts yet."
        )

        return

    st.subheader("📋 Previous Assessments")

    for i, record in enumerate(history, 1):

        assessment_type = record[0]
        score = record[1]
        total = record[2]
        percentage = record[3]

        st.markdown(
            f"### {i}. {assessment_type} Assessment"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Score",
                f"{score}/{total}"
            )

        with col2:
            st.metric(
                "Percentage",
                f"{percentage}%"
            )

        with col3:

            if percentage >= 80:
                st.success("Strong")

            elif percentage >= 60:
                st.info("Average")

            else:
                st.warning("Needs Improvement")

        st.divider() 
# ---------------- JOB RECOMMENDATION ----------------

def job_recommendation():

    st.title("🎯 Job Role Recommendation")

    student = get_student(
        st.session_state.email
    )

    python_score = student[6]
    aptitude_score = student[7]

    st.subheader("📊 Your Assessment Scores")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Python",
            f"{python_score}%"
        )

    with col2:
        st.metric(
            "Aptitude",
            f"{aptitude_score}%"
        )

    st.divider()

    # ---------------- RECOMMENDATION LOGIC ----------------

    if python_score >= 80 and aptitude_score >= 70:

        role = "Python Developer"

        skills = [
            "Advanced Python",
            "Object-Oriented Programming",
            "Data Structures & Algorithms",
            "SQL",
            "Problem Solving"
        ]

    elif python_score >= 70 and aptitude_score >= 70:

        role = "Software Developer"

        skills = [
            "Python / Java",
            "Data Structures & Algorithms",
            "SQL",
            "Problem Solving",
            "Object-Oriented Programming"
        ]

    elif aptitude_score >= 75:

        role = "Data Analyst"

        skills = [
            "Python",
            "SQL",
            "Excel",
            "Statistics",
            "Data Analysis"
        ]

    else:

        role = "Software Trainee"

        skills = [
            "Programming Basics",
            "Python",
            "SQL",
            "Aptitude",
            "Communication Skills"
        ]

    # ---------------- RESULT ----------------

    st.subheader("🎯 Recommended Job Role")

    st.success(
        f"**{role}**"
    )

    st.write(
        "Based on your current assessment performance, "
        "the following skills should be developed:"
    )

    st.subheader("📚 Recommended Skills")

    for skill in skills:

        st.write(
            f"• {skill}"
        )
# ---------------- PREPARATION PLAN ----------------

def preparation_plan():

    st.title("📚 Personalized Preparation Plan")

    student = get_student(
        st.session_state.email
    )

    python_score = student[6]
    aptitude_score = student[7]

    # Determine recommended role

    if python_score >= 80 and aptitude_score >= 70:

        role = "Python Developer"

        topics = [
            "Advanced Python",
            "Object-Oriented Programming",
            "Data Structures & Algorithms",
            "SQL",
            "Problem Solving"
        ]

    elif python_score >= 70 and aptitude_score >= 70:

        role = "Software Developer"

        topics = [
            "Python / Java",
            "Data Structures & Algorithms",
            "SQL",
            "Object-Oriented Programming",
            "Coding Practice"
        ]

    elif aptitude_score >= 75:

        role = "Data Analyst"

        topics = [
            "Python",
            "SQL",
            "Excel",
            "Statistics",
            "Data Analysis"
        ]

    else:

        role = "Software Trainee"

        topics = [
            "Programming Basics",
            "Python Basics",
            "SQL Basics",
            "Aptitude",
            "Communication Skills"
        ]

    # ---------------- ROLE ----------------

    st.subheader("🎯 Target Job Role")

    st.success(role)

    st.divider()

    # ---------------- SCORES ----------------

    st.subheader("📊 Current Performance")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Python",
            f"{python_score}%"
        )

    with col2:

        st.metric(
            "Aptitude",
            f"{aptitude_score}%"
        )

    st.divider()

    # ---------------- PLAN ----------------

    st.subheader("📅 Recommended Preparation Topics")

    for i, topic in enumerate(topics, 1):

        st.write(
            f"### Day {i} — {topic}"
        )

        if topic == "Advanced Python":

            st.write(
                "Practice functions, modules, exception handling, "
                "file handling and advanced Python concepts."
            )

        elif topic == "Python":

            st.write(
                "Practice Python basics, functions, lists, "
                "dictionaries and coding problems."
            )

        elif topic == "Python Basics":

            st.write(
                "Learn variables, data types, conditions, "
                "loops, functions and basic programs."
            )

        elif topic == "SQL":

            st.write(
                "Practice SELECT, WHERE, JOIN, GROUP BY, "
                "subqueries and aggregate functions."
            )

        elif topic == "Data Structures & Algorithms":

            st.write(
                "Practice arrays, strings, searching, sorting, "
                "stacks, queues and basic algorithms."
            )

        elif topic == "Aptitude":

            st.write(
                "Practice percentages, profit and loss, ratios, "
                "time and work, averages and number series."
            )

        elif topic == "Communication Skills":

            st.write(
                "Practice self-introduction, JAM topics, "
                "HR questions and interview communication."
            )

        else:

            st.write(
                f"Practice {topic} concepts and interview questions."
            )

        st.divider()

    st.info(
        "💡 Follow the topics consistently and take the assessments "
        "again to track your improvement."
    )
# ---------------- PROGRESS ----------------

def progress_page():

    st.title("📊 Your Progress")

    student = get_student(
        st.session_state.email
    )

    python_score = student[6]
    aptitude_score = student[7]

    # Overall score
    overall_score = (
        python_score + aptitude_score
    ) / 2

    # Get assessment count
    conn = get_db()

    result = conn.execute(
        """
        SELECT COUNT(*)
        FROM assessment_attempt
        WHERE student_id = ?
        """,
        (student[0],)
    ).fetchone()

    conn.close()

    tests_completed = result[0]

    # ---------------- SUMMARY ----------------

    st.subheader("📈 Performance Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Python",
            f"{python_score}%"
        )

    with col2:
        st.metric(
            "Aptitude",
            f"{aptitude_score}%"
        )

    with col3:
        st.metric(
            "Overall",
            f"{overall_score:.0f}%"
        )

    st.divider()

    # ---------------- PROGRESS BARS ----------------

    st.subheader("🎯 Skill Progress")

    st.write(
        f"🐍 Python — {python_score}%"
    )

    st.progress(
        python_score / 100
    )

    st.write(
        f"🧠 Aptitude — {aptitude_score}%"
    )

    st.progress(
        aptitude_score / 100
    )

    st.write(
        f"🎯 Overall — {overall_score:.0f}%"
    )

    st.progress(
        overall_score / 100
    )

    st.divider()

    # ---------------- TESTS COMPLETED ----------------

    st.subheader("📝 Assessment Activity")

    st.metric(
        "Tests Completed",
        tests_completed
    )

    # ---------------- PERFORMANCE MESSAGE ----------------

    if overall_score >= 80:

        st.success(
            "Excellent progress! Keep practicing consistently. 🎉"
        )

    elif overall_score >= 60:

        st.info(
            "Good progress. Continue improving your weaker areas. 👍"
        )

    else:

        st.warning(
            "You need more practice. Focus on your weak areas. 💪"
        )
# ---------------- PROGRESS ----------------

def progress_page():

    st.title("📊 Your Progress")

    student = get_student(
        st.session_state.email
    )

    python_score = student[6]
    aptitude_score = student[7]

    overall_score = (
        python_score + aptitude_score
    ) / 2

    conn = get_db()

    result = conn.execute(
        """
        SELECT COUNT(*)
        FROM assessment_attempt
        WHERE student_id = ?
        """,
        (student[0],)
    ).fetchone()

    conn.close()

    tests_completed = result[0]

    # Performance Overview
    st.subheader("📈 Performance Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Python",
            f"{python_score}%"
        )

    with col2:
        st.metric(
            "Aptitude",
            f"{aptitude_score}%"
        )

    with col3:
        st.metric(
            "Overall",
            f"{overall_score:.0f}%"
        )

    st.divider()

    # Skill Progress
    st.subheader("🎯 Skill Progress")

    st.write(
        f"🐍 Python — {python_score}%"
    )

    st.progress(
        python_score / 100
    )

    st.write(
        f"🧠 Aptitude — {aptitude_score}%"
    )

    st.progress(
        aptitude_score / 100
    )

    st.write(
        f"🎯 Overall — {overall_score:.0f}%"
    )

    st.progress(
        overall_score / 100
    )

    st.divider()

    # Assessment Activity
    st.subheader("📝 Assessment Activity")

    st.metric(
        "Tests Completed",
        tests_completed
    )

    if overall_score >= 80:

        st.success(
            "Excellent progress! Keep practicing consistently. 🎉"
        )

    elif overall_score >= 60:

        st.info(
            "Good progress. Continue improving your weaker areas. 👍"
        )

    else:

        st.warning(
            "You need more practice. Focus on your weak areas. 💪"
        )                    

# ---------------- MAIN ----------------

if not st.session_state.logged_in:

    option = st.sidebar.radio(
        "Account",
        [
            "Login",
            "Register"
        ]
    )

    if option == "Login":

        login_page()

    else:

        register_page()

else:

    st.sidebar.title(
        "🎓 Smart Placement"
    )

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Python Assessment",
            "Aptitude Assessment",
            "Assessment History",
            "Profile",
            "Skill Analysis",
            "Job Recommendation",
            "Preparation Plan",
            "Progress"
        ]
    )

    if st.sidebar.button("Logout"):

        logout()

    if page == "Dashboard":

        dashboard()
    
    elif page == "Python Assessment":

        python_assessment()

    elif page == "Aptitude Assessment":
        aptitude_assessment() 
    elif page == "Assessment History":
        assessment_history()
    elif page == "Job Recommendation":
        job_recommendation()
    elif page == "Preparation Plan":
        preparation_plan()
    elif page == "Progress":

       progress_page()                       
    elif page == "Profile":

        st.title("👤 Student Profile")

        student = get_student(
            st.session_state.email
        )

        if student is None:

            st.error("Student profile not found.")

        else:

            # ------------------------------------------------
            # Existing student details
            # ------------------------------------------------

            student_id = student[0]
            name = student[1]
            email = student[2]
            college = student[3]
            branch = student[4]


            # ------------------------------------------------
            # Get additional profile information
            # ------------------------------------------------

            conn = get_db()

            profile_data = conn.execute(
                """
                SELECT
                    college_place,
                    pincode,
                    district,
                    joining_year,
                    passedout_year
                FROM student
                WHERE id = ?
                """,
                (student_id,)
            ).fetchone()

            conn.close()


            # If values don't exist yet

            college_place = ""
            pincode = ""
            district = ""
            joining_year = 2023
            passedout_year = 2027


            if profile_data:

                if profile_data[0]:
                    college_place = profile_data[0]

                if profile_data[1]:
                    pincode = profile_data[1]

                if profile_data[2]:
                    district = profile_data[2]

                if profile_data[3]:
                    joining_year = profile_data[3]

                if profile_data[4]:
                    passedout_year = profile_data[4]


            # =================================================
            # PERSONAL INFORMATION
            # =================================================

            st.subheader("👤 Personal Information")

            col1, col2 = st.columns(2)


            with col1:

                st.text_input(
                    "Student Name",
                    value=name,
                    disabled=True
                )


            with col2:

                st.text_input(
                    "Email",
                    value=email,
                    disabled=True
                )


            # =================================================
            # COLLEGE INFORMATION
            # =================================================

            st.subheader("🎓 College Information")

            col1, col2 = st.columns(2)


            with col1:

                college_name = st.text_input(
                    "College Name",
                    value=college
                )

                college_place_input = st.text_input(
                    "Place of College",
                    value=college_place
                )

                district_input = st.text_input(
                    "District",
                    value=district
                )


            with col2:

                st.text_input(
                    "Branch",
                    value=branch,
                    disabled=True
                )

                pincode_input = st.text_input(
                    "Pincode",
                    value=pincode
                )


            # =================================================
            # ACADEMIC TIMELINE
            # =================================================

            st.subheader("📅 Academic Timeline")

            col1, col2 = st.columns(2)


            with col1:

                joining_year_input = st.number_input(
                    "Year of Joining",
                    min_value=2000,
                    max_value=2035,
                    value=int(joining_year),
                    step=1
                )


            with col2:

                passedout_year_input = st.number_input(
                    "Year of Passed Out",
                    min_value=2000,
                    max_value=2040,
                    value=int(passedout_year),
                    step=1
                )


            # =================================================
            # SAVE PROFILE
            # =================================================

            if st.button(
                "💾 Save Profile",
                use_container_width=True
            ):

                if not pincode_input.isdigit():

                    st.error(
                        "Pincode must contain only numbers."
                    )

                elif len(pincode_input) != 6:

                    st.error(
                        "Pincode must contain exactly 6 digits."
                    )

                elif passedout_year_input <= joining_year_input:

                    st.error(
                        "Passed Out Year must be greater than Joining Year."
                    )

                else:

                    conn = get_db()

                    conn.execute(
                        """
                        UPDATE student

                        SET
                            college = ?,
                            college_place = ?,
                            pincode = ?,
                            district = ?,
                            joining_year = ?,
                            passedout_year = ?

                        WHERE id = ?
                        """,

                        (
                            college_name,
                            college_place_input,
                            pincode_input,
                            district_input,
                            joining_year_input,
                            passedout_year_input,
                            student_id
                        )
                    )

                    conn.commit()

                    conn.close()

                    st.success(
                        "✅ Profile updated successfully!"
                    )

                    st.rerun()

    elif page == "Skill Analysis":
        st.title("📈 Skill Analysis")
        student = get_student(
            st.session_state.email
        )
        python_score = student[6]
        aptitude_score = student[7]
        st.write(
            f"Python: {python_score}%"
        )
        st.progress(
            python_score / 100
        )
        st.write(
            f"Aptitude: {aptitude_score}%"
        )
        st.progress(
            aptitude_score / 100
        )
    elif page == "Job Recommendation":

        st.title("🎯 Job Recommendation")
        student = get_student(
            st.session_state.email
        )
        p = student[6]
        a = student[7]
        if p >= 80 and a >= 70:
            st.success(
                "Python Developer"
            )
        elif p >= 70:
            st.success(
                "Software Developer"
            )
        elif a >= 70:
            st.success(
                "Data Analyst"
            )
        else:
            st.info(
                "Software Trainee"
            )
    elif page == "Preparation Plan":

        st.title("📚 Preparation Plan")
        st.write(
            "### Python"
        )
        st.write(
            "• Python Basics"
        )
        st.write(
            "• Functions"
        )
        st.write(
            "• Lists and Dictionaries"
        )

        st.write(
            "• OOP"
        )
        st.write(
            "• DSA"
        )
        st.write(
            "### Aptitude"
        )
        st.write(
            "• Percentages"
        )
        st.write(
            "• Profit and Loss"
        )
        st.write(
            "• Time and Work"
        )
        st.write(
            "• Logical Reasoning"
        )
    elif page == "Progress":

        st.title("📊 Progress")
        student = get_student(
            st.session_state.email
        )

        p = student[6]
        a = student[7]

        overall = (p + a) / 2

        st.metric(
            "Overall Progress",
            f"{overall:.0f}%"
        )

        st.progress(
            overall / 100
        )
