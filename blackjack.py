import discord
from discord.ext import commands

class blackjack(commands.Cog):
    import discord
    from discord.ext import commands

    deck = {"A":(1,11),"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"J":10,"Q":10,"K":10}
    cards = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]

    def __init__(self, bot):
        self.bot = bot
        self.reaction = None
        self.in_game = False
        self.num_players = 0
        #player has tuples : user: (message, hand, ongoing?, busted?)
        self.players = {}

    @commands.command(pass_context=True)
    async def bj(self,ctx):
        if self.in_game:
            await ctx.message.channel.send("A game is already in progress.")
            return
        msg = await ctx.message.channel.send( "A game of BlackJack will start soon. React to join! ( ')> \n"
                                              "Say $start_bj when all the players have joined!")
        await msg.add_reaction(u"\u2705")  # check mark

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if self.in_game:
            await reaction.message.channel.send("Sorry <@" + user.id + ">, a game is in progress. Join the next one! ( ')>")
            return
        if (str(user.id) != "416235862746202113" and reaction.emoji == "✅"): #if not bot and not correct reaction, ignore
            if user not in self.players:
                self.players[user] = [reaction.message, [], True, False]
                self.num_players+=1
                print(user, " has been added.")
            await user.send("You have joined the game of BlackJack! ( ')>")
            await reaction.message.channel.send( "<@" + str(user.id) + "> has joined the game")
            print(self.players , " are the players")

    @commands.command(pass_context=True)
    async def start_bj(self,ctx):
        print("BlackJack starting")
        if self.in_game:
            await ctx.message.channel.send('Game has already started.')
            return
        if self.num_players == 0:
            await ctx.message.channel.send("Can't start with no players!")
            return
        await ctx.message.channel.send('The game of BlackJack is now starting!')
        await ctx.message.channel.send("Check your DMs. I've sent your hands. ( ')> ")
        for elem in self.players.keys():
            self.players[elem][1].append(self.hit())
            self.players[elem][1].append(self.hit())
            card_str = ""
            for card in self.players[elem][1]:
                card_str += card + " "
            await elem.send("Respond with ** hit ** or ** stay ** to play. If you get over 21, you out!")
            await elem.send("Your hand: " + card_str)
            await elem.send(self.sum_hand(self.players[elem][1]))
        self.in_game = True

    @commands.command(pass_context=True)
    async def stop_bj(self,ctx):
        self.in_game = False
        self.players.clear()
        self.num_players = 0
        await ctx.message.channel.send("Game of BlackJack has stopped. Type $bj to start another!")

    def hit(self):
        import random
        return self.cards[random.randint(0, 12)]

    def sum_hand(self, lst):
        temp = []
        count = 0
        #move all the As to the back
        for elem in lst:
            if elem != "A":
                temp.append(elem)
            else:
                count+=1
        for i in range(count):
            temp.append("A")

        sum = 0
        for elem in temp:
            if elem != "A":
                sum += self.deck[elem]
            else:
                pos = self.deck["A"]
                if sum + pos[1] > 21: #if 11 is too big, add 1 instead
                    sum += pos[0]
                else:
                    sum += pos[1]
        return sum

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author not in self.players:
            return
        message.content = message.content.lower()
        if message.author.id != 416235862746202113: #don't respond to bot
            if self.in_game and message.author not in self.players.keys() and (message.content == "hit" or message.content == "stay"):
                await message.channel.send("You not even in the game! <@" + str(message.author.id) + ">")
                return
            if self.in_game and self.players and self.players[message.author][2] == False: #if not on-going
                print("he's done already")
                await message.author.send("Stop it. You done!")
                return
            if not self.in_game and (message.content == "hit" or message.content == "stay"): #can't hit or stay before you even get your cards
                await message.author.send("Yo! Relax... take a chill pill. We didn't start yet!")
                return
            if message.content == "hit":
                print(message.author, " has hit")
                self.user_hit(message)
                card_str = ""
                for card in self.players[message.author][1]:
                    card_str += card + " "
                await message.author.send("Your hand: " + card_str)
                temp_sum = self.sum_hand(self.players[message.author][1])
                await message.author.send("The sum of your current hand is: " + str(temp_sum))
                if temp_sum == 21:
                    await message.author.send("Not bad. Let's wait for others to finish.")
                    await self.players[message.author][0].channel.send("<@" + str(message.author.id) + "> has concluded.")
                    self.players[message.author][2] = False
                    self.players[message.author][3] = False
                    self.num_players-=1
                if temp_sum > 21:
                    await message.author.send("You got over 21! Busted. Ha. Scrub. Jk o.o. Please wait for other players to finish." )
                    self.players[message.author][2] = False
                    self.players[message.author][3] = True
                    await self.players[message.author][0].channel.send("<@" + str(message.author.id) + "> has concluded.")
                    self.num_players -= 1
            if message.content == "stay":
                print(message.author, " has stayed")
                await message.author.send("What are you? My cousin, Chicken?  Bok bok! ( ')>")
                await message.author.send("Let's wait for others to finish. Go back Khappa.")
                self.players[message.author][2] = False
                self.players[message.author][3] = False
                await self.players[message.author][0].channel.send("<@" + str(message.author.id) + "> has concluded.")
                self.num_players -= 1
            await self.game_over_check(message)

    async def game_over_check(self, message):
        #clean up to display all at once
        if self.num_players == 0 and self.players:
            print("game over")
            await self.players[message.author][0].channel.send("Everyone has concluded. Let's check the stats!")
            winners = []
            busted = []
            survived = []
            high = max([self.sum_hand(self.players[elem][1]) for elem in self.players.keys() if self.sum_hand(self.players[elem][1]) <= 21]+[-1])
            for key in self.players.keys():
                if self.sum_hand(self.players[key][1]) == high: #if score = highest valid score, is a winner
                    winners.append(key)
                if self.players[key][3]: #if busted field is checked
                    busted.append(key)
                if not self.players[key][3]: #if not busted
                    survived.append(key)
            msg = "The following people busted: \n"

            for user in busted:
                msg += "<@" + str(user.id) + "> \n"
            msg += "The following people survived (?)\n"
            for user in survived:
                msg += "<@" + str(user.id) + "> with a score of " + str(self.sum_hand(self.players[user][1])) + " \n"
            if high >= 0:
                msg += "Let's hear it for our winners with a score of " + str(high) + "! \n"
                for elem in winners:
                    msg += "<@" + str(elem.id) + "> "
            else:
               msg += "Hm... It doesn't look like anyone won. :/ \n"

            await self.players[message.author][0].channel.send(msg)

            self.players.clear()
            self.in_game = False
            self.num_players = 0

    def user_hit(self,message):
        self.players[message.author][1].append(self.hit())
