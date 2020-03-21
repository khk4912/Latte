import logging
import sys

import discord
from discord.ext import commands

# import for type hint :
from bot import LatteBot


class Test(commands.Cog):
    bot: LatteBot = None

    def __init__(self, bot: LatteBot):
        self.bot: LatteBot = bot

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        # logger.info('[legacy_cogs] [minecraft] Minecraft 모듈이 준비되었습니다.')
        pass

    # Commands
    @commands.group(name='실험',
                    description='실험용 명령어들입니다.')
    async def test(self, ctx: commands.Context):
        """
        실험용 기능 모음집.
        """
        print('')
        await ctx.send('실험용 명령어입니다.')
        pass

    @test.command(name='문자열입력실험1',
                  description='get several strings which are separated with blank(space) as a single string')
    async def str_test1(self, ctx: commands.Context, *, message: str):
        """
        test feature - get multiple strings as a single string.
        by setting the function's parameter 'message' to be the last variable, it will take all strings and store them.
        """
        await ctx.send(f'[str_test1] : {message}')

    @test.command(name='문자열입력실험2',
                  description='get several strings which are separated with blank(space) as a single string(test)')
    async def str_test2(self, ctx: commands.Context, message: str):
        """
        test feature - get multiple strings as a single string.
        """
        await ctx.send(f'[str_test2] : {message}')

    @test.command(name='공지하기',
                  description='get announcement which is consisted of multiple strings and send it to the announce channel.')
    async def announcement_test(self, ctx: commands.Context):
        """
        test feature - get announcement which is consisted of multiple strings and send it to the announce channel.
        """
        await ctx.send('공지사항을 입력해 주세요!')

        def check_announcement_msg(msg):
            return msg is not None and msg.content != ''

        msg: discord.Message = await self.bot.wait_for(event='message', check=check_announcement_msg)
        await msg.delete(delay=3)
        await ctx.send(f'[announcement_test] : 아래의 공지사항을 전달했습니다!\n> {msg.content}')



    @test.group(name='API',
                description='use Client.fetch_something() to call Discord API and retrieves discord objects. ')
    async def API(self, ctx: commands.Context):
        """
        실험용 기능 - fetch_something 모음집(Discord API Calls).
        """
        await ctx.send('Discord API를 호출하는 실험용 명령어입니다.')
        pass

    @API.command(name='user',
                 description='use Client.fetch_user() to call Discord API and retrieves discord.User ')
    async def get_user(self, ctx: commands.Context, member: discord.Member):
        user_from_api = await self.bot.fetch_user(user_id=member.id)
        print(f'[test] [get_user_apicall] user_from_api : {user_from_api}')
        print(f'[test] [get_user_apicall] type(user_from_api) : {type(user_from_api)}')

    @API.command(name='user_profile',
                 description='use Client.fetch_user_profile() to call Discord API and retrieves discord.Profile ')
    async def get_user_profile(self, ctx: commands.Context, member: discord.Member):
        try:
            userprofile_from_api: discord.Profile = await self.bot.fetch_user_profile(user_id=member.id)
            print(f'[test] [get_user_apicall] type(user_from_api) : {type(userprofile_from_api)}')
            print(f'[test] [get_user_apicall] user_from_api : {userprofile_from_api}')
            user_embed: discord.Embed = discord.Embed(
                title='API로 얻어온 유저 정보입니다.',
                description=f'{userprofile_from_api}',
                color=self.bot.latte_color
            )
            user_embed.add_field(name='Hypesquad', value=userprofile_from_api.hypesquad)
            user_embed.add_field(name='Hypesquad Houses', value=userprofile_from_api.hypesquad_houses)
            user_embed.add_field(name='Premium', value=str(userprofile_from_api.premium))
            user_embed.add_field(name='Early Supporter', value=userprofile_from_api.early_supporter)
            await ctx.send(embed=user_embed)
        except Exception as e:
            error_embed: discord.Embed = discord.Embed(
                title='오류 발생!',
                description=f'{e.with_traceback(e.__traceback__)}',
                color=discord.Colour.red()
            )
            await ctx.send(embed=error_embed)




def setup(bot):
    # logger.info('[legacy_cogs] [minecraft] Minecraft 모듈을 준비합니다.')
    bot.add_cog(Test(bot))
