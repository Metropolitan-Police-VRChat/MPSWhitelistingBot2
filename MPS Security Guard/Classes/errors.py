# Community

# Community
from discord.ext import commands


class MPSOnly(commands.CheckFailure):
    """
    Custom exception for checking if a command can only be used by MPS members.

    Attributes:
    -----------
    message : str
        The error message to be displayed when the check fails.
        Defaults to 'This command can only be used by MPS members. Please make sure you have the correct role assigned.'

    Methods:
    --------
    __init__(self, message=None)
        Initializes the MPSOnly exception with the provided message.
        If no message is provided, it defaults to the predefined message.
    """

    def __init__(self, message=None):
        super().__init__(
            message or 'This command can only be used by the MPS Staff Team. Please make sure you have the correct role assigned.')


class StaffRoleOnly(commands.CheckFailure):
    """
    Custom exception for checking if a command can only be used by MPS White Shirts.

    Attributes:
    -----------
    message : str
        The error message to be displayed when the check fails.
        Defaults to 'This command can only be used by MPS White Shirts. Please make sure you have the correct role assigned.'

    Methods:
    --------
    __init__(self, message=None)
        Initializes the StaffRoleOnly exception with the provided message.
        If no message is provided, it defaults to the predefined message.
    """

    def __init__(self, message=None):
        super().__init__(
            message or 'This command can only be used by the MPS Staff Team. Please make sure you have the correct role assigned.')


class WrongChannel(commands.CheckFailure):
    """
    Custom exception for checking if a command cannot be used in the current channel.

    Attributes:
    -----------
    message : str
        The error message to be displayed when the check fails.
        Defaults to 'This command cannot be used in this channel. Please make sure you are in the correct channel.'

    Methods:
    --------
    __init__(self, message=None)
        Initializes the WrongChannel exception with the provided message.
        If no message is provided, it defaults to the predefined message.
    """

    def __init__(self, message=None):
        super().__init__(
            message or 'This command cannot be used in this channel. Please make sure you are in the correct channel.')


class WrongServer(commands.CheckFailure):
    """
    Custom exception for checking if a bot does not work in the current server.

    Attributes:
    -----------
    message : str
        The error message to be displayed when the check fails.
        Defaults to 'This bot does not work in this server. Please make sure you are in the correct server.'

    Methods:
    --------
    __init__(self, message=None)
        Initializes the WrongServer exception with the provided message.
        If no message is provided, it defaults to the predefined message.
    """

    def __init__(self, message=None):
        super().__init__(
            message or 'This bot does not work in this server. Please make sure you are in the correct server.')
