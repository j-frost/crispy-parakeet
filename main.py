import os
import discord

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} is here now')


if __name__ == "__main__":
    client.run(DISCORD_TOKEN)
