import logging
import sys

import discord
from discord.ext import commands

# import for type hint :
from bot import LatteBot


class Developer(commands.Cog):
    bot: LatteBot = None

    def __init__(self, bot: LatteBot):
        self.bot: LatteBot = bot

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        # logger.info('[legacy_cogs] [developer] Developer 모듈이 준비되었습니다.')
        pass

    # Commands
    @commands.group(name='개발자',
                    description='개발자 기능들입니다.')
    async def dev(self, ctx: commands.Context):
        """
        개발자 전용 명령어들입니다.
        """
        if ctx.invoked_subcommand is None:
            dev_embed: discord.Embed = discord.Embed(
                title='라테봇 개발자 정보',
                description='라테봇을 개발하는 사람들의 정보입니다.',
                color=self.bot.latte_color
            )
            dev_embed.set_footer(text=f'{ctx.author.name} 님이 요청하셨습니다!', icon_url=ctx.author.avatar_url)
            dev_embed.set_thumbnail(url=self.bot.user.avatar_url)

            dev_users: str = ''
            for dev_id in self.bot.dev_ids:
                dev_user: discord.User = discord.utils.find(lambda u: u.id == dev_id, self.bot.users)
                dev_users += f'{dev_user.name}#{dev_user.discriminator}\n'
            dev_embed.add_field(name='개발자', value=dev_users)
            
            dev_embed.add_field(name='라테봇 공식 커뮤니티', value=f'[바로가기]({self.bot.official_community_invite} "공식 커뮤니티로 가는 포탈이 생성되었습니다 - 삐릿")')

            await ctx.send(embed=dev_embed)
        else:
            if ctx.author.id in self.bot.dev_ids:
                await self.bot.process_commands(ctx.message)

    @dev.command(name='종료',
                 description='봇을 종료합니다. [WIP]')
    async def stop(self, ctx: commands.Context):
        """
        봇을 종료합니다.
        """
        await ctx.send('봇을 종료합니다!')
        self.bot.do_reboot = False
        await self.bot.close()
        pass


def setup(bot):
    # logger.info('[legacy_cogs] [developer] Developer 모듈을 준비합니다.')
    bot.add_cog(Developer(bot))