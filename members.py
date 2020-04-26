import re

import discord
from discord.ext import commands


class MembersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        dialog = []
        channel = member.guild.system_channel
        if channel is not None:
            def check_mention(message):
                return self.bot.user.mentioned_in(message) and message.author == member

            dialog.append(await channel.send(
                f'Пользователь {member.mention} подключился. Пожалуйста напиши нам своё имя в таком формате: "@bot "твоё имя""'))
            try:
                while True:
                    msg = await self.bot.wait_for("message", timeout=60.0, check=check_mention)
                    dialog.append(msg)
                    regex = r"^\s*<@!\d+>\s*(.+)\s*$"
                    typed_name = re.match(regex, msg.content).group(1) if re.match(regex,
                                                                                   msg.content) is not None else None
                    if typed_name is None:
                        dialog.append(await channel.send("Что-то пошло не так. Попробуйте ещё раз"))
                        continue
                    member_name = member.display_name
                    new_nickname = f'{member_name} ({typed_name})'
                    await member.edit(nick=new_nickname)
                    return True

            except TimeoutError:
                await member.kick(reason="Run out of time")
            finally:
                for msg in dialog:
                    await msg.delete()

        return True

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'\n\nLogged in as: {self.bot.user.name} - {self.bot.user.id}\nVersion: {discord.__version__}\n')
        game = discord.Game(name="zhopochlenning", type=1)
        await self.bot.change_presence(status=discord.Status.online, activity=game)
        print(f'Successfully logged in and booted...!')


def setup(bot):
    bot.add_cog(MembersCog(bot))
