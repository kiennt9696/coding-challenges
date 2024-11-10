from quiz.repositories.leaderboard import LeaderBoardRepo


class LeaderboardService:
    """
    Provide multiple APIs to retrieve the Leaderboard for optimal strategy.
    """
    def __init__(self, leaderboard_repo: LeaderBoardRepo):
        self.leaderboar_repo = leaderboard_repo

    def get_user_rank(self, user_id, quiz_id):
        return self.leaderboar_repo.get_user_rank(quiz_id, user_id)

    def get_user_score(self, user_id, quiz_id):
        return self.leaderboar_repo.get_user_score(quiz_id, user_id)

    def get_top_k_users(self, quiz_id, k):
        return self.leaderboar_repo.get_top_k_players(quiz_id, k)

    def get_m_users_around_rank(self, quiz_id, user_id, user_rank, m):
        return self.leaderboar_repo.get_m_users_around_rank(quiz_id, user_id, user_rank, m)

    def get_full_leaderboard_by_quiz(self, user_id, quiz_id, k=100, m=2):
        user_score = self.get_user_score(user_id, quiz_id)
        user_rank = self.get_user_rank(user_id, quiz_id)
        top_k_players = self.get_top_k_users(quiz_id, k)
        m_users_around = self.get_m_users_around_rank(quiz_id, user_id, user_rank, m)
        res = {
            "top_users": top_k_players,
            "users_around": m_users_around,
            "current_user": {
                "score": user_score,
                "rank": user_rank
            }
        }
        return res

