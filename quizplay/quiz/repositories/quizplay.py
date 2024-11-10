from redis import Redis

from helpers.redis_client import ClientBase, RedisClient


class QuizPlayRepo(ClientBase):
    def __init__(self, client: RedisClient):
        super().__init__(client)

    def set_score(self, quiz_id: str, user_id:str, score: int) -> None:
        """
        Using ZADD to set the user's score in the sorted set (leaderboard)
        O(log(n))
        """
        leaderboard_key = f"leaderboard:{quiz_id}"

        self.redis.get_instance(quiz_id).zadd(leaderboard_key, {user_id: score}, nx=True)

    def update_score(self, quiz_id: str, user_id:str, score: int) -> None:
        """
        Using ZINCRBY to add/update the user's score in the sorted set (leaderboard)
        O(log(n))
        """
        leaderboard_key = f"leaderboard:{quiz_id}"

        self.redis.get_instance(quiz_id).zincrby(leaderboard_key, score, user_id)

