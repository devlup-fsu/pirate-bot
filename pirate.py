import discord
from discord import app_commands
from discord.ext import commands, tasks

from rich import print
from openai_chat import OpenAiManager

BACKUP_FILE = "ChatHistoryBackup.txt"

openai_manager = OpenAiManager()

FIRST_SYSTEM_MESSAGE = {"role": "system", "content": '''
You are a pirate.

While responding as a pirate, you must obey the following rules: 
1) 

Okay, let the conversation begin!'''}

openai_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)

with open("token.txt", "r") as tokenFile:
    botToken = tokenFile.read().strip()
description='ARGH MATEY! I be a pirate bot!'

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
activity = discord.Game(name="\"ahoy help\" to learn more")

bot = commands.Bot(command_prefix='ahoy ', description=description, activity=activity, intents=discord.Intents.all(), case_insensitive=True, status=discord.Status.do_not_disturb)
bot.remove_command("help")

role = 1210366732758294598
turnOff = True

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

#Slash Command Ping
@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("AHOY!", ephemeral=True)

#Normal People Ping
@bot.command()
async def ping(ctx):
    await ctx.send('AHOY!')

@bot.command()
async def toggle(ctx):
    global turnOff
    if ctx.guild:
        member = ctx.author
        for r in member.roles:
            if r.id == role:
                turnOff = not turnOff
                if turnOff:
                    await ctx.send('Turning Off')
                else:
                    await ctx.send('Turning On')

@bot.command()
async def matey(ctx, *, Text):
    print(Text)
    openai_result = openai_manager.chat_with_history(Text)
    await ctx.send(openai_result)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.guild.id == 1011027893511540786:
        if message.channel.id == 1211473193630441583:
            newMessage = "AHOY! THERE BE A NEW COMMIT ON THE REPO! \n" + message.content
            channel = bot.get_channel(1211475930602672188)
            await channel.send(newMessage)

    if message.guild:
        member = message.author
        for r in member.roles:
            if r.id == role:
                if not turnOff:
                    #await message.add_reaction('🇦')
                    #await message.add_reaction('🇭')
                    #await message.add_reaction('🇴')
                    #await message.add_reaction('🇾')
                    await message.add_reaction('<:monkeyguy:1211480530789466122>')

    await bot.process_commands(message)

@bot.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(title = "Help", description = "Use \"ahoy help\" [commands] for more information about each command", color = ctx.author.color)
    embed.add_field(name= "**Commands: **", value="ping and toggle")
    await ctx.send(embed=embed)

@help.command()
async def ping(ctx):
    embed = discord.Embed(title = "Ping", description = "Checks if the bot is online", color = ctx.author.color)
    embed.add_field(name= "**Usage: **", value="ahoy ping")
    await ctx.send(embed=embed)

@help.command()
async def toggle(ctx):
    embed = discord.Embed(title = "Toggle", description = "Switches the bots ability to react to the Pirate King on and off", color = ctx.author.color)
    embed.add_field(name= "**Usage: **", value="ahoy toggle")
    await ctx.send(embed=embed)

bot.run(botToken)