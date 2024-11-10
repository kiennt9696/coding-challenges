from functools import lru_cache


class VocabularyQuizSDK(object):
    """
    This is a mock class to return quiz info
    """
    def __init__(self):
        pass

    @lru_cache(maxsize=1000)
    def get_quiz(self, quiz_id):
        """
        this function should be cache in production because it's rarely changed
        """
        sample_quiz = {
            "id": quiz_id,
            "questions": {
                "1": {
                    "question": "How old is Bob",
                    "options": {"A": "1", "B": "2", "C": "3"}
                },
                "2": {
                    "question": "How old is Alice",
                    "options": {"A": "1", "B": "2", "C": "3"}
                },
                "3": {
                    "question": "How old is Snow",
                    "options": {"A": "1", "B": "2", "C": "3"}
                }
            }
        }
        return sample_quiz

    @lru_cache(maxsize=1000)
    def get_quiz_answer(self, quiz_id):
        """
        question_id : answer & point
        this function should be cache in production because it's rarely changed
        """
        sample_answer = {
            "1": {
                "answer": "A",
                "point": 10
            },
            "2": {
                "answer": "B",
                "point": 20
            },
            "3": {
                "answer": "C",
                "point": 30
            },

        }
        return sample_answer
