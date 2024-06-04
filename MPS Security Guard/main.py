import asyncio
import logging
import os
import traceback
from sys import platform

import discord
from discord.ext import commands

import Classes.commands as bot_commands
import Classes.errors as errors
import Classes.help_command as help_command
from Classes.UserManager import UserManager
from Classes.extra_functions import get_settings_file, handleError, is_officer, check_officer_status

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Determine settings file dynamically
settings_file_name = "remote_settings" if platform.startswith("linux") else "test_settings"
settings = get_settings_file(settings_file_name)

# Initialize bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=settings["bot_prefix"], help_command=None, intents=intents)
bot.settings = settings
bot.user_manager = UserManager(bot, "vrc_name_db.csv")


# Global checks
@bot.check
def supports_dms(ctx):
    """
    Check if the bot supports direct messages.

    Parameters:
    ctx (discord.ext.commands.Context): The context of the command.

    Returns:
    bool: True if the bot supports direct messages, False otherwise.
    """
    if ctx.guild is None:
        raise commands.NoPrivateMessage("This bot does not support direct messages.")
    return True


@bot.check
def is_correct_server(ctx):
    """
    Check if the command is executed in the correct server.

    Parameters:
    ctx (discord.ext.commands.Context): The context of the command.

    Returns:
    bool: True if the command is executed in the correct server, False otherwise.
    """
    if ctx.guild.id != bot.settings["Server_ID"]:
        raise errors.WrongServer()
    return True


# Discord Events
@bot.event
async def on_ready():
    """
    Event triggered when the bot is ready.
    """
    logger.info("Bot is ready")
    await bot.loop.create_task(check_officer_status(bot))
    await asyncio.gather(
        bot.add_cog(help_command.Help(bot)),
        bot.add_cog(bot_commands.VRChatAccoutLink(bot)),
        bot.add_cog(bot_commands.Other(bot))
    )


@bot.event
async def on_member_update(before, after):
    """
    Event triggered when a member's information is updated.

    Parameters:
    before (discord.Member): The member before the update.
    after (discord.Member): The member after the update.
    """
    if is_officer(bot, before) and not is_officer(bot, after):
        bot.user_manager.remove_user(before.id)


@bot.event
async def on_error(event):
    """
    Event triggered when an error occurs in an event.

    Parameters:
    event (str): The name of the event.
    *args: Variable length argument list.
    **kwargs: Arbitrary keyword arguments.
    """
    logger.error(f"Error encountered in event: {event}")
    await handleError(bot, f"Error encountered in event: {event}")


@bot.event
async def on_command_error(ctx, exception):
    """
    Event triggered when a command error occurs.

    Parameters:
    ctx (discord.ext.commands.Context): The context of the command.
    exception (Exception): The exception that occurred.
    """
    logger.info("on_command_error triggered")
    exception_message = str(exception).replace("raised an exception", "encountered a problem")
    await ctx.send(exception_message)

    debug_channel = bot.get_channel(bot.settings["bot_debug_channel"])
    if debug_channel is not None:
        traceback_info = traceback.format_exc()
        error_message = (
            f"***ERROR***\n\n"
            f"{exception_message}\n"
            f"{traceback_info}"
        )
        logger.error(error_message)
        await debug_channel.send(error_message)


# Start the bot
bot_token = os.getenv("DISCORD_BOT_TOKEN")
if bot_token:
    bot.run(bot_token)
else:
    logger.error("Bot token not found. Please set the DISCORD_BOT_TOKEN environment variable.")
