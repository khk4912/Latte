import logging
import sys

import discord
from discord.ext import commands

# import for type hint :
from bot import LatteBot


class Minecraft(commands.Cog):
    bot: LatteBot = None

    def __init__(self, bot: LatteBot):
        self.bot: LatteBot = bot

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        # logger.info('[legacy_cogs] [minecraft] Minecraft 모듈이 준비되었습니다.')
        pass

    # Commands
    @commands.group(name='마크',
                    description='마인크래프트 관련 기능입니다.')
    async def minecraft(self, ctx: commands.Context):
        """
        마인크래프트 관련 기능을 제공하는 모듈입니다.
        서버별 콘피그의 "minecraft" 영역을 사용합니다.

        "minecraft": {
            "type": "modded",          # 바닐라 서버인지, 모드서버인지, 플러그인 서버인지
            "map_type": "",            # 서바이벌인지, 크리에이티브인지, 하드코어인지
            "mc_role": "플레이어",      # 마인크래프트 역할 이름
        }
        """
        if ctx.command != '마크':
            pass
        await ctx.send(f'마크 관련 기능들입니다!')

    @minecraft.command(name='서버설정',
                       description='현재 서버를 마인크래프트 서버로 설정합니다.')
    async def set_minecraft_server(self):
        """
        명령어가 사용된 길드를 마인크래프트 서버로 설정하고 필요한 설정들을 초기화합니다.
        """
        pass

    @minecraft.group(name='패치노트',
                     description='패치노트 관련 명령어 그룹입니다.')
    async def patchnote(self):
        """
        패치노트 관련 기능입니다.
        """
        pass

    @patchnote.group(name='업로드',
                     description='신규 패치노트를 업로드합니다.')
    async def upload(self):
        """
        신규 패치노트를 업로드합니다.
        """
        pass

    @patchnote.group(name='서버정보',
                     description='마크 서버의 정보를 입력합니다.')
    async def set_serverinfo(self):
        """
        패치노트 관련 기능입니다.
        """
        pass


def setup(bot):
    # logger.info('[legacy_cogs] [minecraft] Minecraft 모듈을 준비합니다.')
    bot.add_cog(Minecraft(bot))
