import os
import discord
from dotenv import load_dotenv
from support.logging import *
from respite import channels, commands, messages, roles


client = discord.Client()

@client.event
async def on_ready():
    Logger.log('The bot is now active.')
    channel = discord.utils.get(client.get_all_channels(), name=channels.BOT_CHANNEL)
    await channel.send(messages.WELCOME)

@client.event
async def on_message(message):
    if message.content.startswith(commands.SYNC_CHARACTER) and message.author.bot == False:
        cmd = message.content[1:]
        if cmd.startswith(commands.ECHO):
            content = cmd[len(commands.ECHO):].strip()
            print(content)
            await message.channel.send(content)

load_dotenv()
client.run(os.getenv('DISCORD_TOKEN'))