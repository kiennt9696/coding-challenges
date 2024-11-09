from helpers.vocalbulary_quiz import VocabularyQuizSDK
from quiz.repositories import quiz_play_repo, leaderboard_repo
from quiz.services.leaderboard import LeaderboardService
from quiz.services.quizplay import QuizPlayService

quizplay_service = QuizPlayService(quiz_play_repo=quiz_play_repo, quiz_sdk=VocabularyQuizSDK())
leaderboard_service = LeaderboardService(leaderboard_repo=leaderboard_repo)