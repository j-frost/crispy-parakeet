import discord
import random
import numpy
import asyncio
from discord import VoiceChannel, Member

class CrispyParakeet(discord.Client):

    async def distribute(self, source: VoiceChannel, channel1: VoiceChannel, channel2: VoiceChannel):
        [team1, team2] = numpy.array_split(random.shuffle(source.members), 2)
        asyncio.run(move_all_to(team1, channel1))
        asyncio.run(move_all_to(team2, channel2))


async def move_all_to(members: [Member], channel: VoiceChannel):
    await asyncio.gather(*[member.move_to(channel) for member in members])
