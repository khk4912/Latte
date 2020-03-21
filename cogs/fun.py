import logging
import sys

import discord
from discord.ext import commands
from discord.utils import find

import random

# import for type hint :
from bot import LatteBot


class Fun(commands.Cog):
    bot: LatteBot = None

    def __init__(self, bot: LatteBot):
        self.bot: LatteBot = bot

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        # logger.info('[cogs] [fun] Fun 모듈이 준비되었습니다.')
        pass

    # Commands
    @commands.group(name='즐길거리',
                    description='재밌는 명령어들 총집합!')
    async def fun(self, ctx: commands.Context):
        """
        재미삼아 만들어본 기능들!
        """
        pass

    @fun.command(name='아무말',
                 description='아무말이나 말하는 라테봇을 볼 수 있어요!')
    async def random_text(self, ctx: commands.Context):
        try:
            with open(file='./resources/fun/random_texts.txt', mode='rt', encoding='utf-8') as rand_txt_file:
                rand_txts: list = rand_txt_file.readlines()
                choice_txt: str = random.choice(rand_txts)
                await ctx.send(choice_txt)
        except Exception as e:
            error_embed: discord.Embed = discord.Embed(
                title='오류 발생!',
                description=f'{e.with_traceback(e.__traceback__)}'
                            f'\n명령어 실행 도중 문제가 발생했습니다! 라테봇 공식 커뮤니티에서 오류 제보를 해주시면 감사하겠습니다!'
                            f'\n[공식 커뮤니티 바로가기]({self.bot.official_community_invite})',
                color=discord.Colour.red()
            )
            error_embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
            error_embed.set_footer(text=f'{ctx.author.name} 님께서 요청하셨습니다!', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=error_embed)

    @fun.command(name='주사위',
                 description='6면짜리 주사위를 던져요!')
    async def roll_the_dice(self, ctx: commands.Context):
        result = random.randint(1, 6)
        result_embed: discord.Embed = discord.Embed(
            title='🎲 주사위를 던졌어요!',
            description=f'결과 : {result}',
            color=self.bot.latte_color
        )
        result_embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
        result_embed.set_footer(text=f'{ctx.author.name} 님께서 요청하셨습니다!', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=result_embed)

    @fun.command(name='음악추천',
                 description='음악을 추천합니다!')
    async def suggest_random_song(self, ctx: commands.Context):
        """
        suggest random song from local file(./resources/fun/suggested_songs.txt).
        :param ctx: discord.ext.commands.Context type variable. stores several information of command's context.
        :return: None
        """
        try:
            with open(file='./resources/fun/suggested_songs.txt', mode='rt', encoding='utf-8') as songs_file:
                songs_datas: list = songs_file.readlines()
                choice_song_data: str = random.choice(songs_datas)
                """
                choice_song structure:
                user-id(user who suggested the song)|song-url|title|(artists)
                """
                choice_song_info: list = choice_song_data.split('|')

                url_enc_type: str = ''
                if 'https:' in choice_song_info[1]:
                    url_enc_type = 'https:'
                elif 'http:' in choice_song_info[1]:
                    url_enc_type = 'http:'
                else:
                    return Exception('올바른 URL이 아닙니다!')

                song_embed: discord.Embed = discord.Embed(
                    title=f'**{choice_song_info[2]}**', # song title
                    description=f'[음악 바로가기]({choice_song_info[1]})',   # song url
                    color=self.bot.latte_color
                )

                if '//www.youtube.com/' in choice_song_info[1]:
                    # https://www.youtube.com/watch?v=oX8JkxEFrRw -> oX8JkxEFrRw,
                    # https://www.youtube.com/watch?v=jp-CVYGEsjg&list=PLiuyAiQgbis44AS8abPGUl7oL3zwQZTrr&index=13&t=0s
                    # -> watch?v=jp-CVYGEsjg&list=PLiuyAiQgbis44AS8abPGUl7oL3zwQZTrr&index=13&t=0s
                    # -> ['watch?v=jp-CVYGEsjg', 'list=PLiuyAiQgbis44AS8abPGUl7oL3zwQZTrr', 'index=13', 't=0s']
                    # -> 'watch?v=jp-CVYGEsjg' -> 'jp-CVYGEsjg'
                    # resource : https://webdir.tistory.com/472 , https://yeahvely.tistory.com/30

                    youtube_vid_id: str = str(choice_song_info[1]).replace(f'{url_enc_type}//www.youtube.com/', '').split('&')[0].replace('watch?v=', '')
                    song_embed.set_thumbnail(url=f'http://img.youtube.com/vi/{youtube_vid_id}/maxresdefault.jpg')

                elif '//youtu.be/' in choice_song_info[1]:
                    # https://youtu.be/nVCubhQ454c -> nVCubhQ454c,
                    # https://www.youtube.com/watch?v=jp-CVYGEsjg&list=PLiuyAiQgbis44AS8abPGUl7oL3zwQZTrr&index=13&t=0s
                    # -> watch?v=jp-CVYGEsjg&list=PLiuyAiQgbis44AS8abPGUl7oL3zwQZTrr&index=13&t=0s
                    # -> ['watch?v=jp-CVYGEsjg', 'list=PLiuyAiQgbis44AS8abPGUl7oL3zwQZTrr', 'index=13', 't=0s']
                    # -> 'watch?v=jp-CVYGEsjg' -> 'jp-CVYGEsjg'
                    # resource : https://webdir.tistory.com/472 , https://yeahvely.tistory.com/30

                    youtube_vid_id: str = str(choice_song_info[1]).replace(f'{url_enc_type}//youtu.be/', '').split('&')[0].replace('watch?v=', '')
                    song_embed.set_thumbnail(url=f'http://img.youtube.com/vi/{youtube_vid_id}/maxresdefault.jpg')

                else:
                    pass

                song_embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
                song_embed.set_footer(text=f'{ctx.author.name} 님께서 요청하셨습니다!', icon_url=ctx.author.avatar_url)

                suggested_user: discord.User = find(lambda u: u.id == int(choice_song_info[0]), self.bot.users)
                if suggested_user is None:
                    song_embed.add_field(name='이 음악을 추천한 사람', value='현재 이 봇이 확인할 수 없는 유저입니다...')
                else:
                    song_embed.add_field(name='이 음악을 추천한 사람', value=f'{suggested_user.name}#{suggested_user.discriminator}')

                await ctx.send(embed=song_embed)
        except Exception as e:
            error_embed: discord.Embed = discord.Embed(
                title='오류 발생!',
                description=f'{e.with_traceback(e.__traceback__)}'
                            f'\n명령어 실행 도중 문제가 발생했습니다! 라테봇 공식 커뮤니티에서 오류 제보를 해주시면 감사하겠습니다!'
                            f'\n[공식 커뮤니티 바로가기]({self.bot.official_community_invite})',
                color=discord.Colour.red()
            )
            error_embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
            error_embed.set_footer(text=f'{ctx.author.name} 님께서 요청하셨습니다!', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=error_embed)


def setup(bot):
    # logger.info('[cogs] [fun] Fun 모듈을 준비합니다.')
    bot.add_cog(Fun(bot))
