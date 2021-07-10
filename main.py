import os
import discord
from crispy_parakeet import CrispyParakeet
from flask import Flask
import threading

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')


app = Flask(__name__)


@app.route("/")
def ok():
    return 'ok'


if __name__ == "__main__":
    daemon = threading.Thread(
        name='bogus web server',
        target=app.run,
        kwargs={'host':'0.0.0.0', 'port':int(os.environ.get("PORT", 8080))}
    )
    daemon.setDaemon(True)
    daemon.start()
    CrispyParakeet().run(DISCORD_TOKEN)
