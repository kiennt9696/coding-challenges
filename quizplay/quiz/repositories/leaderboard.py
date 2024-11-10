from typing import List, Tuple

from helpers.merge_n_sorted_list import get_top_k_from_sorted_lists
from helpers.redis_client import RedisClient, ClientBase


class LeaderBoardRepo(ClientBase):
    def __init__(self, client: RedisClient):
        super().__init__(client)

    def get_user_score(self, quiz_id: str, user_id: str) -> int:
        """
        Using ZSCORE
        O(log(n))
        """
        leaderboard_key = f"leaderboard:{quiz_id}"

        # Get the score for the user
        score = self.redis.get_instance(quiz_id).zscore(leaderboard_key, user_id)
        if score is None:
            return 0
        return int(score)

    def get_user_rank(self, quiz_id: str, user_id: str) -> int:
        """
        Using ZREVRANK
        O(log(n))
        """
        leaderboard_key = f"leaderboard:{quiz_id}"

        # Get the rank for the user
        rank = self.redis.get_instance(quiz_id).zrevrank(leaderboard_key, user_id)
        if rank is None:
            return -1
        return int(rank)

    def get_top_k_players(self, quiz_id: str, k: int) -> List[Tuple[str, int]]:
        """
        Using ZREVRANGE
        O(log(n) + k)
        """
        leaderboard_key = f"leaderboard:{quiz_id}"
        top_players = self.redis.get_instance(quiz_id).zrevrange(leaderboard_key, 0, k - 1, withscores=True)
        return [(user.decode('utf-8'), int(score)) for user, score in top_players]

    def get_top_k_players_shard_by_user_id(self, quiz_id: str, k: int) -> List[Tuple[str, int]]:
        """
        Using ZREVRANGE
        """
        leaderboard_key = f"leaderboard:{quiz_id}"
        local_topk_candidates = []
        for redis_node in self.redis.instances:
            local_top_k = self.redis.instances[redis_node].zrevrange(leaderboard_key, 0, k - 1, withscores=True)
            local_topk_candidates.append(local_top_k)
        top_players = get_top_k_from_sorted_lists(local_topk_candidates, k)
        return [(user.decode('utf-8'), int(score)) for user, score in top_players]

    def get_m_users_around_rank(self, quiz_id: str, user_id: str, user_rank: int, m: int) -> List[Tuple[str, int]]:
        """
        Using ZREVRANGE
        O(log(n) + m)
        """
        leaderboard_key = f"leaderboard:{quiz_id}"
        start = max(0, user_rank - m // 2)
        end = user_rank + m // 2
        users_around_rank = self.redis.get_instance(quiz_id).zrevrange(leaderboard_key, start, end, withscores=True)
        return [(user.decode('utf-8'), int(score)) for user, score in users_around_rank]



