from flask import request, jsonify

from quiz.services import quizplay_service


def join_quiz(quiz_id):
    data = request.get_json()
    user_id = data.get("user_id")
    quizplay_service.join_quiz(quiz_id, user_id)
    return "", 204


def submit_answer(quiz_id):
    data = request.get_json()
    user_id = data.get("user_id")
    question_id = data.get("question_id")
    answer = data.get("answer")
    correct = quizplay_service.submit_answer(quiz_id, user_id, question_id, answer)
    result = {
        "status": "correct" if correct else "incorrect"
    }
    return jsonify(result), 200

