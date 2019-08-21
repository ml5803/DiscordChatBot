import discord
from discord.ext import commands

class TTT2p(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reactions = "↖⬆↗⬅⏺➡↙⬇↘"
        self.ttt2p_games = {}

    @commands.command(pass_context=True)
    async def ttt2p(self, ctx):
        """ Tic Tac Toe """
        await self.ttt2p_new(ctx.message.author, ctx.message.mentions[0], ctx.message.channel)

    async def ttt2p_new(self,user1, user2, channel):
        response = "<@" + str(user1.id) + "> is playing " + "<@" + str(user2.id) + ">\n"
        response += "Go go: \n"
        msg = await channel.send(response)
        await self.makeButtons2p(msg)
        game_id = msg.id
        self.ttt2p_games[game_id] = [self.makeBoard(), str(user1.id),str(user2.id),1, msg]
        response = self.makeGridStr(self.ttt2p_games[game_id][0], response)
        await msg.edit(content = response)
        print(self.ttt2p_games[game_id])

    def makeGridStr(self, lst, str):
        for row in range(0,3):
            for col in range(0,3):
                if (lst[row][col] == "x"):
                    str += ":regional_indicator_x:"
                if (lst[row][col] == "o"):
                    str += ":regional_indicator_o:"
                if (lst[row][col] == " "):
                    str += ":white_large_square:"
            str += "\n"
        return str

    def makeBoard(self):
        board = []
        for i in range(0,3):
            board.append([" ", " ", " "])
        return board

    async def makeButtons2p(self, msg):
        await msg.add_reaction(u"\u2196")  # 0 tl
        await msg.add_reaction(u"\u2B06")  # 1 t
        await msg.add_reaction(u"\u2197")  # 2 tr
        await msg.add_reaction(u"\u2B05")  # 3 l
        await msg.add_reaction(u"\u23FA")  # 4 mid
        await msg.add_reaction(u"\u27A1")  # 5 r
        await msg.add_reaction(u"\u2199")  # 6 bl
        await msg.add_reaction(u"\u2B07")  # 7 b
        await msg.add_reaction(u"\u2198")  # 8 br

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if (str(user) != "Sleepy#9088" and reaction.emoji in self.reactions ):
            game_id = reaction.message.id
            curr_game = self.ttt2p_games[game_id]
            if curr_game[curr_game[3]]==str(user.id):
                move = self.decodeMove(str(reaction.emoji))
                #print(move)
                if curr_game[3] == 1:
                    if curr_game[0][move[0]][move[1]] == " ":
                        curr_game[0][move[0]][move[1]] = 'x'
                        if curr_game[3] == 1:
                            curr_game[3] = 2
                        elif curr_game[3] == 2:
                            curr_game[3] = 1
                if curr_game[3] == 2:
                    if curr_game[0][move[0]][move[1]] == " ":
                        curr_game[0][move[0]][move[1]] = 'o'
                        if curr_game[3] == 1:
                            curr_game[3] = 2
                        elif curr_game[3] == 2:
                            curr_game[3] = 1
            print(curr_game)
            await self.boardUpdate(curr_game)
            if (self.checkWin(curr_game[0],'x')==2 or self.checkWin(curr_game[0],'o')==2):
                response = "By the decree of SleepyBot, I declare <@" + str(user.id) + "> as the crowned penguin!"
                await reaction.message.delete()
                await reaction.message.channel.send(response)
                del self.ttt2p_games[game_id]
            if (self.checkWin(curr_game[0],'x')==1):
                response = "Game doo doo. No one won (')>!"
                await reaction.message.delete()
                await reaction.message.channel.send(response)
                del self.ttt2p_games[game_id]


    async def boardUpdate(self,game):
        response = "<@" + game[1] + ">'s and <@" + game[2] +">" + " Game: \n"
        response = self.makeGridStr(game[0], response )
        await game[4].edit(content = response)

    def decodeMove(self, emoji):
        dict = {
            u"\u2196": (0,0),
            u"\u2B06": (0,1),
            u"\u2197": (0,2),
            u"\u2B05": (1,0),
            u"\u23FA": (1,1),
            u"\u27A1": (1,2),
            u"\u2199": (2,0),
            u"\u2B07": (2,1),
            u"\u2198": (2,2)
        }
        return dict[emoji] if emoji in dict else None

    def checkWin(self,board,char):
        winConditions = [[(0,0),(1,1),(2,2)],[(0,2),(1,1),(2,0)], #diagonals
                         [(0,0),(0,1),(0,2)],[(1,0),(1,1),(1,2)],[(2,0),(2,1),(2,2)], #rows
                         [(0,0),(1,0),(2,0)],[(0,1),(1,1),(2,1)],[(0,2),(1,2),(2,2)] #columns
                        ]

        #if win condition, return 2
        for condition in winConditions:
            if(board[condition[0][0]][condition[0][1]] == char and board[condition[1][0]][condition[1][1]] == char and board[condition[2][0]][condition[2][1]] == char):
                print("We have a winner")
                return 2

        #if draw return 1
        move = 0
        for row in board:
            for cell in row:
                if cell == "x" or cell == "o":
                    move+=1
        if move >= 9:
            print("Game draw")
            return 1

        #if game ongoing, return 0
        return 0
