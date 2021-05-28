import os

import discord

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


if __name__ == "__main__":
    client.run(DISCORD_TOKEN)
