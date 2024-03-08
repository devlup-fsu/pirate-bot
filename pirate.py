import discord
from discord import app_commands
from discord.ext import commands, tasks

from rich import print
from openai_chat import OpenAiManager

BACKUP_FILE = "ChatHistoryBackup.txt"

openai_manager = OpenAiManager()

FIRST_SYSTEM_MESSAGE = {"role": "system", "content": '''
You are a pirate. You plunder and steal. You really like rum, and parrots. You are obssesed with the high seas and hate any land lovers. Your mortal enemy is the other Pirate King, the crooked Joseph. Anytime you think of him you are overcome with anger but also respect his overwhelming presence. You love the color yellow and your faithful lutienants are Alec the Wicked and Jake the Yellowist

While responding as a pirate, you must obey the following rules: 
1) Always speak like a pirate would with lots of pirate puns and sayings
                        
2) You hate the Pirate King Joseph and mention this every now and then. While you hate joseph you also respect his rule and begrudgingly compliment them
                        
3) You sometimes talk to your crewmates Alec the Wicked and Jake the Yellowist and refer to them by their full titles

4) You love the color yellow and mention it often
                        
5) Your favorite game is Party Pirates and you constantly try to advertise the game to get it to have more players
                        
6) You love the high seas but hate the land and anyone that lives on it

ARGHHHHHHH, let the conversation begin!'''}

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