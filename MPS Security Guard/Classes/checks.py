# Community
from discord.ext import commands

# Mine
from Classes.extra_functions import is_officer
from Classes.extra_functions import is_higher_up
import Classes.errors as errors


def is_mps():
    def predicate(ctx):
        if is_officer(ctx.bot, ctx.author) is False:
            raise errors.MPSOnly()
        return True

    return commands.check(predicate)


def is_staff_role():
    def predicate(ctx):
        if is_higher_up(ctx.bot, ctx.author) is False:
            raise errors.StaffRoleOnly()
        return True

    return commands.check(predicate)


def is_admin_bot_channel():
    def predicate(ctx):
        if ctx.message.channel.id != ctx.bot.settings["admin_bot_channel"]:
            raise errors.WrongChannel("This command only works in the admin bot channel.")
        return True

    return commands.check(predicate)


def is_general_bot_channel():
    def predicate(ctx):
        if ctx.message.channel.id != ctx.bot.settings["admin_bot_channel"] and ctx.message.channel.id != \
                ctx.bot.settings["general_bot_channel"]:
            raise errors.WrongChannel("This command only works in the general bot channel or admin bot channel.")
        return True

    return commands.check(predicate)
