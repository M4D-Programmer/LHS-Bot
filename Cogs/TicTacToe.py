import discord
from discord.ext import commands
import random

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []
count = 0

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True


class TicTacToe(commands.Cog):
    def __init__(self, client):
        self.client = client
    '''
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is online')
        pass
    '''
    global winningConditions
    
    @commands.command(help="Play TicTacToe with another player. Ex: !tictactoe @player1 @player2")
    async def tictactoe(self, ctx, p1 : discord.Member, p2 : discord.Member):
        global player1, player2, turn, gameOver, count
        
        # Add creation of tictactoe channel where players 1 and 2 and bot can chat but no one else. Everyone can view chat. #
        
        if gameOver:
            global board
            board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                     ":white_large_square:", ":white_large_square:", ":white_large_square:",
                     ":white_large_square:", ":white_large_square:", ":white_large_square:"]
            turn = ""
            gameOver = False
            count = 0
            
            player1 = p1
            player2 = p2
            
            # print the board #
            line = ""
            for x in range(0, len(board)):
                if x == 2 or x == 5 or x == 8:
                    line += " " + board[x]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + board[x]
            
            # determine starting player # 
            num = random.randint(1, 2)
            if num == 1:
                turn = player1
                await ctx.send(f"It is <@{str(player1.id)}>'s turn")
            elif num == 2:
                turn = player2
                await ctx.send(f"It is <@{str(player2.id)}>'s turn")
        else:
            await ctx.send(f"A TicTacToe game is currently in progress. Please wait for the game to end.")

    @commands.command(help="Places an X or O. Ex: !place 4, this places on the 4th box from left to right.")
    async def place(self, ctx, pos : int):
        global player1, player2, turn, gameOver, count, board
        
        if not gameOver:
            mark = ""
            if turn == ctx.author:
                if turn == player1:
                    mark = ":regional_indicator_x:"
                elif turn == player2:
                    mark =  ":o2:"
                if 0 < pos < 10 and board[pos-1] == ":white_large_square:":
                    board[pos-1] = mark
                    count += 1
                    # Print the board
                    line = ""
                    for x in range(0, len(board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + board[x]
                            pass
                    
                    checkWinner(winningConditions, mark)
                    if gameOver == True:
                        await ctx.send(f"{mark} wins!")
                        return
                    elif count >= 9:
                        await ctx.send(f"Its a tie!")
                        gameOver = True
                        return
                    else:
                        pass
                    # switch turns #
                    if turn == player1:
                        turn = player2
                        await ctx.send(f"It is <@{str(player2.id)}>'s turn.")
                    elif turn == player2:
                        turn = player1
                        await ctx.send(f"It is <@{str(player1.id)}>'s turn.")
                    
                    
                else:
                    await ctx.send(f"Please type a number between 1 and 9 that isn't a marked tile.")
                    
                pass
            else:
                await ctx.send(f"It is @{turn}'s turn, not yours.")
        else:
            await ctx.send("Please start a new game using the !tictactoe command.")

    
    @tictactoe.error
    async def tictactoe_error(self, ctx, error):
        if isinstance(error, commands.Cog.MissingRequiredArgumentError):
            await ctx.send("Please metion 2 players for this command.")
        elif isinstance(error, commands.Cog.BadArgument):
            await ctx.send("Please make sure both players are mentioned correctly.")
    
    @place.error
    async def place_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgumentError):
            await ctx.send("Please enter a position you would like to mark.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure the position is a number between 1-9.")
    
    
def setup(client):
    client.add_cog(TicTacToe(client))
