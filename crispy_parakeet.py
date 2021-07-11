import random

import discord
import numpy
from discord import Member, VoiceChannel


class CrispyParakeet(discord.Client):

    async def distribute(self, src: str, chan1: str, chan2: str):
        source = await self.fetch_channel(src)
        channel1 = await self.fetch_channel(chan1)
        channel2 = await self.fetch_channel(chan2)
        [team1, team2] = numpy.array_split(random.shuffle(source.members), 2)
        for member in team1:
            await member.move_to(channel1)
        for member in team2:
            await member.move_to(channel2)
