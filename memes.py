import aiohttp
from discord.ext import commands


class MemesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="meme")
    async def get_meme(self, ctx):
        """
        Send a random meme
        """
        async with aiohttp.ClientSession() as session:
            async with session.get('https://meme-api.herokuapp.com/gimme/1') as r:
                if r.status == 200:
                    json = await r.json()
                    meme_link = json.get("memes")[0].get("url")
                    await ctx.send(meme_link)
def setup(bot):
    bot.add_cog(MemesCog(bot))
