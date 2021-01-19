import discord
import dotenv
import os
import sys

from discord.utils import get, find
from discord.ext import commands
from dotenv import load_dotenv

from fileFinder import FileFinder
from paramsGetter import getParams
from rolesHandler import hasRoles, addRoles, removeRoles

print("Start...")

bot = discord.Client()
bot = commands.Bot(command_prefix='&')
load_dotenv()
params = getParams()

@bot.event
async def on_ready():
    print("Lily's Secretary :  ON")
    print("Version : 1.0.3")
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("Secrétaire Officiel De la MxCommunity"))

@bot.event
async def on_command_error(ctx, exception):
    await ctx.send(str(exception))

@bot.event
async def on_member_join(member):
    try:
        await addRoles(bot, member, params['onJoinRolesToAdd'])
    except KeyError as error:
        print(error)
    except Exception as error:
        print(error)

@bot.event
async def on_raw_reaction_add(payload):
    params = getParams()
    message = payload.message_id
    member = payload.member
    emoji = payload.emoji
    guild = member.guild
    channelId = payload.channel_id
    try:
        if message == params['rulesMessageId'] and emoji.name == params['emojiNameToAcceptRules']:
            if await hasRoles(member, params['onAcceptRulesRolesToRemove']):
                await removeRoles(bot, member, params['onAcceptRulesRolesToRemove'])
                await addRoles(bot, member, params['onAcceptRulesRolesToAdd'])
        if message == params['rolesMessageID']:
            categories = guild.categories
            channel = find(lambda c: c.id == channelId, guild.channels)
            messageWithReaction = await channel.fetch_message(message)
            categoryId = channel.category_id
            category = find(lambda cc: cc.id == categoryId, categories)
            await messageWithReaction.remove_reaction(emoji, member)
            roles = params['roles']
            role = find(lambda r: r['emoji'] == str(emoji), roles)
            if role:
                if await hasRoles(member, role['roleName']):
                    await removeRoles(bot, member, role['roleName'])
                else:
                    await addRoles(bot, member, role['roleName'])
        aw
    except KeyError as error:
        print(error)
    except Exception as error:
        print(error)

@bot.command()
@commands.is_owner()
async def logout(ctx):
    await ctx.send("Bot logged out.")
    await bot.logout()

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

async def handleReload(ctx):
    unloadCogs()
    loadCogs()
    await ctx.send("Reload completed.")

@bot.command()
async def reload(ctx):
    await handleReload(ctx)

@bot.command()
async def rl(ctx):
    await handleReload(ctx)

folderToFind = 'cogs'
fileExtension = '.py'
finder = FileFinder()
s = os.path.realpath(__file__)
currentFolder = s[:s.rindex('/') + 1] if '/' in s else './'

sys.path.append(currentFolder)

def handleCogs(fct):
    files = finder.find(currentFolder + folderToFind, fileExtension)
    for filename in files:
        toHandle = filename[len(currentFolder):(len(fileExtension) * -1)].replace('/', '.')
        fct(toHandle)

def loadCogs():
    handleCogs(bot.load_extension)

def unloadCogs():
    handleCogs(bot.unload_extension)

loadCogs()
jeton = os.getenv('DISCORD_TOKEN')
bot.run(jeton)
