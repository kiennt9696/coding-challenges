from flask import render_template

from helpers.vocalbulary_quiz import VocabularyQuizSDK


def index():
    # Select 2 random questions
    quiz = VocabularyQuizSDK()
    selected_questions = quiz.get_quiz("quiz1")
    params = {
        "num_questions": len(selected_questions["questions"]),
    }
    num_questions = params.get('num_questions')
    quiz_title =  params.get('quiz_title', 'Vocabulary Quiz')

    # Pass the num_questions variable to the template
    return render_template('index.html', questions=selected_questions, num_questions=num_questions, quiz_title=quiz_title)