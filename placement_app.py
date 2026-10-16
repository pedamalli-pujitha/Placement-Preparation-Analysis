from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
app = Flask(__name__)
app.secret_key = "smart-placement-secret-key"

# =========================================================
# DATABASE CONFIGURATION
# =========================================================

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
# =========================================================
# STUDENT DATABASE MODEL
# =========================================================
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    college = db.Column(db.String(150))

    branch = db.Column(db.String(100))

    password = db.Column(
        db.String(255),
        nullable=False
    )

    # Assessment Scores
    python_score = db.Column(
        db.Integer,
        default=0
    )

    aptitude_score = db.Column(
        db.Integer,
        default=0
    )
class AssessmentAttempt(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id"),
        nullable=False
    )

    assessment_type = db.Column(
        db.String(50),
        nullable=False
    )

    score = db.Column(
        db.Integer,
        nullable=False
    )

    total = db.Column(
        db.Integer,
        nullable=False
    )

    percentage = db.Column(
        db.Integer,
        nullable=False
    )

    attempted_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )    
# =========================================================
# PYTHON ASSESSMENT QUESTIONS
# =========================================================

questions = [
    {
        "question": "Which keyword is used to define a function in Python?",
        "options": ["function", "def", "define", "fun"],
        "answer": "def"
    },
    {
        "question": "Which data type is used to store True or False?",
        "options": ["int", "str", "bool", "float"],
        "answer": "bool"
    },
    {
        "question": "Which symbol is used for comments in Python?",
        "options": ["//", "#", "/*", "--"],
        "answer": "#"
    },
    {
        "question": "Which function is used to find the length of a list?",
        "options": ["size()", "length()", "len()", "count()"],
        "answer": "len()"
    },
    {
        "question": "Which of the following is a Python list?",
        "options": ["(1, 2, 3)", "[1, 2, 3]", "{1, 2, 3}", "<1, 2, 3>"],
        "answer": "[1, 2, 3]"
    }
]


# =========================================================
# APTITUDE ASSESSMENT QUESTIONS
# =========================================================

aptitude_questions = [
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
        "question": "What is the next number in the series: 2, 4, 6, 8, ?",
        "options": ["9", "10", "11", "12"],
        "answer": "10"
    },
    {
        "question": "A train travels 60 km in 1 hour. How far will it travel in 3 hours?",
        "options": ["120 km", "150 km", "180 km", "200 km"],
        "answer": "180 km"
    },
    {
        "question": "What is the average of 10, 20 and 30?",
        "options": ["15", "20", "25", "30"],
        "answer": "20"
    },
    {
        "question": "If a number is increased from 100 to 120, what is the percentage increase?",
        "options": ["10%", "15%", "20%", "25%"],
        "answer": "20%"
    },
    {
        "question": "Find the odd one out.",
        "options": ["Apple", "Mango", "Carrot", "Banana"],
        "answer": "Carrot"
    },
    {
        "question": "If 3 workers complete a job in 6 days, how many worker-days are required?",
        "options": ["9", "18", "21", "24"],
        "answer": "18"
    },
    {
        "question": "What is the simple interest on ₹1000 at 10% per year for 2 years?",
        "options": ["₹100", "₹150", "₹200", "₹250"],
        "answer": "₹200"
    },
    {
        "question": "A shopkeeper buys an item for ₹500 and sells it for ₹600. What is the profit?",
        "options": ["₹50", "₹75", "₹100", "₹150"],
        "answer": "₹100"
    }
]


# =========================================================
# HOME
# =========================================================
@app.route("/")
def home():
    return redirect(url_for("login"))
# =========================================================
# REGISTER
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        college = request.form.get("college")
        branch = request.form.get("branch")
        password = request.form.get("password")

        # Check whether email already exists
        existing_student = Student.query.filter_by(
            email=email
        ).first()

        if existing_student:
            return "Email already registered. Please use another email."

        # Hash password before saving
        hashed_password = generate_password_hash(password)

        # Create new student
        new_student = Student(
            name=name,
            email=email,
            college=college,
            branch=branch,
            password=hashed_password
        )

        # Save student to database
        db.session.add(new_student)
        db.session.commit()

        # Store information in session
        session["name"] = name
        session["email"] = email
        session["college"] = college
        session["branch"] = branch

        return redirect(url_for("dashboard"))

    return render_template("register.html")

# ======================S===================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        # Find student by email
        student = Student.query.filter_by(
            email=email
        ).first()

        # Check email and password
        if student and check_password_hash(
            student.password,
            password
        ):

            session["name"] = student.name
            session["email"] = student.email
            session["college"] = student.college
            session["branch"] = student.branch

            return redirect(url_for("dashboard"))

        else:

            return "Invalid email or password."

    return render_template("login.html")

# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if "email" not in session:
        return redirect(url_for("login"))

    # Get student from database
    student = Student.query.filter_by(
        email=session["email"]
    ).first()

    if not student:
        return "Student not found."

    # Get scores from database
    python_score = student.python_score
    aptitude_score = student.aptitude_score

    # Calculate overall score
    scores = []

    if python_score is not None and python_score > 0:
        scores.append(python_score)

    if aptitude_score is not None and aptitude_score > 0:
        scores.append(aptitude_score)

    if scores:
        overall_score = int(sum(scores) / len(scores))
    else:
        overall_score = None

    # Number of completed tests
    tests_completed = len(scores)

    return render_template(
        "dashboard.html",
        student=student,
        name=student.name,
        python_score=python_score if python_score > 0 else None,
        aptitude_score=aptitude_score if aptitude_score > 0 else None,
        overall_score=overall_score,
        tests_completed=tests_completed
    )
# =========================================================
# PYTHON ASSESSMENT
# =========================================================

@app.route("/assessment", methods=["GET", "POST"])
def assessment():

    # Login check
    if "email" not in session:
        return redirect(url_for("login"))

    # -----------------------------------------------------
    # QUESTIONS
    # -----------------------------------------------------
    questions = [
        {
            "question": "Which keyword is used to define a function in Python?",
            "options": ["func", "define", "def", "function"],
            "answer": "def"
        },
        {
            "question": "Which data type is used to store multiple values in Python?",
            "options": ["int", "list", "float", "bool"],
            "answer": "list"
        },
        {
            "question": "Which symbol is used for comments in Python?",
            "options": ["//", "#", "/*", "--"],
            "answer": "#"
        },
        {
            "question": "Which function is used to display output in Python?",
            "options": ["display()", "show()", "print()", "output()"],
            "answer": "print()"
        },
        {
            "question": "Which keyword is used to create a class in Python?",
            "options": ["object", "class", "struct", "define"],
            "answer": "class"
        }
    ]

    # -----------------------------------------------------
    # START ASSESSMENT
    # -----------------------------------------------------
    if request.method == "GET":

        session["python_question"] = 0
        session["python_correct"] = 0

    # Current question number
    question_index = session.get("python_question", 0)

    # -----------------------------------------------------
    # SUBMIT ANSWER
    # -----------------------------------------------------
    if request.method == "POST":

        selected_answer = request.form.get("answer")

        # Check answer
        if selected_answer == questions[question_index]["answer"]:

            session["python_correct"] = (
                session.get("python_correct", 0) + 1
            )

        # Move to next question
        question_index += 1

        session["python_question"] = question_index

    # -----------------------------------------------------
    # ASSESSMENT COMPLETED
    # -----------------------------------------------------
    if question_index >= len(questions):

        correct = session.get("python_correct", 0)

        total = len(questions)

        percentage = int(
            (correct / total) * 100
        )

        # Save score in session
        session["python_score"] = percentage

        # -------------------------------------------------
        # GET STUDENT
        # -------------------------------------------------
        student = Student.query.filter_by(
            email=session["email"]
        ).first()

        if student:

            # Save Python score
            student.python_score = percentage

            # Save assessment history
            attempt = AssessmentAttempt(
                student_id=student.id,
                assessment_type="Python",
                score=correct,
                total=total,
                percentage=percentage
            )

            db.session.add(attempt)

            # Save to database
            db.session.commit()

        # Show result
        return render_template(
            "result.html",
            percentage=percentage,
            score=correct,
            correct=correct,
            total=total,
            subject="Python"
        )
# -----------------------------------------------------
# SHOW QUESTION
# -----------------------------------------------------

    question = questions[question_index]

    return render_template(
        "assessment.html",
        question=question,
        question_number=question_index + 1,
        total_questions=len(questions)
    )
#==============================================
# PYTHON QUESTIONS
# =========================================================

@app.route("/question/<int:number>", methods=["GET", "POST"])
def question(number):

    if "email" not in session:
        return redirect(url_for("login"))

    if number < 0 or number >= len(questions):
        return redirect(url_for("result"))

    if request.method == "POST":

        selected_answer = request.form.get("answer")

        answers = session.get("answers", [])

        answers.append(selected_answer)

        session["answers"] = answers

        next_number = number + 1

        if next_number < len(questions):

            return redirect(
                url_for("question", number=next_number)
            )

        else:

            return redirect(url_for("result"))

    current_question = questions[number]

    return render_template(
        "assessment.html",
        question=current_question,
        number=number,
        total=len(questions)
    )


# =========================================================
# PYTHON RESULT
# =========================================================

@app.route("/result")
def result():

    if "email" not in session:
        return redirect(url_for("login"))

    answers = session.get("answers", [])

    score = 0

    for i in range(min(len(answers), len(questions))):

        if answers[i] == questions[i]["answer"]:
            score += 1

    total = len(questions)

    percentage = int((score / total) * 100)

    session["python_score"] = percentage

    session["tests_completed"] = session.get(
        "tests_completed", 0
    ) + 1

    return render_template(
        "result.html",
        score=score,
        total=total,
        percentage=percentage,
        test_name="Python Assessment"
    )


# =========================================================
# APTITUDE ASSESSMENT START
# =========================================================

@app.route("/aptitude")
def aptitude():

    if "email" not in session:
        return redirect(url_for("login"))

    session["aptitude_answers"] = []

    return redirect(
        url_for("aptitude_question", number=0)
    )


# =========================================================
# APTITUDE QUESTIONS
# =========================================================

@app.route("/aptitude/question/<int:number>", methods=["GET", "POST"])
def aptitude_question(number):

    if "email" not in session:
        return redirect(url_for("login"))

    if number < 0 or number >= len(aptitude_questions):
        return redirect(url_for("aptitude_result"))

    if request.method == "POST":

        selected_answer = request.form.get("answer")

        answers = session.get("aptitude_answers", [])

        answers.append(selected_answer)

        session["aptitude_answers"] = answers

        next_number = number + 1

        if next_number < len(aptitude_questions):

            return redirect(
                url_for(
                    "aptitude_question",
                    number=next_number
                )
            )

        else:

            return redirect(
                url_for("aptitude_result")
            )

    current_question = aptitude_questions[number]

    return render_template(
        "aptitude.html",
        question=current_question,
        number=number,
        total=len(aptitude_questions)
    )

# =========================================================
# APTITUDE RESULT
# =========================================================

@app.route("/aptitude/result")
def aptitude_result():

    if "email" not in session:
        return redirect(url_for("login"))

    answers = session.get("aptitude_answers", [])

    score = 0

    for i in range(
        min(len(answers), len(aptitude_questions))
    ):

        if answers[i] == aptitude_questions[i]["answer"]:
            score += 1

    total = len(aptitude_questions)

    percentage = int((score / total) * 100)

    # Save score in session
    session["aptitude_score"] = percentage

    # =====================================================
    # SAVE APTITUDE SCORE TO DATABASE
    # =====================================================

    student = Student.query.filter_by(
        email=session["email"]
    ).first()

    if student:

        student.aptitude_score = percentage

        db.session.commit()

    # =====================================================
    # TESTS COMPLETED
    # =====================================================

    session["tests_completed"] = session.get(
        "tests_completed", 0
    ) + 1

    return render_template(
        "result.html",
        score=score,
        total=total,
        percentage=percentage,
        test_name="Aptitude Assessment"
    )

# =========================================================
# SKILL ANALYSIS
# =========================================================

@app.route("/skill-analysis")
def skill_analysis():

    if "email" not in session:
        return redirect(url_for("login"))

    # Get student from database
    student = Student.query.filter_by(
        email=session["email"]
    ).first()

    if not student:
        return "Student not found."

    # Get scores from database
    python_score = student.python_score or 0
    aptitude_score = student.aptitude_score or 0

    # Calculate overall score
    scores = []

    if python_score > 0:
        scores.append(python_score)

    if aptitude_score > 0:
        scores.append(aptitude_score)

    if scores:
        overall_score = int(sum(scores) / len(scores))
    else:
        overall_score = 0

    # =====================================================
    # PYTHON SKILL
    # =====================================================

    if python_score >= 80:
        python_level = "Strong"
    elif python_score >= 60:
        python_level = "Average"
    else:
        python_level = "Needs Improvement"

    # =====================================================
    # APTITUDE SKILL
    # =====================================================

    if aptitude_score >= 80:
        aptitude_level = "Strong"
    elif aptitude_score >= 60:
        aptitude_level = "Average"
    else:
        aptitude_level = "Needs Improvement"

    # =====================================================
    # STRONG AND WEAK SKILLS
    # =====================================================

    strong_skills = []
    weak_skills = []

    if python_score >= 80:
        strong_skills.append("Python")
    elif python_score > 0:
        weak_skills.append("Python")

    if aptitude_score >= 80:
        strong_skills.append("Aptitude")
    elif aptitude_score > 0:
        weak_skills.append("Aptitude")

    return render_template(
        "skill_analysis.html",
        student=student,
        python_score=python_score,
        aptitude_score=aptitude_score,
        overall_score=overall_score,
        python_level=python_level,
        aptitude_level=aptitude_level,
        strong_skills=strong_skills,
        weak_skills=weak_skills
    )
# =========================================================
# PERSONALIZED PREPARATION PLAN
# =========================================================
@app.route("/preparation-plan")
def preparation_plan():

    if "email" not in session:
        return redirect(url_for("login"))

    student = Student.query.filter_by(
        email=session["email"]
    ).first()

    if not student:
        return "Student not found."

    # Get scores
    python_score = student.python_score
    aptitude_score = student.aptitude_score

    # =====================================================
    # PYTHON PLAN
    # =====================================================

    if python_score is None:

        python_plan = [
            "Complete Python Assessment"
        ]

    elif python_score >= 80:

        python_plan = [
            "Advanced Python Programming",
            "Object-Oriented Programming",
            "Data Structures using Python",
            "Python Coding Practice"
        ]

    elif python_score >= 60:

        python_plan = [
            "Python Basics Revision",
            "Functions and Modules",
            "Lists, Tuples and Dictionaries",
            "Basic Coding Practice"
        ]

    else:

        python_plan = [
            "Python Fundamentals",
            "Variables and Data Types",
            "Conditional Statements",
            "Loops and Functions"
        ]


    # =====================================================
    # APTITUDE PLAN
    # =====================================================

    if aptitude_score is None:

        aptitude_plan = [
            "Complete Aptitude Assessment"
        ]

    elif aptitude_score >= 80:

        aptitude_plan = [
            "Advanced Aptitude Mock Tests",
            "Logical Reasoning Practice",
            "Quantitative Aptitude Practice",
            "Time Management"
        ]

    elif aptitude_score >= 60:

        aptitude_plan = [
            "Quantitative Aptitude Basics",
            "Logical Reasoning",
            "Number Problems",
            "Daily Aptitude Practice"
        ]

    else:

        aptitude_plan = [
            "Basic Mathematics",
            "Percentages",
            "Profit and Loss",
            "Number System"
        ]


    # =====================================================
    # PLACEMENT PLAN
    # =====================================================

    placement_plan = [
        "Resume Preparation",
        "Technical Interview Preparation",
        "Communication Skills",
        "HR Interview Questions",
        "Mock Interviews"
    ]


    # =====================================================
    # JOB ROLE
    # =====================================================

    if python_score is not None and aptitude_score is not None:

        if python_score >= 80:
            job_role = "Python Developer"

        elif aptitude_score >= 80:
            job_role = "Software Developer"

        else:
            job_role = "Software Developer"

    else:

        job_role = "Complete both assessments"


    # =====================================================
    # SEND DATA TO HTML
    # =====================================================

    return render_template(
        "preparation_plan.html",

        student=student,

        python_score=python_score,

        aptitude_score=aptitude_score,

        python_plan=python_plan,

        aptitude_plan=aptitude_plan,

        placement_plan=placement_plan,

        job_role=job_role
    )

    # =====================================================
    # APTITUDE PLAN
    # =====================================================

    if aptitude_score >= 80:

        aptitude_plan = [
            "Advanced Aptitude Mock Tests",
            "Logical Reasoning Practice",
            "Quantitative Aptitude Practice",
            "Time Management"
        ]

    elif aptitude_score >= 60:

        aptitude_plan = [
            "Quantitative Aptitude Basics",
            "Logical Reasoning",
            "Number Problems",
            "Daily Aptitude Practice"
        ]

    else:

        aptitude_plan = [
            "Basic Mathematics",
            "Percentages",
            "Profit and Loss",
            "Number System"
        ]

# =====================================================
# PLACEMENT PLAN
# =====================================================

    placement_plan = [
        "Resume Preparation",
        "Technical Interview Preparation",
        "Communication Skills",
        "HR Interview Questions",
        "Mock Interviews"
    ]

    return render_template(
        "preparation_plan.html",
        student=student,
        python_score=python_score,
        aptitude_score=aptitude_score,
        python_plan=python_plan,
        aptitude_plan=aptitude_plan,
        placement_plan=placement_plan
    )
# =========================================================
# PROGRESS
# =========================================================

@app.route("/progress")
def progress():

    if "email" not in session:
        return redirect(url_for("login"))

    student = Student.query.filter_by(
        email=session["email"]
    ).first()

    if not student:
        return "Student not found."

    # Get scores from database
    python_score = student.python_score
    aptitude_score = student.aptitude_score

    # Use 0 only for calculation
    python_value = python_score if python_score is not None else 0
    aptitude_value = aptitude_score if aptitude_score is not None else 0

    # =====================================================
    # OVERALL PROGRESS
    # =====================================================

    scores = []

    if python_score is not None:
        scores.append(python_value)

    if aptitude_score is not None:
        scores.append(aptitude_value)

    if scores:
        overall_score = int(sum(scores) / len(scores))
    else:
        overall_score = 0

    # =====================================================
    # TESTS COMPLETED
    # =====================================================

    tests_completed = len(scores)

    # =====================================================
    # PREPARATION TOPICS
    # =====================================================

    topics = [
        "Python",
        "Aptitude",
        "Data Structures",
        "SQL",
        "Communication"
    ]

    # =====================================================
    # SEND DATA TO HTML
    # =====================================================

    return render_template(
        "progress.html",
        student=student,
        python_score=python_score,
        aptitude_score=aptitude_score,
        overall_score=overall_score,
        tests_completed=tests_completed,
        progress_percentage=overall_score,
        topics=topics
    )
# =========================================================
# STUDENT PROFILE
# =========================================================

@app.route("/profile", methods=["GET", "POST"])
def profile():

    if "email" not in session:
        return redirect(url_for("login"))

    # Get student from database
    student = Student.query.filter_by(
        email=session["email"]
    ).first()

    if not student:
        return "Student not found."

    # UPDATE PROFILE
    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        college = request.form.get("college")
        branch = request.form.get("branch")

        # Check if another student already uses this email
        existing_student = Student.query.filter(
            Student.email == email,
            Student.id != student.id
        ).first()

        if existing_student:
            return "This email is already registered."

        student.name = name
        student.email = email
        student.college = college
        student.branch = branch

        db.session.commit()

        # Update session
        session["name"] = student.name
        session["email"] = student.email
        session["college"] = student.college
        session["branch"] = student.branch

        return redirect(url_for("profile"))

    # GET PROFILE DATA

    python_score = student.python_score or 0
    aptitude_score = student.aptitude_score or 0

    # Calculate overall score
    scores = []

    if python_score > 0:
        scores.append(python_score)

    if aptitude_score > 0:
        scores.append(aptitude_score)

    if scores:
        overall_score = int(sum(scores) / len(scores))
    else:
        overall_score = None

    # Job role
    if python_score >= 80 and aptitude_score >= 70:

        job_role = "Python Developer"

    elif python_score >= 70 and aptitude_score >= 70:

        job_role = "Software Developer"

    elif aptitude_score >= 75:

        job_role = "Data Analyst"

    else:

        job_role = "Software Trainee"

    # FINAL RESPONSE
    return render_template(
        "profile.html",
        student=student,
        name=student.name,
        email=student.email,
        college=student.college,
        branch=student.branch,
        python_score=python_score,
        aptitude_score=aptitude_score,
        overall_score=overall_score,
        job_role=job_role
    )


# =========================================================
# JOB ROLE RECOMMENDATION
# =========================================================

@app.route("/job-recommendation")
def job_recommendation():

    if "email" not in session:
        return redirect(url_for("login"))

    # Get student from database
    student = Student.query.filter_by(
        email=session["email"]
    ).first()

    if not student:
        return "Student not found."

    # Get scores
    python_score = student.python_score or 0
    aptitude_score = student.aptitude_score or 0

    # Job role recommendation
    if python_score >= 80 and aptitude_score >= 70:

        job_role = "Python Developer"

        reason = (
            "Your Python and Aptitude performance "
            "shows strong suitability for Python development."
        )

        skills = [
            "Python",
            "Object-Oriented Programming",
            "Data Structures",
            "SQL",
            "Problem Solving"
        ]

    elif python_score >= 70 and aptitude_score >= 70:

        job_role = "Software Developer"

        reason = (
            "Your technical and aptitude scores "
            "show good software development potential."
        )

        skills = [
            "Python",
            "Java",
            "SQL",
            "Data Structures",
            "Problem Solving"
        ]

    elif aptitude_score >= 75:

        job_role = "Data Analyst"

        reason = (
            "Your aptitude performance indicates "
            "good analytical and problem-solving ability."
        )

        skills = [
            "Python",
            "SQL",
            "Excel",
            "Statistics",
            "Data Analysis"
        ]

    else:

        job_role = "Software Trainee"

        reason = (
            "Improve your technical and aptitude skills "
            "to prepare for software development roles."
        )

        skills = [
            "Programming Basics",
            "Python",
            "SQL",
            "Aptitude",
            "Communication Skills"
        ]

    return render_template(
        "job_recommendation.html",
        student=student,
        python_score=python_score,
        aptitude_score=aptitude_score,
        job_role=job_role,
        reason=reason,
        skills=skills
    )
    # =====================================================
    # DISPLAY PROFILE
    # =====================================================

    return render_template(
        "profile.html",

        # Student details from database
        student=student,

        # Existing profile values
        name=student.name,
        email=student.email,
        college=student.college,
        branch=student.branch,

        # Assessment information
        python_score=python_score,
        aptitude_score=aptitude_score,
        overall_score=overall_score,
        job_role=job_role
    )

# =========================================================
# FINAL PLACEMENT DASHBOARD
# =========================================================

@app.route("/final-dashboard")
def final_dashboard():

    if "email" not in session:
        return redirect(url_for("login"))

    # Get student from database
    student = Student.query.filter_by(
        email=session["email"]
    ).first()

    if not student:
        return "Student not found."

    # Get scores from DATABASE
    python_score = student.python_score
    aptitude_score = student.aptitude_score

    # =====================================================
    # OVERALL SCORE
    # =====================================================

    scores = []

    if python_score is not None:
        scores.append(python_score)

    if aptitude_score is not None:
        scores.append(aptitude_score)

    if scores:
        overall_score = int(sum(scores) / len(scores))
    else:
        overall_score = 0

    # =====================================================
    # STRONG AND WEAK AREA
    # =====================================================

    if python_score is not None and aptitude_score is not None:

        if python_score >= aptitude_score:
            strong_area = "Python"
            weak_area = "Aptitude"
        else:
            strong_area = "Aptitude"
            weak_area = "Python"

    elif python_score is not None:

        strong_area = "Python"
        weak_area = "Complete Aptitude Assessment"

    elif aptitude_score is not None:

        strong_area = "Aptitude"
        weak_area = "Complete Python Assessment"

    else:

        strong_area = "No assessment completed"
        weak_area = "Complete assessments"

    # =====================================================
    # JOB ROLE
    # =====================================================

    if python_score is not None and aptitude_score is not None:

        if python_score >= 80 and aptitude_score >= 70:
            job_role = "Python Developer"

        elif python_score >= 70 and aptitude_score >= 70:
            job_role = "Software Developer"

        elif aptitude_score >= 75:
            job_role = "Data Analyst"

        else:
            job_role = "Software Trainee"

    else:

        job_role = "Complete both assessments"

    # =====================================================
    # PREPARATION TOPICS
    # =====================================================

    if python_score is not None and aptitude_score is not None:

        if python_score < aptitude_score:

            topics = [
                "Python Basics",
                "Functions and Modules",
                "Lists, Tuples and Dictionaries",
                "Object-Oriented Programming",
                "Python Coding Practice"
            ]

        else:

            topics = [
                "Percentages",
                "Profit and Loss",
                "Time and Work",
                "Time, Speed and Distance",
                "Logical Reasoning"
            ]

    else:

        topics = []

        if python_score is None:
            topics.append("Complete Python Assessment")

        if aptitude_score is None:
            topics.append("Complete Aptitude Assessment")

    # =====================================================
    # FINAL DASHBOARD
    # =====================================================

    return render_template(
        "final_dashboard.html",

        student=student,

        name=student.name,
        email=student.email,
        college=student.college,
        branch=student.branch,

        python_score=python_score,
        aptitude_score=aptitude_score,

        overall_score=overall_score,

        strong_area=strong_area,
        weak_area=weak_area,

        job_role=job_role,

        topics=topics
    )

# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))
# =========================================================
# ERROR HANDLERS
# =========================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "error.html"
    ), 404


@app.errorhandler(500)
def internal_server_error(error):

    return render_template(
        "error.html"
    ), 500    

# =========================================================
# RUN APPLICATION
# =========================================================
if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5001)