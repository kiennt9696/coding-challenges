from flask import request, jsonify

from quiz.services import leaderboard_service


def get_leaderboard(quiz_id):
    data = request.get_json()
    user_id = data.get("user_id")
    mode = data.get("mode")
    if mode == "score":
        score = leaderboard_service.get_user_score(user_id, quiz_id)
        return jsonify({
            "name": user_id,
            "score": score
        }), 200
    elif mode == "rank":
        rank = leaderboard_service.get_user_rank(user_id, quiz_id)
        return jsonify({
            "name": user_id,
            "rank": rank
        }), 200
    elif mode == "top":
        top_k_users = leaderboard_service.get_top_k_users(quiz_id, 3)
        return jsonify(top_k_users), 200
    elif mode == "around":
        user_rank = data.get("user_rank", -1)
        m_users_around_rank = leaderboard_service.get_m_users_around_rank(quiz_id, user_rank, 2)
        return jsonify(m_users_around_rank), 200
    return leaderboard_service.get_full_leaderboard_by_quiz(user_id, quiz_id)
