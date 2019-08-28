class script:
    """
    A class containing data for running a shell script
    """

    def __init__(self, shell="/bin/sh", payload="echo payload", user="root"):
        """
        @shell the shell that is running this very script
        @payload the commands that the shell will be running
        @user the user that is going to run this shell script
        """
        self.shell = shell
        self.payload = payload
        self.user = user
