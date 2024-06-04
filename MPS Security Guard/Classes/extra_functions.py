import asyncio
import traceback

import commentjson as json
import discord


def get_settings_file(settings_file_name, in_settings_folder=True):
    file_path = f"settings/{settings_file_name}.json" if in_settings_folder else f"{settings_file_name}.json"
    with open(file_path, "r") as json_file:
        return json.load(json_file)


async def handleerror(bot, *text):
    error_text = "***ERROR***\n\n" + "\n".join(map(str, text)) + "\n" + traceback.format_exc()
    print(error_text)
    channel = bot.get_channel(bot.settings["bot_debug_channel"])
    try:
        await channel.send(error_text)
    except discord.InvalidArgument:
        await channel.send("***I ENCOUNTERED AN ERROR AND THE ERROR MESSAGE DOES NOT FIT IN DISCORD.***")


def is_officer(bot, member):
    if member is None: return False
    officer_roles = [x["id"] for x in bot.settings["role_ladder"] if x.get("is_officer")]
    return any(role.id in officer_roles or role.id == bot.settings["MPS_role"] for role in member.roles)


def is_higher_up(bot, member):
    if member is None: return False
    staff_roles = [x["id"] for x in bot.settings["role_ladder"] if x.get("is_staff_role")]
    return any(role.id in staff_roles for role in member.roles)


async def check_officer_status(bot):
    await bot.wait_until_ready()
    guild = bot.get_guild(bot.settings["Server_ID"])
    while not bot.is_closed():
        try:
            for user_id, _ in bot.user_manager.all_users.copy():
                member = guild.get_member(user_id)
                if not member or not is_officer(bot, member):
                    bot.user_manager.remove_user(user_id)
        except Exception as error:
            print("Error when checking officer health")
            print(error)
            print(traceback.format_exc())
        await asyncio.sleep(3600)


async def send_long_str(ctx, string):
    output_str = ""
    for line in string.splitlines():
        if len(output_str + line + "\n") < 2000:
            output_str += line + "\n"
        else:
            await ctx.send(output_str)
            output_str = line
    await ctx.send(output_str)
