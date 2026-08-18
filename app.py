from flask import Flask, render_template, request, session
from dotenv import load_dotenv
from google import genai
import os
import json
import re
import markdown

load_dotenv()

app = Flask(__name__)
app.secret_key = "student-skill-gap-secret-key"

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-3.5-flash"


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------

@app.route("/")
def home():
    return render_template("home.html")


# ---------------------------------------------------------
# SKILLS PAGE
# ---------------------------------------------------------

@app.route("/skills")
def skills():
    return render_template("skills.html")


# ---------------------------------------------------------
# GEMINI IDENTIFIES SKILLS FOR ANY SELECTED ROLE
# ---------------------------------------------------------

@app.route("/generate-skills", methods=["POST"])
def generate_skills():

    name = request.form.get("name")
    career = request.form.get("career")

    prompt = f"""
You are an expert technology career advisor.

A student wants to become:

{career}

Identify the most important technical skills required for this exact role.

Do NOT assume the role is Python Developer, Data Analyst, or Web Developer.

Understand the exact career/technology role entered by the student.

Return 6 to 10 important technical skills.

For every skill provide:

- skill_name
- required_level from 1 to 10
- explanation

Include technologies, programming languages, frameworks,
databases, tools, concepts, platforms or other technical skills
that are genuinely relevant to this career.

Do not include soft skills.

Return ONLY valid JSON.

Example:

[
    {{
        "skill_name": "HTML5",
        "required_level": 9,
        "explanation": "Used to structure web pages."
    }},
    {{
        "skill_name": "CSS3",
        "required_level": 9,
        "explanation": "Used for styling and responsive layouts."
    }}
]
"""

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        # Get Gemini response
        ai_text = response.text.strip()

        # Remove markdown code fences if Gemini adds them
        ai_text = re.sub(
            r"```json",
            "",
            ai_text,
            flags=re.IGNORECASE
        )

        ai_text = re.sub(r"```", "", ai_text)

        ai_text = ai_text.strip()

        # Convert JSON into Python list
        skills_data = json.loads(ai_text)

        # Save information for next pages
        session["name"] = name
        session["career"] = career
        session["skills"] = skills_data

        return render_template(
            "rate_skills.html",
            name=name,
            career=career,
            skills=skills_data
        )

    except Exception as e:

        return f"""
        <h2>Gemini Error</h2>
        <p>{str(e)}</p>
        <p>Please try again after a few seconds.</p>
        """


# ---------------------------------------------------------
# RATE SKILLS + GENERATE AI QUIZ
# ---------------------------------------------------------

@app.route("/rate-skills", methods=["POST"])
def rate_skills():

    skills = session.get("skills", [])

    name = session.get("name", "")
    career = session.get("career", "")

    # Store student's skill ratings
    student_skills = []

    for i, skill in enumerate(skills):

        rating = request.form.get(
            f"skill_{i}",
            "0"
        )

        try:
            rating = int(rating)
        except:
            rating = 0

        rating = max(0, min(10, rating))

        student_skills.append({
            "skill_name": skill["skill_name"],
            "required_level": skill["required_level"],
            "student_level": rating
        })

    # Save ratings
    session["student_skills"] = student_skills

    # Convert skills into JSON text for Gemini
    skills_text = json.dumps(
        student_skills,
        indent=2
    )

    # -----------------------------------------------------
    # GENERATE PERSONALIZED AI QUIZ
    # -----------------------------------------------------

    prompt = f"""
You are an AI technical skill assessment system.

Student career goal:

{career}

The student's current self-rated technical skills are:

{skills_text}

Create a technical assessment specifically for this student.

IMPORTANT:

- Questions must be based on the skills listed above.
- Questions must match the student's current level.
- If a student rates a skill 0-3, ask beginner questions.
- If a student rates a skill 4-6, ask intermediate questions.
- If a student rates a skill 7-10, ask advanced questions.
- Do NOT ask unrelated questions.
- Do NOT always ask the same questions.
- Questions should change depending on the selected career and skills.
- Create exactly 8 questions.
- Each question must have 4 options.
- Only one option must be correct.

Return ONLY valid JSON.

Format:

[
    {{
        "skill": "HTML5",
        "level": "beginner",
        "question": "Which HTML tag is used for a paragraph?",
        "options": [
            "<p>",
            "<div>",
            "<h1>",
            "<span>"
        ],
        "correct_answer": 0
    }}
]
"""

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        ai_text = response.text.strip()

        # Remove markdown code fences
        ai_text = re.sub(
            r"```json",
            "",
            ai_text,
            flags=re.IGNORECASE
        )

        ai_text = re.sub(
            r"```",
            "",
            ai_text
        )

        ai_text = ai_text.strip()

        # Convert Gemini JSON into Python
        quiz_questions = json.loads(ai_text)

        # Save quiz
        session["quiz"] = quiz_questions

        return render_template(
            "quiz.html",
            name=name,
            career=career,
            questions=quiz_questions
        )

    except Exception as e:

        return f"""
        <h2>Quiz Generation Error</h2>
        <p>{str(e)}</p>
        <p>Please try again.</p>
        """


# ---------------------------------------------------------
# QUIZ SUBMISSION + AI ASSESSMENT
# ---------------------------------------------------------

@app.route("/quiz", methods=["POST"])
def quiz():

    questions = session.get(
        "quiz",
        []
    )

    student_skills = session.get(
        "student_skills",
        []
    )

    career = session.get(
        "career",
        "Technology"
    )

    if not questions:
        return "Quiz session expired. Please start again."

    score = 0

    skill_results = {}

    # -----------------------------------------------------
    # CHECK ANSWERS
    # -----------------------------------------------------

    for i, question in enumerate(questions):

        answer = request.form.get(
            f"q{i}"
        )

        correct_answer = str(
            question["correct_answer"]
        )

        skill = question["skill"]

        # Create skill result if needed
        if skill not in skill_results:

            skill_results[skill] = {
                "correct": 0,
                "total": 0
            }

        skill_results[skill]["total"] += 1

        # Check answer
        if answer == correct_answer:

            score += 1

            skill_results[skill]["correct"] += 1

    total_questions = len(questions)

    percentage = round(
        (score / total_questions) * 100
    )

    # -----------------------------------------------------
    # CREATE DATA FOR GEMINI
    # -----------------------------------------------------

    assessment_data = {
        "career": career,
        "self_rated_skills": student_skills,
        "quiz_score": f"{score}/{total_questions}",
        "percentage": percentage,
        "skill_wise_results": skill_results
    }

    assessment_text = json.dumps(
        assessment_data,
        indent=2
    )

    # -----------------------------------------------------
    # GEMINI FINAL ASSESSMENT
    # -----------------------------------------------------

    prompt = f"""
You are an AI career skill-gap analyzer.

Analyze the following student's assessment.

{assessment_text}

The student wants to become:

{career}

Provide a personalized technical skill assessment.

IMPORTANT:

Compare:

1. Student's self-rated skill level
2. Required skill level
3. Quiz performance

Identify:

- Strong skills
- Weak skills
- Skill gaps
- Skills that need immediate improvement
- Recommended topics for each weak skill
- Overall career readiness percentage

Do not blindly trust the student's self-rating.

Use the quiz performance to identify whether
the student's claimed skill level appears accurate.

Give practical recommendations suitable for a college student.

Keep the answer clear and easy to understand.
"""

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        ai_assessment = markdown.markdown(
            response.text,
            extensions=["extra"]
        )

    except Exception:

        ai_assessment = (
            "AI assessment could not be generated at the moment. "
            "Please try again."
        )

    # -----------------------------------------------------
    # FINAL RESULT
    # -----------------------------------------------------

    return render_template(
        "quiz_result.html",
        career=career,
        score=score,
        total_questions=total_questions,
        percentage=percentage,
        ai_assessment=ai_assessment
    )


# ---------------------------------------------------------
# START APPLICATION
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)