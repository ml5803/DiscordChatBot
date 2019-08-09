import discord
from discord.ext import commands
import copy

class connectFour(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rows = 6
        self.cols = 7
        self.reactions = ""
        self.games = {}
        #games is dictionary of : {"messageid": board, user1, user2,which user,message object, dictionary of next avaiable in a col}
        #format of secondary dictionary: {col:row}

    @commands.command(pass_context=True)
    async def c4(self,ctx):
        await self.c4_new(ctx.message.author, ctx.message.mentions[0], ctx.message.channel)

    def makeBoard(self):
        board = []
        for i in range(0, self.rows):
            board.append([" "] * self.cols)
        print(board)
        return board

    def makeGridStr(self,lst,str):
        for row in range(self.rows):
            for col in range(self.cols):
                if (lst[row][col] == "x"):
                    str += ":red_circle:"
                if (lst[row][col] == "o"):
                    str += ":white_circle:"
                if (lst[row][col] == " "):
                    str += ":white_large_square:"
            str += "\n"
        return str

    async def c4_new(self,user1, user2, channel):
        response = "<@" + str(user1.id) + "> is playing " + "<@" + str(user2.id) + ">\n"
        response += "Go go: \n"
        msg = await channel.send(response)
        await self.makeButtonsC4(msg)
        game_id = msg.id
        self.games[game_id] = [self.makeBoard(), str(user1.id),str(user2.id),1, msg,{}]
        response = self.makeGridStr(self.games[game_id][0], response)
        await msg.edit(content=response)
        print("game id", game_id)
        self.print_grid(self.games[game_id][0])

    def print_grid(self,lst):
        print("grid:")
        for i in range(len(lst)):
            print(lst[i])

    async def makeButtonsC4(self,msg):
        await msg.add_reaction(u"\u0031" + u"\u20E3")  #1
        await msg.add_reaction(u"\u0032" + u"\u20E3")  #2
        await msg.add_reaction(u"\u0033" + u"\u20E3")  #3
        await msg.add_reaction(u"\u0034" + u"\u20E3")  #4
        await msg.add_reaction(u"\u0035" + u"\u20E3")  #5
        await msg.add_reaction(u"\u0036" + u"\u20E3")  #6
        await msg.add_reaction(u"\u0037" + u"\u20E3")  #7

    #todo: make on_reaction_add, find_last_free_spot, win_condition,

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.id != 416235862746202113:
            self.decodeMove(reaction,user)
            await self.boardUpdate(self.games[reaction.message.id])
            await reaction.message.remove_reaction(reaction.emoji,user)

    def decodeMove(self,reaction, user):
        #no switch statements in python
        dispatch = {"1⃣":0,"2⃣":1,"3⃣":2,"4⃣":3,"5⃣":4,"6⃣":5,"7⃣":6}
        col = dispatch[str(reaction.emoji)]
        symbol_dict = {1:"x", 2:"o"}
        symbol = symbol_dict[self.games[reaction.message.id][3]]
        if col not in self.games[reaction.message.id][5].keys(): #first move of the column
            self.games[reaction.message.id][0][self.rows-1][col] = symbol
            self.games[reaction.message.id][5][col] = 1
        else:
            self.games[reaction.message.id][0][self.rows - 1 - self.games[reaction.message.id][5][col]][col] = symbol
            self.games[reaction.message.id][5][col] += 1
        self.print_grid(self.games[reaction.message.id][0])
        return

    async def boardUpdate(self,game):
        response = "<@" + game[1] + ">'s and <@" + game[2] +">" + " Game: \n"
        response = self.makeGridStr(game[0], response)
        await game[4].edit(content = response)

    @commands.command()
    async def test(self,ctx):
        print(self.games)