from discord.ext import commands

from settings import TOKEN, COMMAND_PREFIX

bot = commands.Bot(command_prefix=COMMAND_PREFIX, description="welcome bot")
if __name__ == '__main__':
    bot.load_extension("members")
    bot.load_extension("memes")
    bot.run(TOKEN, bot=True, reconnect=True)
