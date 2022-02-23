# Python Packages
import os
import discord
from dotenv import load_dotenv

# Respite Packages
from support.logging import *
from respite import channels, commands, messages


client = discord.Client()

@client.event
async def on_ready():
    Logger.log('The bot is now active.')
    channel = discord.utils.get(client.get_all_channels(), name=channels.BOT_CHANNEL)
    await channel.send(messages.WELCOME)

@client.event
async def on_message(message):
    if message.content.startswith(commands.SYNC_CHARACTER) and message.author.bot == False:
        Logger.log(f'[{message.author} ({message.author.nick})] in {message.channel}: {message.content}')

        fields = message.content[1:].split(' ')
        cmd = fields[0]

        if cmd == commands.ECHO:
            await message.channel.send(' '.join(fields[1:]))

load_dotenv()
client.run(os.getenv('DISCORD_TOKEN'))