import discord


class CrispyParakeet(discord.Client):

    async def on_message(self, message):
        if message.author == self.user or self.user.id not in map(lambda mention: mention.id, message.mentions):
            print('message not for me')
            return

        arguments = message.content.split(' ')
        if len(arguments) < 5:
            await message.channel.send("I don't get it. There's not enough arguments here :?")
            return

        command = arguments[1]
        if command != 'move':
            await message.channel.send(f"Sorry, I don't understand what I have to do when you say {command}")

        source_name = arguments[2]
        target_1_name = arguments[3]
        target_2_name = arguments[4]

        await message.channel.send(f'Alrighty ;) trying to {command} everyone from {source_name} randomly into {target_1_name} and {target_2_name}')

        target_1_channel = next(chan for chan in message.guild.voice_channels if chan.name == target_1_name)
        message.author.move_to(target_1_channel)

        await message.channel.send(f'Should be done now :)')
