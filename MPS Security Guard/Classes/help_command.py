import discord
from discord.ext import commands

from Classes.extra_functions import handleError


class Help(commands.Cog):
    """
    A cog for providing help information about the bot's commands.
    """

    def __init__(self, bot):
        """
        Initialize the Help cog.

        Parameters:
        bot (discord.ext.commands.Bot): The bot instance.
        """
        self.bot = bot
        self.missing_help_information_str = "No help information"

    def get_title(self, command):
        """
        Get the title of a command.

        Parameters:
        command (discord.ext.commands.Command): The command.

        Returns:
        str: The title of the command.
        """
        return f"{self.bot.command_prefix}{command.name} {command.signature}"

    def _get_short_long_description(self, long_help_text):
        """
        Get the short and long descriptions from a help text.

        Parameters:
        long_help_text (str): The help text.

        Returns:
        tuple: A tuple containing the short description and the long description.
        """
        if not long_help_text:
            return self.missing_help_information_str, self.missing_help_information_str

        split_help_text = long_help_text.split("\n")
        short_desc_done = False
        short_desc = ""
        long_desc = ""
        for line in split_help_text:
            if not short_desc_done:
                if line != "":
                    short_desc += line
                else:
                    short_desc_done = True

            if line != "":
                long_desc += line + " "
            else:
                long_desc += "\n\n"

        return short_desc, long_desc

    def get_short_description(self, long_help_text):
        """
        Get the short description from a help text.

        Parameters:
        long_help_text (str): The help text.

        Returns:
        str: The short description.
        """
        return self._get_short_long_description(long_help_text)[0]

    def get_long_description(self, long_help_text):
        """
        Get the long description from a help text.

        Parameters:
        long_help_text (str): The help text.

        Returns:
        str: The long description.
        """
        return self._get_short_long_description(long_help_text)[1]

    @staticmethod
    async def can_use(command, ctx):
        """
        Check if a command can be used in the current context.

        Parameters:
        command (discord.ext.commands.Command): The command.
        ctx (discord.ext.commands.Context): The context.

        Returns:
        bool: True if the command can be used, False otherwise.
        """
        try:
            await command.can_run(ctx)
            return True
        except commands.CommandError:
            return False

    @staticmethod
    async def send_error(ctx, error_message):
        """
        Send an error message to the context.

        Parameters:
        ctx (discord.ext.commands.Context): The context.
        error_message (str): The error message.
        """
        await ctx.send(None, embed=discord.Embed(
            title="Error",
            description=error_message,
            color=discord.Color.red()
        ))

    @commands.command(pass_context=True)
    @commands.has_permissions(add_reactions=True, embed_links=True)
    async def help(self, ctx, *command):
        """
        Get information about all the commands.
        """
        try:
            if not command:
                help_embed = discord.Embed(
                    title="Accessable commands",
                    description=f"Use `{self.bot.command_prefix}help command` to find out more information about a specific command",
                    color=discord.Color.from_rgb(255, 255, 51)
                )

                for single_command in self.bot.walk_commands():
                    if await self.can_use(single_command, ctx):
                        title = self.get_title(single_command)
                        short_description = self.get_short_description(single_command.help)
                        help_embed.add_field(name=title, value=short_description, inline=False)

                await ctx.send(None, embed=help_embed)

            else:
                if len(command) > 1:
                    await self.send_error(ctx, "You passed in too many arguments.")
                    return

                for command_in_bot in self.bot.commands:
                    if command_in_bot.name == command[0]:
                        if await self.can_use(command_in_bot, ctx):
                            await ctx.send(None, embed=discord.Embed(
                                title=self.get_title(command_in_bot),
                                description=self.get_long_description(command_in_bot.help),
                                color=discord.Color.green()
                            ))
                        else:
                            await self.send_error(ctx, "The command you searched for cannot be used here.")
                        break

                else:
                    await self.send_error(ctx, "The command you searched for was not found.")

        except Exception as error:
            await ctx.send("Something failed with the help command.")
            await handleError(self.bot, error)
