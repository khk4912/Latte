import logging
import sys

import discord
from discord.ext import commands

# import for type hint :
from discord.utils import get, find

from bot import LatteBot


class Management(commands.Cog):
    bot: LatteBot = None

    def __init__(self, bot: LatteBot):
        self.bot: LatteBot = bot

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        # logger.info('[cogs] [management] Management 모듈이 준비되었습니다.')
        pass

    '''
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """
        on_raw_reaction_add(payload):
            ...

        봇에 캐싱되지 않은 메세지에 반응이 추가되었을 때 실행되는 이벤트입니다.
        paylod는 discord.RawReactionActionEvent class로, 자세한 설명은

        on_raw_reaction_add() 이벤트 설명 : https://discordpy.readthedocs.io/en/latest/api.html#event-reference
        payload 설명 : https://discordpy.readthedocs.io/en/latest/api.html#discord.RawReactionActionEvent

        에서 확인하실 수 있습니다.
        """
        # payload에서 필요한 정보를 저장한다.
        msg_id: int = payload.message_id  # 반응 추가 이벤트가 발생한 메세지 id
        guild_id: int = payload.guild_id  # 반응 추가 이벤트가 발생한 길드 id
        user_id: int = payload.user_id  # 반응 추가 이벤트를 발생시킨 유저 id
        member = payload.member  # 반응 추가 이벤트를 발생시킨 사용자. REACTION_ADD 유형의 이벤트에서만 사용 가능하다.

        guild: discord.Guild = find(lambda g: g.id == guild_id, self.bot.guilds)  # 반응 추가 이벤트가 발생한 길드
        # logger.debug(f'[legacy_cogs] [management] (on_raw_reaction_add) guild.name = {guild.name}')
        server_config = self.bot.server_config_dict[guild.name]

        # autorole 용 변수들
        # 서버별로 roles_dict 내부 카테고리가 다를것을 상정하고, 루프를 돌며 이모지 명칭을 찾는다.
        emoji: discord.PartialEmoji = payload.emoji

        # Message IDs
        # autorole msg id of guild which occured this event
        role_setting_msg_ids: list = server_config['role_setting_msg_ids']
        # auth msg id of guild which occured this event
        auth_msg_id: int = server_config['auth']['auth_msg_id']

        if msg_id in role_setting_msg_ids:
            await self.check_autorole(server_config=server_config, member=member, guild=guild, emoji=emoji)

        elif msg_id == auth_msg_id:
            await self.check_auth(server_config=server_config, guild=guild, member=member, emoji=emoji)

        else:
            # logger.info(f'[legacy_cogs] [management] (on_raw_reaction_add) {user_id} 님이 {guild_id} 서버의 {msg_id} 메세지에서 {emoji} 반응을 추가했습니다.')
            pass

    async def check_autorole(self, server_config: dict, member: discord.Member, guild: discord.Guild, emoji: discord.PartialEmoji):
        """
        자동역할 기능 부분
        """
        # logger.info(f'[legacy_cogs] [management] (on_raw_reaction_add) <autorole> {user_id} 님이 역할을 신청했습니다.')

        selected_emoji_category: str = ''  # roles_dict의 카테고리 분류 저장

        roles_dict = server_config['roles_dict']
        for category in roles_dict.keys():
            for role_emoji_name in roles_dict[category].keys():
                if role_emoji_name == emoji.name:
                    selected_emoji_category = category
                    break
        # logger.debug(f'[legacy_cogs] [management] (on_raw_reaction_add) <autorole> selected_emoji_category = {selected_emoji_category}')

        role_name = server_config['roles_dict'][selected_emoji_category][emoji.name]
        # logger.debug(f'[legacy_cogs] [management] (on_raw_reaction_add) <autorole> {user_id} 님이 신청한 역할 : {role_name}')
        role = get(guild.roles, name=role_name)

        if role is not None:
            if member is not None:
                await member.add_roles(role, reason='Auto role assignment using bot.', atomic=True)
            else:
                # logger.error('[legacy_cogs] [management] (on_raw_reaction_add) <autorole> member not found')
                pass
        else:
            # logger.error('[legacy_cogs] [management] (on_raw_reaction_add) <autorole> role not found')
            pass

    async def check_auth(self, server_config: dict, guild: discord.Guild, member: discord.Member, emoji: discord.PartialEmoji):
        """
        사용자 인증 부분
        """
        # logger.info(f'[legacy_cogs] [management] (on_raw_reaction_add) <auth> {user_id} 님이 인증 절차를 거쳤습니다.')
        # logger.debug(f'[legacy_cogs] [management] (on_raw_reaction_add) <auth> 사용된 이모지 : {emoji}, emoji.name = {emoji.name}')
        if emoji.name == '✅':

            noauth_role_name: str = server_config['auth']['noauth_role_name']
            auth_role_name: str = server_config['auth']['auth_role_name']
            # logger.info(f'[legacy_cogs] [management] (on_raw_reaction_add) <auth> {member.display_name}님이 ✅ 반응을 제거해 인증을 취소했습니다.')

            noauth_role = get(guild.roles, name=noauth_role_name)
            # logger.debug(f'[legacy_cogs] [management] (on_raw_reaction_add) <auth> noauth_role = {noauth_role}')
            await member.remove_roles(noauth_role)
            auth_role = get(guild.roles, name=auth_role_name)
            # logger.debug(f'[legacy_cogs] [management] (on_raw_reaction_add) <auth> auth_role = {auth_role}')
            await member.add_roles(auth_role)
        else:
            # logger.info(f'[legacy_cogs] [management] (on_raw_reaction_add) {user_id} 님이 {guild_id} 서버의 {msg_id} 메세지에서 {emoji} 반응을 추가했습니다.')
            pass
    '''

    # Commands
    @commands.group(name='관리',
                    description='서버 관리 기능을 제공하는 명령어 그룹입니다.')
    async def manage(self, ctx: commands.Context):
        """
        서버 관리 기능을 제공하는 명령어 그룹입니다.
        """
        # logger.info(f'[legacy_cogs] [management] {ctx.author} 유저가 {ctx.command} 명령어를 사용했습니다!')
        if ctx.invoked_subcommand is None:
            await ctx.send('현재 다음과 같은 명령어들이 있어요!\n\n' +
                           '**자동역할** : 관리자 전용 명령어로, 명령어를 사용한 채널에 자동역할 메세지를 생성하고 해당 메세지에 반응을 추가하고 제거하는 방식으로 역할 부여를 자동화합니다.\n' +
                           '**설정보기** : 관리자 전용 명령어로, 명령어를 사용한 서버의 불러와진 설정(json)을 코드 하이라이팅을 입혀 채팅으로 보여줍니다.')
        else:
            pass
        
    @commands.has_guild_permissions(administrator=True)
    @manage.command(name='추방',
                    description='멘션한 유저를 추방합니다.')
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason: str = None):
        await member.kick(reason=reason)
        kick_embed = discord.Embed(title="**킥**", description=f"*{member.mention} 님이 킥 처리되었습니다.*")
        kick_embed.add_field(name="**사유**", value=f"*{reason}*", inline=False)

        log_ch_id: int = self.bot.guild_configs[ctx.guild.name]['module_settings']['management']['ch_ids']['log']
        if log_ch_id != 0:
            await self.bot.get_channel(log_ch_id).send(embed=kick_embed)

    @commands.has_guild_permissions(administrator=True)
    @manage.command(name='차단',
                    description='멘션한 유저를 차단합니다.')
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason: str = None):
        await member.ban(reason=reason)
        ban_embed = discord.Embed(title="**밴**", description=f"*{member.mention} 님이 밴 처리되었습니다.*")
        ban_embed.add_field(name="**사유**", value=f"*{reason}*", inline=False)

        log_ch_id: int = self.bot.guild_configs[ctx.guild.name]['module_settings']['management']['ch_ids']['log']
        if log_ch_id != 0:
            await self.bot.get_channel(log_ch_id).send(embed=ban_embed)

    @commands.has_guild_permissions(administrator=True)
    @manage.command(name='차단해제',
                    description='멘션한 유저의 차단을 해제합니다.')
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason: str = None):
        await member.unban(reason=reason)
        unban_embed = discord.Embed(title="**언밴**", description=f"*{member.mention} 님이 밴 해제 처리되었습니다.*")
        unban_embed.add_field(name="**사유**", value=f"*{reason}*", inline=False)

        log_ch_id: int = self.bot.guild_configs[ctx.guild.name]['module_settings']['management']['ch_ids']['log']
        if log_ch_id != 0:
            await self.bot.get_channel(log_ch_id).send(embed=unban_embed)

    # @commands.has_guild_permissions(administrator=True)
    @commands.has_guild_permissions(manage_messages=True)
    @manage.command(name='채팅청소',
                    description='주어진 개수만큼 해당 채널에서 메세지를 삭제합니다.')
    async def cleaner(self, ctx: commands.Context, amount: int = 5):
        if amount < 1:
            await ctx.send(f'{amount} 는 너무 적습니다!')
            return

        del_msgs: list = await ctx.channel.purge(limit=amount)
        count: int = len(del_msgs)
        purge_embed = discord.Embed(title="채팅 청소기 MK.1 🌀", description=f"채팅창을 청소했습니다. {count}개의 메세지를 삭제했습니다.")
        await ctx.send(embed=purge_embed)

        log_ch_id: int = self.bot.guild_configs[ctx.guild.name]['module_settings']['management']['ch_ids']['log']
        if log_ch_id != 0:
            await self.bot.get_channel(log_ch_id).send(embed=purge_embed)

    @commands.has_guild_permissions(administrator=True)
    @manage.command(name='투표',
                    description='투표를 생성합니다. 사용 양식은 아래와 같습니다 :\n'
                                f'__{bot.command_prefix}관리 투표 제목, 설명, 항목1, 항목2, 항목3, ... , 항목9\n__'
                                '제목은 반드시 입력하셔야 하며, 선택지는 두개 이상 9개 이하로 입력하셔야 합니다.')
    async def create_vote(self, ctx: commands.Context, *, vote_content: str):
        num_unicode_emoji: list = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣']  # 1~9
        # Process vote_content to title(str), choices(list[str])
        vote_datas: list = vote_content.split(',')
        title: str = vote_datas.pop(0)  # First content from vote_content must be the title
        desc: str = vote_datas.pop(0)   # Second content(which now moved to first) must be the description.
        # logger.info(f'title = {title}')
        # logger.info(f'vote_datas = {vote_datas}')
        choices = vote_datas
        del vote_datas

        choices_count: int = len(choices)

        # Check if the command is used properly
        # If vote has only one choice or no choice:
        if 2 > choices_count or choices_count > 9:
            await ctx.send(f'투표는 2개 이상 9개 이하의 선택지로 구성되어야 합니다!')
            return
        # If vote does not have a title:
        if title == '':
            await ctx.send(f'투표 제목 없이는 투표를 진행할 수 없습니다.')
            return

        # Create an Embed which contains informations of this vote:
        vote_embed = discord.Embed(title=f"[투표] {title}", description=desc, color=self.bot.latte_color)

        # Loops for add choices field in vote_embed:
        for num in range(choices_count):
            vote_embed.add_field(name=num_unicode_emoji[num], value=choices[num], inline=True)

        vote_embed.add_field(name='게시 일자', value=ctx.message.created_at, inline=False)
        vote_embed.add_field(name='주의사항', value='현재 봇은 투표 결과를 자동으로 집계해주진 않습니다.\n'
                                                '각 문항별 득표수는 해당 문항의 반응 개수 - 1(봇이 남긴 반응)입니다.', inline=False)

        vote_msg: discord.Message = await ctx.send(embed=vote_embed)

        # Loops for add number reaction in vote_msg:
        for num in range(choices_count):
            await vote_msg.add_reaction(num_unicode_emoji[num])


def setup(bot: LatteBot):
    # logger.info('[cogs] [management] Management 모듈을 준비합니다.')
    bot.add_cog(Management(bot))
