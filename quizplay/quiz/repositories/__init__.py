from quiz.extensions import redis_client
from quiz.repositories.leaderboard import LeaderBoardRepo
from quiz.repositories.quizplay import QuizPlayRepo

quiz_play_repo = QuizPlayRepo(client=redis_client)
leaderboard_repo = LeaderBoardRepo(client=redis_client)



