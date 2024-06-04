# Standard
import csv

# Community


class UserManager:
    """
    This class handles interaction with the user storage CSV file.
    """

    def __init__(self, bot, file_name):
        """
        Initialize UserManager with bot instance and file name.

        Parameters:
        bot (discord.ext.commands.Bot): The bot instance.
        file_name (str): The name of the CSV file to store user data.
        """
        self.bot = bot
        self.file_name = file_name
        self.all_users = []
        self.read_list()

    def get_vrc_by_discord(self, discord_id):
        """
        Get VRChat username by Discord ID.

        Parameters:
        discord_id (int): The Discord ID.

        Returns:
        str: The VRChat username if found, otherwise None.
        """
        for user in self.all_users:
            if user[0] == discord_id:
                return user[1]
        return None

    def get_discord_by_vrc(self, vrchat_name):
        """
        Get Discord ID by VRChat username.

        Parameters:
        vrchat_name (str): The VRChat username.

        Returns:
        int: The Discord ID if found, otherwise None.
        """
        for user in self.all_users:
            if user[1] == vrchat_name:
                return user[0]
        return None

    def add_user(self, discord_id, vrchat_name):
        """
        Add a new user to the CSV file.

        Parameters:
        discord_id (int): The Discord ID.
        vrchat_name (str): The VRChat username.
        """
        self.remove_user(discord_id)
        self.all_users.append([discord_id, vrchat_name])
        self.write_list()

    def remove_user(self, discord_id):
        """
        Remove a user from the CSV file by Discord ID.

        Parameters:
        discord_id (int): The Discord ID.
        """
        i = 0
        while i < len(self.all_users):
            if self.all_users[i][0] == discord_id:
                del self.all_users[i]
            else:
                i += 1
        self.write_list()

    def read_list(self):
        """
        Read user data from the CSV file.
        """
        try:
            with open(self.file_name, "r", encoding="utf-8") as csv_file:
                cursor = csv.reader(csv_file)
                self.all_users = []
                for line in cursor:
                    if len(line) == 2:
                        self.all_users.append([int(line[0]), line[1]])
        except FileNotFoundError:
            self.all_users = []

    def write_list(self):
        """
        Write user data to the CSV file.
        """
        with open(self.file_name, "w", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file, lineterminator='\n')
            writer.writerows(self.all_users)
