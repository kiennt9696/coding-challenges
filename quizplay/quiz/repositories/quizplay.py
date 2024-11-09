from redis import Redis

from helpers.util import ClientBase


class QuizPlayRepo(ClientBase):
    def __init__(self, client: Redis):
        super().__init__(client)

    def update_score(self, quiz_id: str, user_id:str, score: int) -> None:
        """
        Using ZADD to add/update the user's score in the sorted set (leaderboard)
        O(log(n))
        """
        leaderboard_key = f"leaderboard:{quiz_id}"

        self.redis.zadd(leaderboard_key, {user_id: score})
        print(leaderboard_key, score, user_id)

