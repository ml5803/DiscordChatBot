import random
import discord
from tictactoe import TTT
from tictactoe2p import TTT2p
from blackjack import blackjack
import asyncio
from discord.ext import commands

client = discord.Client()
bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'), description='Sleepy')

#check connection
@bot.event
async def on_ready():
    print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))

@bot.command(pass_context=True)
async def greet(ctx):
    await bot.say("Hi <@" + str(ctx.message.author.id) + ">")
    await bot.say("I'm SleepyBot!")

@bot.command(pass_context=True)
async def hug(ctx):
    await bot.say("I hugs " + '<@' + str(ctx.message.author.id) + '>')

@bot.command(pass_context=True)
async def slap(ctx):
    count = 0
    items = ['a majestic potato', 'a glorious apple', 'a festive donkey']
    msg = '<@' + str(ctx.message.author.id) + '> slapped '
    for member in ctx.message.mentions:
        count += 1
        msg += '<@' + str(member.id) + '> '

    msg += 'with ' + items[random.randint(0, len(items) - 1)] + "!"
    if count == 0:
        await bot.say("Fk you," + '<@' + str(ctx.message.author.id) + '> ' + ". Actually slap someone!")
    else:
        await bot.say(msg)

@bot.command()
async def roast():
    roasts = ["no u", "screw u", "your forehead brighter than your future ;)"]
    await bot.say(roasts[random.randint(0, len(roasts) - 1)])

@bot.command(pass_context=True)
async def ship(ctx, member: discord.Member = None):
    members = [x for x in bot.get_all_members()]
    guy1 = members[random.randint(0, len(members) - 1)]
    guy2 = members[random.randint(0, len(members) - 1)]
    if member is None:
        if guy1.name == guy2.name:
            await bot.say("I ship " + guy1.name + " with " + guy2.name + "!")
            await bot.say("No, that wasn't a mistake. My matchmaking software couldn't find you a match :'( .")
            return
        else:
            await bot.say("I ship " + guy1.name + " with " + guy2.name + "!")
            return
    else:
        print(member.id)
        if member.id == "233795765728706561":
            await bot.say("Sorry. He's taken. Back off my owner >:c")
            return
        if member.id == "416235862746202113":
            await bot.say("I'm matched with " + '<@' + '233795765728706561' + '>. We both Sleepy and Bots!')
            return
        if member.name == guy1.name:
            await bot.say("I'm sorry. I tried but it appears you are a lonely boi :'( .")
            return
        else:
            await bot.say('<@' + str(member.id) + '> is a perfect match with ' + guy1.name + "!")
            if (guy1.name == 'Sleepy'):
                await bot.say("Wait. Hold up. I reject your reality and substitute my own! >:(")
                await bot.say("Poof! You are now single!")
                return
            else:
                await bot.say("*Psst. Am I invited to the wedding?*")
                return

#due to TTT and TTT2p using the same emojis, only 1 may be active at a time
#bot.add_cog(TTT(bot))
bot.add_cog(TTT2p(bot))
bot.add_cog(blackjack(bot))
bot.run("This my number. Use your own!")