import discord
import random
import numpy
import asyncio
from discord import VoiceChannel, Member

class CrispyParakeet(discord.Client):

    async def distribute(self, src: str, chan1: str, chan2: str):
        source = await self.fetch_channel(src)
        channel1 = await self.fetch_channel(chan1)
        channel2 = await self.fetch_channel(chan2)
        [team1, team2] = numpy.array_split(random.shuffle(source.members), 2)
        asyncio.run(move_all_to(team1, channel1))
        asyncio.run(move_all_to(team2, channel2))


async def move_all_to(members: [Member], channel: VoiceChannel):
    await asyncio.gather(*[member.move_to(channel) for member in members])
