import logging
import os
import sys

import discord
from discord.ext import commands

import json

# 로깅 설정
logging.getLogger("discord.gateway").setLevel(logging.WARNING)
logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s: %(message)s")
)
logger.addHandler(handler)

# global variables
# bot infos
token: str = ""  # Discord Bot's token. load from config.txt in init(), save to config.txt in save_datas()
config_file_name = "test/test_config.txt"
# config_file_name = './config.txt'

"""
Bot Codes
"""


class LatteBot(commands.Bot):
    # Bot Management Variables
    do_reboot: bool = False
    dev_ids: list = [280855156608860160]
    official_community_invite: str = "https://discord.gg/ks5m5HE"

    # Bot Decorative Variables
    latte_color: discord.Colour = discord.Color.from_rgb(236, 202, 179)

    def __init__(self, *args, **kwargs):
        self.guild_configs: dict = {}
        self.dev_ids: list = [280855156608860160]
        self.do_reboot: bool = False
        self.official_community_invite: str = "https://discord.gg/ks5m5HE"
        super().__init__(*args, **kwargs)

    """
    [ Settings Management ]
    Using files and database, bot manages settings of many servers
    """

    def settings_init(self):
        global token
        """
        Loads setting files(config.txt, server_setting/*.json)
        """
        try:
            print(f"[init] > {config_file_name}를 불러옵니다.")
            bot_config_file = open(mode="rt", file=config_file_name, encoding="utf-8")
            # config.txt 파일 불러오기
            print("[init] > config.txt 를 성공적으로 불러왔습니다.")
            token = bot_config_file.read().replace("token=", "")
            if token == "":
                print("[init] > config.txt를 불러왔으나, token이 비어있네요 :(")
                token = input("[init] > discord application의 bot token을 입력해 주세요! : ")
            print(f"[init] > token = {token}")
            bot_config_file.close()
        except FileNotFoundError as e:
            print(f"[init] > {config_file_name} 가 존재하지 않습니다! 설정이 필요합니다.")
            print(f"[init] > Exception Type : {type(e)}")
            print(f"[init] > Exception Value : {e}")
            token = input("[init] > discord application의 bot token을 입력해 주세요! : ")
            # mode = x(create a new file as writing mode)t(text mode)
            bot_config_file = open(mode="xt", file=config_file_name, encoding="utf-8")
            bot_config_file.write(f"token={token}")
            bot_config_file.close()
        except Exception as e:
            print(f"[init] > 오류가 발생했습니다!")
            print(f"[init] > Exception Type : {type(e)}")
            print(f"[init] > Exception Value : {e}")

        # Load server_configs/{guild.name}_config.json
        files: list = os.listdir("./server_configs")
        server_config_files: list = []
        for server_config_file in files:
            if "_config.json" in server_config_file:
                server_config_files.append(server_config_file)
            else:
                continue

        for config_filedir in server_config_files:
            with open(
                file=f"server_configs/{config_filedir}", mode="rt", encoding="utf-8"
            ) as config_file:
                config: dict = json.load(fp=config_file)
                self.guild_configs[config["guild_name"]] = config

        # Load Cogs(Extensions)
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                extension = filename[0:-3]
                try:
                    print(f"filename[0:3] = {extension}")
                    bot.load_extension(f"cogs.{extension}")
                except Exception as e:
                    print(f"[init] > {e.with_traceback(e.__traceback__)}")
                    print(f"[init] > {extension} 모듈을 불러오는데 실패했습니다! 계속 진행합니다...")
                    continue

    def settings_save(self):
        """
        save settings datas to the file.
        """
        global token, bot

        # 봇 설정파일 저장
        print(f"[save_datas] > {config_file_name}를 저장합니다...")
        try:
            with open(
                file=config_file_name, mode="wt", encoding="utf-8"
            ) as bot_config_file:
                print(f"token={token}")
                bot_config_file.write(f"token={token}")
        except Exception as e:
            print("[save_datas] > 오류가 발생했습니다!")
            print(e.with_traceback(e.__traceback__))
            return "**config.txt** 파일을 저장하는데 실패했습니다!", e
        else:
            print(f"[save_datas] > {config_file_name}를 저장했습니다!")

        # 서버별 설정파일 저장
        for config in self.guild_configs:
            with open(
                file=f'./server_configs/{config["guild_name"]}_config.json',
                mode="wt",
                encoding="utf-8",
            ) as config_file:
                json.dump(obj=config, fp=config_file)

        # 만약 봇이 꺼지면서 실행된것이 아닌, 명령어로 실행된 경우라면 init() 함수를 사용해 설정을 다시 불러온다.
        if not bot.is_closed():
            print("[save_datas] > 새롭게 저장한 설정들을 봇의 전체 설정에 반영합니다.")
            self.settings_init()
            print("[save_datas] > 설정 불러오기에 성공했습니다!")

        return "설정 저장에 성공했습니다!", None

    def check_reboot(self):
        # if reboot mode on, run reboot code
        if self.is_closed() and self.do_reboot:
            print("[check_reboot] > 봇 재시작 명령이 들어와 봇을 재시작합니다!")
            excutable = sys.executable
            args = sys.argv[:]
            args.insert(0, excutable)
            os.execv(sys.executable, args)
        else:
            print("[check_reboot] > 봇 재시작 명령이 없으므로 봇을 종료합니다.")


desc = "카페라테를 좋아하는 개발자가 만든 디스코드 봇이에요!"
bot = LatteBot(
    command_prefix=["라떼야 ", "라떼봇 ", "라떼 ", "라테야 ", "라테봇 ", "라테 "], description=desc
)

"""
[ Cogs Management ]
Using discord.ext.commands.Cog, this bot manages several function per extension.
"""


@bot.group(name="모듈", invoke_without_command=True)
async def manage_module(ctx: commands.Context):
    if ctx.author.id in bot.dev_ids:
        if ctx.invoked_subcommand is None:
            msg = ">>> **현재 불러와진 모듈**"
            for module in bot.extensions:
                msg += f'\n \* {str(module).replace("cogs.", "")}'

            msg += "\n\n사용법: `모듈 (로드/언로드/리로드) [모듈이름]`"
            await ctx.send(msg)
        else:
            pass
    else:
        return await ctx.send("봇의 개발자가 아니므로 사용할 수 없습니다!")
        pass


@manage_module.command(name="로드")
async def cmd_cog_load(ctx: commands.Context, extension: str):
    if ctx.author.id not in bot.dev_ids:
        return await ctx.send("봇의 개발자가 아니므로 사용할 수 없습니다!")

    try:
        bot.load_extension(f"cogs.{extension}")
    except commands.errors.ExtensionNotFound:
        return await ctx.send("해당 모듈을 찾을 수 없습니다.")
    except commands.errors.ExtensionAlreadyLoaded:
        return await ctx.send("해당 모듈은 이미 불러와졌습니다.")
    except commands.errors.NoEntryPointError:
        return await ctx.send('해당 모듈에 setup() 함수가 없습니다."')
    except commands.errors.ExtensionFailed:
        return await ctx.send("해당 모듈의 setup() 실행에 실패했습니다.")
    except Exception as e:
        logger.exception(f"Error while load cog {extension}")
        return await ctx.send(
            "모듈에 문제가 발생했습니다!"
            + f"\n > Exception Type : {type(e)}"
            + f"\n > Exception Content : {e}"
        )
    else:
        return await ctx.send(f"> {extension} 모듈을 로드했습니다.")


@manage_module.command(name="언로드")
async def cmd_cog_unload(ctx: commands.Context, extension: str):
    if ctx.author.id not in bot.dev_ids:
        return await ctx.send("봇의 개발자가 아니므로 사용할 수 없습니다!")
    try:
        bot.unload_extension(f"cogs.{extension}")
    except commands.errors.ExtensionNotLoaded:
        return await ctx.send("해당 모듈이 로드되지 않았습니다.")
    except Exception as e:
        logger.exception(f"Error while load cog {extension}")
        return await ctx.send(
            "모듈에 문제가 발생했습니다!"
            + f"\n > Exception Type : {type(e)}"
            + f"\n > Exception Content : {e}"
        )
    else:
        return await ctx.send(f"> {extension} 모듈을 언로드했습니다.")


@manage_module.command(name="리로드")
async def cmd_cog_reload(ctx: commands.Context, extension: str):
    if ctx.author.id in bot.dev_ids:
        try:
            bot.reload_extension(f"cogs.{extension}")
        except commands.errors.ExtensionNotLoaded:
            return await ctx.send("해당 모듈이 로드되지 않았습니다.")
        except commands.errors.ExtensionNotFound:
            return await ctx.send("해당 모듈을 찾을 수 없습니다.")
        except commands.errors.NoEntryPointError:
            return await ctx.send("해당 모듈에 setup() 함수가 없습니다.")
        except commands.errors.ExtensionFailed:
            return await ctx.send("해당 모듈의 setup() 실행에 실패했습니다.")
        except Exception as e:
            logger.exception(f"Error while load cog {extension}")
            return await ctx.send(
                "모듈에 문제가 발생했습니다!"
                + f"\n > Exception Type : {type(e)}"
                + f"\n > Exception Content : {e}"
            )
        else:
            return await ctx.send(f"> {extension} 모듈을 리로드했습니다.")
    else:
        return await ctx.send("봇의 개발자가 아니므로 사용할 수 없습니다!")


"""
[ Discord.py Event Management ]

"""


@bot.event
async def on_ready():
    logger.info("봇 온라인!")
    logger.info(f"owner_id : {bot.owner_id}")
    logger.info(f"dev_ids : {bot.dev_ids}")
    # 봇이 플레이중인 게임을 설정할 수 있습니다.
    await bot.change_presence(
        status=discord.Status.online, activity=discord.Game(name="라떼는 달달합니다!", type=1)
    )


@bot.event
async def on_guild_join(guild: discord.Guild):
    logger.info(f"새로운 서버에 참여했습니다! : {guild.name}")
    with open(
        file="./server_configs/sample_config.json", mode="rt", encoding="utf-8"
    ) as sample_config_file:
        config: dict = json.load(fp=sample_config_file)
        config["guild_name"] = guild.name
        bot.guild_configs[guild.name] = config


@bot.event
async def on_guild_remove(guild: discord.Guild):
    logger.info(f"참여했던 서버에서 나갔습니다... : {guild.name}")
    # 저장해두던 서버 설정에서 나간 서버의 설정파일 지우기
    del bot.guild_configs[guild.name]

    # 로컬에 저장된 서버 설정 파일 지우기
    files: list = os.listdir("./server_configs")
    removed_server_config_file_name = f"{guild.name}_config.json"
    for file in files:
        if file == config_file_name:
            try:
                os.remove(path=f"./server_configs/{removed_server_config_file_name}")
            except Exception as e:
                logger.error(e.with_traceback(e.__traceback__))


@bot.event
async def on_command_error(ctx: commands.Context, e: Exception):
    logger.error(e.with_traceback(e.__traceback__))


if __name__ == "__main__":
    # print ASCII ART
    with open(file="resources/latte_ascii.txt", mode="rt", encoding="utf-8") as f:
        print(f.read())

    # init bot settings : loads config, server settings
    bot.settings_init()

    # set token
    print(f"token = {token}")

    # run bot
    bot.run(token)

    # save datas before program stops
    result, error = bot.settings_save()
    print(f"save_datas() 실행결과 : {result}")
    if error is not None:
        print(f"save_datas() 실행결과 발생한 오류 : {error.with_traceback(error.__traceback__)}")

    # check if the bot need to be rebooted
    bot.check_reboot()
