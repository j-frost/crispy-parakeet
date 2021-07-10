import discord


class CrispyParakeet(discord.Client):

    async def on_message(self, message):
        if message.author == self.user or self.user.id not in map(lambda mention: mention.id, message.mentions):
            print('message not for me')
            return

        if len(message.split(' ')) < 4:
            await message.channel.send("I don't get it. There's not enough arguments here :?")
            return

        command = message.split(' ')[0]
        source_voice_channel = message.split(' ')[1]
        target_1_voice_channel = message.split(' ')[2]
        target_2_voice_channel = message.split(' ')[3]

        await message.channel.send(f'Alrighty ;) trying to move everyone from {source_voice_channel} randomly into {target_1_voice_channel} and {target_2_voice_channel}')

        await message.channel.send(f'Should be done now :)')
