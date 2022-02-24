# Python Packages
import os
import discord
from dotenv import load_dotenv

# Respite Packages
from support.logging import *
from respite import channels, commands, messages
from osrs import hiscores, exceptions, rsn_register

client = discord.Client()

#AGENDA:
#TODO: Add smarter help messages.
#TODO: Figure out how to make a periodic timer event.
#TODO: Add storage for a user's HS data.
#TODO: Add a pretty reporting message.
#TODO: Support SOTW and BOTM.

@client.event
async def on_ready():
    Logger.log('The bot is now active.')
    channel = discord.utils.get(client.get_all_channels(), name=channels.BOT_CHANNEL)
    await channel.send(messages.WELCOME)

@client.event
async def on_message(message):
    if message.content.startswith(commands.SYNC_CHARACTER) and message.author.bot == False:
        Logger.log(f'[{message.author} ({message.author.nick})] in {message.channel}: {message.content}')

        fields = list(filter(None, message.content[1:].split(' ')))
        cmd = fields[0]

        if cmd == commands.ECHO:
            await message.channel.send(' '.join(fields[1:]))

        if cmd == commands.REG_RSN:
            if len(fields) > 1:
                rsn = ' '.join(fields[1:])
            else:
                return
            if rsn_register.RsnReg.register(message.author, rsn):
                await message.channel.send(f'RSN "{rsn}" is now registered to {message.author}')
            else:
                await message.channel.send(f'Could not register RSN "{rsn}" to {message.author}')

        if cmd == commands.HS_LVL:
            if len(fields) > 1:
                skill = fields[1].lower()
            else:
                return

            rsn = None
            lookup = rsn_register.RsnReg.lookup(message.author)
            if lookup is not None:
                rsn = lookup
            elif message.author.nick is not None:
                rsn = message.author.nick
            else:
                rsn = message.author.name

            ret_msg = f''
            try:
                player_data = hiscores.get_hs_info(rsn)
                skill_data = player_data['skills'].loc[skill]
                ret_msg = f"{rsn}: Level {skill} {skill_data.loc['level']} Experience: {skill_data.loc['xp']} Rank: {skill_data.loc['rank']}"
                await message.delete()
            except exceptions.BadRequestException:
                ret_msg = f'Unable to complete request.'
            except exceptions.BadRsnException:
                ret_msg = f'Could not find RSN: {rsn}'
            except KeyError:
                ret_msg = f'Could not find skill: {skill}'
            finally:
                await message.channel.send(ret_msg)

        if cmd == commands.HS_KC:
            if len(fields) > 1:
                boss = ' '.join(fields[1:]).lower()
            else:
                return

            rsn = None
            lookup = rsn_register.RsnReg.lookup(message.author)
            if lookup is not None:
                rsn = lookup
            elif message.author.nick is not None:
                rsn = message.author.nick
            else:
                rsn = message.author.name

            ret_msg = f''
            try:
                player_data = hiscores.get_hs_info(rsn)
                boss_data = player_data['bosses'].loc[boss]
                ret_msg = f"{rsn}: {boss.capitalize()} KC: {boss_data.loc['kc']} Rank: {boss_data.loc['rank']}"
                await message.delete()
            except exceptions.BadRequestException:
                ret_msg = f'Unable to complete request.'
            except exceptions.BadRsnException:
                ret_msg = f'Could not find RSN: {rsn}'
            except KeyError:
                ret_msg = f'Could not find boss: {boss}'
            finally:
                await message.channel.send(ret_msg)

        if cmd == commands.HS_CLUES:
            if len(fields) > 1:
                clue = ' '.join(fields[1:]).lower()
            else:
                return

            rsn = None
            lookup = rsn_register.RsnReg.lookup(message.author)
            if lookup is not None:
                rsn = lookup
            elif message.author.nick is not None:
                rsn = message.author.nick
            else:
                rsn = message.author.name

            ret_msg = f''
            try:
                player_data = hiscores.get_hs_info(rsn)
                clue_data = player_data['activities'].loc[clue]
                ret_msg = f"{rsn}: Clue scroll: ({clue}): {clue_data.loc['score']} Rank: {clue_data.loc['rank']}"
                await message.delete()
            except exceptions.BadRequestException:
                ret_msg = f'Unable to complete request.'
            except exceptions.BadRsnException:
                ret_msg = f'Could not find RSN: {rsn}'
            except KeyError:
                ret_msg = f'Could not find clue: {clue}'
            finally:
                await message.channel.send(ret_msg)


load_dotenv()
client.run(os.getenv('DISCORD_TOKEN'))