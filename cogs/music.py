import logging
import sys

import discord
from discord.ext import commands

# import for type hint :
from bot import LatteBot

class Music(commands.Cog):
    bot: LatteBot = None

    def __init__(self, bot: LatteBot):
        self.bot: LatteBot = bot

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        # logger.info('[legacy_cogs] [minecraft] Minecraft 모듈이 준비되었습니다.')
        pass

    # Commands
    @commands.group(name='음악',
                    description='음악 관련 기능들입니다.')
    async def music(self, ctx: commands.Context):
        """
        음악 관련 기능을 제공하는 모듈입니다.
        음악 스트리밍 중심으로 디스코드의 음성 채팅방에서 음악 감상을 즐길 수 있도록 하는 기능들을 모아두었습니다.

        "minecraft": {
            "type": "modded",          # 바닐라 서버인지, 모드서버인지, 플러그인 서버인지
            "map_type": "",            # 서바이벌인지, 크리에이티브인지, 하드코어인지
            "mc_role": "플레이어",      # 마인크래프트 역할 이름
        }
        """
        if ctx.command != '마크':
            pass
        await ctx.send(f'마크 관련 기능들입니다!')

    @music.command(name='추가',
                       description='재생목록에 음악을 추가합니다.')
    async def set_minecraft_server(self):
        """
        음악 재생목록에 음악을 추가합니다.
        """
        pass


def setup(bot):
    # logger.info('[legacy_cogs] [minecraft] Minecraft 모듈을 준비합니다.')
    bot.add_cog(Music(bot))