# quiz/views.py

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Question
import random


def home(request):
    """Home page view"""
    # Clear any existing quiz session
    if "quiz_questions" in request.session:
        del request.session["quiz_questions"]
    if "current_question" in request.session:
        del request.session["current_question"]
    if "score" in request.session:
        del request.session["score"]
    if "incorrect_answers" in request.session:
        del request.session["incorrect_answers"]

    return render(request, "quiz/home.html")


def start_quiz(request):
    """Initialize a new quiz with 10 random questions"""
    # Get all question IDs
    all_questions = list(Question.objects.values_list("id", flat=True))

    # Select 10 random questions
    selected_ids = random.sample(all_questions, min(10, len(all_questions)))

    # Store in session
    request.session["quiz_questions"] = selected_ids
    request.session["current_question"] = 0
    request.session["score"] = 0
    request.session["incorrect_answers"] = []

    return redirect("quiz_question")


def quiz_question(request):
    """Display the current quiz question"""
    # Check if quiz is initialized
    if "quiz_questions" not in request.session:
        return redirect("home")

    quiz_questions = request.session["quiz_questions"]
    current_index = request.session.get("current_question", 0)

    # Check if quiz is complete
    if current_index >= len(quiz_questions):
        return redirect("results")

    # Get current question
    question_id = quiz_questions[current_index]
    question = Question.objects.get(id=question_id)

    context = {
        "question": question,
        "question_number": current_index + 1,
        "total_questions": len(quiz_questions),
        "score": request.session.get("score", 0),
    }

    return render(request, "quiz/question.html", context)


def check_answer(request):
    """Check the submitted answer and return result"""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    question_id = request.POST.get("question_id")
    user_answer = request.POST.get("answer")

    question = Question.objects.get(id=question_id)
    is_correct = question.is_correct(user_answer)

    # Update score
    if is_correct:
        request.session["score"] = request.session.get("score", 0) + 1
    else:
        # Store incorrect answer
        incorrect_answers = request.session.get("incorrect_answers", [])
        incorrect_answers.append(
            {
                "question": question.question,
                "user_answer": user_answer,
                "correct_answer": question.correct_answer,
                "options": dict(question.get_options()),
            }
        )
        request.session["incorrect_answers"] = incorrect_answers

    request.session.modified = True

    return JsonResponse(
        {"is_correct": is_correct, "correct_answer": question.correct_answer}
    )


def next_question(request):
    """Move to the next question"""
    request.session["current_question"] = request.session.get("current_question", 0) + 1
    request.session.modified = True
    return redirect("quiz_question")


def results(request):
    """Display quiz results"""
    if "quiz_questions" not in request.session:
        return redirect("home")

    context = {
        "score": request.session.get("score", 0),
        "total_questions": len(request.session.get("quiz_questions", [])),
        "incorrect_answers": request.session.get("incorrect_answers", []),
    }

    return render(request, "quiz/results.html", context)
