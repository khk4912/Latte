import logging
import sys

import discord
from discord.ext import commands

# import for type hint :
from bot import LatteBot


class Utils(commands.Cog):
    bot: LatteBot = None

    def __init__(self, bot: LatteBot):
        self.bot: LatteBot = bot

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        # logger.info('[legacy_cogs] [utils] Utils 모듈이 준비되었습니다.')
        pass

    # Commands
    @commands.command(name='핑',
                      description='봇의 응답 지연시간을 보여줍니다. 핑퐁!')
    async def ping(self, ctx: commands.Context):
        await ctx.send(f'Pong! ({round(self.bot.latency * 1000)}ms)')

    @commands.command(name='정보',
                      description='호출한 유저의 정보를 보여줍니다. [WIP]')
    async def get_user_info(self, ctx: commands.Context, member: discord.Member):
        # Create an Embed which contains member's information
        info_embed: discord.Embed = discord.Embed(
            colour=discord.Colour.blue(),
            author=f'{self.bot.user.name}',
            title=f'{member.display_name}',
            description=f'{member.display_name} 님의 프로필 정보입니다!',
            type='rich')
        info_embed.set_thumbnail(url=member.avatar_url)
        info_embed.set_footer(text=f'{ctx.author.name} 님이 요청하셨습니다!', icon_url=ctx.author.avatar_url)

        info_embed.add_field(name='이름', value=f'{member.name}#{member.discriminator}', inline=False)
        status_dict: dict = {discord.Status.online: '온라인',
                             discord.Status.offline: '오프라인',
                             discord.Status.idle: "자리비움",
                             discord.Status.do_not_disturb: "방해금지"}
        info_embed.add_field(name='유저 상태', value=status_dict[member.status], inline=True)

        info_embed.add_field(name='Discord 가입 년도', value=member.created_at, inline=False)
        info_embed.add_field(name='서버 참여 날짜', value=member.joined_at, inline=True)

        is_nitro: bool = bool(member.premium_since)
        info_embed.add_field(name='프리미엄(니트로) 여부', value=str(is_nitro), inline=False)
        if is_nitro:
            info_embed.add_field(name='프리미엄 사용 시작 날짜', value=member.premium_since, inline=True)
        """
        info_embed.add_field(name='Hypesquad 여부', value=user_profile.hypesquad, inline=False)
        if user_profile.hypesquad:
            info_embed.add_field(name='소속된 Hypesquad house', value=user_profile.hypesquad_houses, inline=True)
        
        info_embed.add_field(name='메일 인증 사용여부', value=member.verified, inline=False)
        info_embed.add_field(name='2단계 인증 사용여부', value=member.mfa_enabled, inline=True)
        """
        info_embed.add_field(name='모바일 여부', value=member.is_on_mobile(), inline=False)

        await ctx.send(embed=info_embed)

    @commands.command(name='활동정보',
                      description='호출한 유저의 현재 활동정보를 보여줍니다.')
    async def get_user_activity(self, ctx: commands.Context, member: discord.Member):
        # Create an Embed which contains member's information
        ac_embed: discord.Embed = discord.Embed(
            title=f'{member.display_name}',
            description=f'{member.display_name} 님의 활동 정보입니다!',
            colour=self.bot.latte_color,
            author=f'{self.bot.user.name}',
            type='rich'
        )
        ac_embed.set_thumbnail(url=member.avatar_url)
        ac_embed.set_footer(text=f'{ctx.author.name} 님이 요청하셨습니다!', icon_url=ctx.author.avatar_url)

        if len(member.activities) == 0:
            ac_embed.add_field(name=f'활동 정보가 없습니다!', value='현재 진행중인 활동이 없습니다.', inline=False)
            return await ctx.send(embed=ac_embed)
        else:
            count: int = 1
            for ac in member.activities:
                ac_embed.add_field(name='\u200b', value='\u200b', inline=False)  # 공백 개행을 만든다.
                print(f'ac{count} = {type(ac)}')
                print(f'ac{count}.type = {ac.type}')
                try:
                    if ac.type == discord.ActivityType.playing:
                        ac_embed.add_field(name=f'활동 {count} 이름', value=ac.name, inline=False)
                        ac_embed.add_field(name=f'활동 {count} 유형', value='플레이 중', inline=False)
                        if ac.large_image_url is not None:
                            ac_embed.add_field(name='활동 이미지', value='\u200b', inline=False)
                            ac_embed.set_image(url=ac.large_image_url)
                    elif ac.type == discord.ActivityType.streaming:
                        ac_embed.add_field(name=f'활동 {count} 이름', value=ac.name, inline=False)
                        ac_embed.add_field(name=f'활동 {count} 유형', value='방송 중', inline=False)
                        if type(ac) == discord.Streaming:
                            ac_embed.add_field(name=f'**방송 정보**', value='\u200b', inline=False)
                            ac_embed.add_field(name=f'방송 플랫폼', value=ac.platform, inline=False)
                            if ac.twitch_name is not None:
                                ac_embed.add_field(name=f'트위치 이름', value=ac.twitch_name, inline=True)
                            ac_embed.add_field(name='방송 주소', value=ac.url, inline=False)
                            if ac.game is not None:
                                ac_embed.add_field(name='방송중인 게임', value=ac.game, inline=False)

                    elif ac.type == discord.ActivityType.listening:
                        ac_embed.add_field(name=f'활동 {count} 이름', value=ac.name, inline=False)
                        ac_embed.add_field(name=f'활동 {count} 유형', value='플레이 중', inline=False)

                        ac_embed.add_field(name=f'\u200b', value='WIP', inline=False)

                    elif ac.type == discord.ActivityType.watching:
                        ac_embed.add_field(name=f'활동 {count} 이름', value=ac.name, inline=False)
                        ac_embed.add_field(name=f'활동 {count} 유형', value='시청 중', inline=False)

                        ac_embed.add_field(name=f'\u200b', value='WIP', inline=False)

                    elif ac.type == discord.ActivityType.custom:
                        ac_extra = ''
                        if ac.emoji is not None:
                            ac_extra += ac.emoji.name
                        ac_embed.add_field(name=f'활동 {count} 이름', value=ac_extra+ac.name, inline=False)
                        ac_embed.add_field(name=f'활동 {count} 유형', value='사용자 지정 활동', inline=False)

                    elif ac.type == discord.ActivityType.unknown:
                        ac_embed.add_field(name=f'활동 {count} 이름', value='알 수 없는 활동입니다!', inline=False)
                    else:
                        ac_embed.add_field(name=f'요청하신 사용자의 활동을 파악하지 못했습니다!', value='유효한 활동 유형이 아닙니다 :(', inline=False)
                except Exception as e:
                    ac_embed.add_field(name=f'오류 발생!', value='활동 정보를 불러오지 못했습니다 :(', inline=False)
                    ac_embed.add_field(name=f'오류 내용', value=str(e.with_traceback(e.__traceback__)), inline=False)

                count += 1

        await ctx.send(embed=ac_embed)

    @commands.command(name='서버정보',
                      description='명령어가 사용된 서버의 정보를 보여줍니다.')
    async def get_server_info(self, ctx: commands.Context):
        guild: discord.Guild = ctx.guild
        # Create an Embed which contains member's information
        info_embed: discord.Embed = discord.Embed(
            colour=discord.Colour.blue(),
            author=f'{self.bot.user.name}',
            title=f'{guild.name}',
            description=f'{guild.name} 서버 정보입니다!',
            type='rich')
        info_embed.set_thumbnail(url=guild.icon_url)
        info_embed.add_field(name='서버 주인', value=guild.owner.mention, inline=False)
        info_embed.add_field(name='서버 생성 날짜', value=guild.created_at, inline=True)

        await ctx.send(embed=info_embed)

    @commands.command(name='알람설정',
                      description='새로운 알람을 설정합니다. [WIP]')
    async def setalarm(self, ctx: discord.ext.commands.Context, h: str = '0', m: str = '0', s: str = '0'):
        author: discord.Member = ctx.author
        hour = int(h)
        min = int(m)
        sec = int(s)
        # logger.debug(f'time = {hour} {min} {sec}')
        await ctx.send(f'{hour}시간 {min}분 {sec}초 주기로 알람을 설정했습니다.')
        self.bot.do_waitforsec = True
        import asyncio
        totalsec = hour * 3600 + min * 60 + sec
        while self.bot.do_waitforsec:
            # logger.debug(f'[알람] wating sec : {totalsec}')
            for currentmin in range(0, hour * 60 + min):
                # logger.info(f'[알람] {currentmin}분 지났습니다.')
                lefttime = (hour * 60 + min) - currentmin
                # logger.debug(f'lefttime = {lefttime}')
                await self.bot.change_presence(status=discord.Status.online,
                                               activity=discord.Game(name=f'알람까지 {lefttime}분 남았습니다', type=1))
                await asyncio.sleep(60)

            await asyncio.sleep(sec)
            # logger.info(f'[알람] 시간이 다 되었습니다!')
            await ctx.send(f'{author.mention} 시간이 다 되었습니다!')
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=discord.Game(name='아직 작업중!', type=1))

    @commands.command(name='알람끄기',
                      description='현재 실행중인 모든 알람을 종료합니다. [WIP]')
    async def stopalarm(self, ctx: discord.ext.commands.Context):
        self.bot.do_waitforsec = False
        await ctx.send('알람을 종료했습니다!')

    @commands.command(name='초대링크',
                      description='봇을 서버에 초대할 수 있는 링크를 생성합니다.')
    async def get_invite_url(self, ctx: commands.Context):
        """
        봇 초대링크를 생성, 전송합니다.
        """
        bot_invite_url: str = discord.utils.oauth_url(client_id=str(self.bot.user.id))
        print(f'[test] [get_bot_invite_oauth] type(bot_invite_url) : {type(bot_invite_url)}')
        print(f'[test] [get_bot_invite_oauth] bot_invite_url : {bot_invite_url}')
        await ctx.send(f'> 초대 링크입니다! -> {bot_invite_url}')

    @commands.command(name='박제',
                      description='메세지 url을 받아 해당 메세지를 박제합니다.')
    async def capture_bad(self, ctx: commands.Context, msg_link: str):
        if 'https://discordapp.com/channels/' not in msg_link:
            return await ctx.send(
                '올바르지 않은 링크입니다! 박제하려는 메세지의 링크를 전달해 주세요!\n> 방법 : 박제하려는 메세지에 **우클릭** -> **메세지 링크 복사** 클릭')
        else:
            # https://discordapp.com/channels/server_id/channel_id/message_id -> server_id/channel_id/message_id
            # -> ['server_id/channel_id/message_id']
            msg_data: list = msg_link.replace('https://discordapp.com/channels/', '').split('/')
            captured_guild: discord.Guild = ctx.guild
            captured_ch: discord.abc.GuildChannel = captured_guild.get_channel(channel_id=int(msg_data[1]))
            captured_msg: discord.Message = await captured_ch.fetch_message(msg_data[2])

            captured_embed: discord.Embed = discord.Embed(
                title='메세지 박제됨 : ',
                description=captured_msg.content,
                # 루미너스 브론드        [R236/G202/B179]
                color=self.bot.latte_color
            )
            captured_embed.set_author(name=captured_msg.author.name, icon_url=captured_msg.author.avatar_url)
            captured_embed.add_field(name='바로가기!', value=f'[원본 메세지]({msg_link} "박제된 메세지로 가는 포탈이 생성되었습니다 - 삐릿")')

            await ctx.send(embed=captured_embed)


def setup(bot):
    # logger.info('[legacy_cogs] [utils] Utils 모듈을 준비합니다.')
    bot.add_cog(Utils(bot))
