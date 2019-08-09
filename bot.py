import random
import discord
from tictactoe2p import TTT2p
from blackjack import blackjack
from connectfour import connectFour
from discord.ext import commands

bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'))

#check connection
@bot.event
async def on_ready():
    print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))

@bot.command(pass_context=True)
async def greet(ctx):
    await ctx.send("Hi <@" + str(ctx.message.author.id) + ">")
    await ctx.send("I'm Sleepybot!")

@bot.command(pass_context=True)
async def hug(ctx):
    await ctx.send("I hugs " + '<@' + str(ctx.message.author.id) + '>')

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
        await ctx.send('<@' + str(ctx.message.author.id) + '> ' + ", actually slap someone! or I'll show you my flipper ( ')>!")
    else:
        await ctx.send(msg)

@bot.command()
async def roast(ctx):
    roasts = ["no u", "screw u", "your forehead brighter than your future ;)"]
    await ctx.send(roasts[random.randint(0, len(roasts) - 1)])

@bot.command(pass_context=True)
async def ship(ctx, member: discord.Member = None):
    members = [x for x in bot.get_all_members()]
    guy1 = members[random.randint(0, len(members) - 1)]
    guy2 = members[random.randint(0, len(members) - 1)]
    if member is None:
        if guy1.name == guy2.name:
            await ctx.send("I ship " + guy1.name + " with " + guy2.name + "!")
            await ctx.send("No, that wasn't a mistake. My matchmaking software couldn't find you a match :'( .")
            return
        else:
            await ctx.send("I ship " + guy1.name + " with " + guy2.name + "!")
            return
    else:
        print(member.id)
        if member.id == "233795765728706561":
            await ctx.send("Sorry. He's taken. Back off my owner >:c")
            return
        if member.id == "416235862746202113":
            await ctx.send("I'm matched with " + '<@' + '233795765728706561' + '>. We ctxh Sleepy and ctxs!')
            return
        if member.name == guy1.name:
            await ctx.send("I'm sorry. I tried but it appears you are a lonely boi :'( .")
            return
        else:
            await ctx.send('<@' + str(member.id) + '> is a perfect match with ' + guy1.name + "!")
            if (guy1.name == 'Sleepy'):
                await ctx.send("Wait. Hold up. I reject your reality and substitute my own! >:(")
                await ctx.send("Poof! You are now single!")
                return
            else:
                await ctx.send("*Psst. Am I invited to the wedding?*")
                return

bot.add_cog(TTT2p(bot))
bot.add_cog(blackjack(bot))
bot.add_cog(connectFour(bot))
bot.run("Oops. My token. You use your own.")
