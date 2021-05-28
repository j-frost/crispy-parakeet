import os

import discord
from flask import Flask

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


app = Flask(__name__)


@app.route("/")
def hello_world():
    return


if __name__ == "__main__":
    client.run(DISCORD_TOKEN)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
