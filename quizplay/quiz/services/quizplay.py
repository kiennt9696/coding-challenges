from helpers.vocalbulary_quiz import VocabularyQuizSDK
from quiz.exceptions import InvalidParameter
from quiz.repositories.quizplay import QuizPlayRepo


class QuizPlayService(object):
    def __init__(self, quiz_play_repo: QuizPlayRepo, quiz_sdk: VocabularyQuizSDK):
        self.quiz_sdk = quiz_sdk
        self.quiz_play_repo = quiz_play_repo

    def _check_quiz_exist(self, quiz_id):
        quiz_info = self.quiz_sdk.get_quiz(quiz_id)
        if not quiz_info:
            raise InvalidParameter(error_code=4001001, params="quiz_id")

    def join_quiz(self, quiz_id, user_id) -> None:
        self._check_quiz_exist(quiz_id)
        # when joining just, score is 0
        self.quiz_play_repo.set_score(quiz_id, user_id, 0)

    def submit_answer(self, quiz_id, user_id, question_id, answer) -> bool:
        self._check_quiz_exist(quiz_id)
        quiz_answer = self.quiz_sdk.get_quiz_answer(quiz_id)
        if not quiz_answer:
            raise InvalidParameter(error_code=4001001, params="quiz_id")
        if not quiz_answer.get(question_id):
            raise InvalidParameter(error_code=4001001, params="question_id")
        if quiz_answer[question_id].get("answer") == answer:
            self.quiz_play_repo.update_score(quiz_id, user_id, quiz_answer[question_id]["point"])
            return True
        return False


