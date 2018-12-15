import logging

from flask import Flask, request

from functions import entrypoint


def create_app():
    """Create a development Flask application.

    Returns:
        A Flask application that is used only for Debug and Integration
            tests. This is not meant to be used, because the main
            entrypoint is expected to be executed in Google Cloud Functions.
    """
    app = Flask(__name__)

    @app.route("/webhook", methods=["POST"])
    def webhook():
        return entrypoint(request)

    return app


if __name__ == "__main__":
    # Webhook executed in a running Flask server. 
    # NOTE: This mode MUST be used only for debug and MUST NEVER include
    # any kind of logic because it will NOT be executed in a Google 
    # Cloud Function
    logging.warning("'/webhook' function is meant to be deployed in Google Cloud Function")
    app = create_app()
    app.run()
