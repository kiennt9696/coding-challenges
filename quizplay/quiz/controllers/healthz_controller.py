from flask import current_app


def is_alive():
    current_app.logger.info("Calling Keep Alive")
    return "is alive", 200
