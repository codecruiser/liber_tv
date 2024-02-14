# LibreBus is an object used to facilite inner communication between elements in the app.
# It was created to separate explicit communication from standard one.

class LibreBus(object):

    channels = {}

    def __new__(cls):
        # let's have it as a singelton
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def register(self, channel_name, communicator):
        """
        Adds a communicator method into a list of the channel.

        :param channel_name: a name of communication line
        :param communicator: a method which will be receiver
        """
        if not channel_name in self.channels:
            self.channels[channel_name] = []
        if communicator not in self.channels[channel_name]:
            self.channels[channel_name].append(communicator)

    def unregister(self, channel_name, communicator):
        """
        Removes communicator from channel.

        :param channel_name: a name of communication line
        :param communicator: a method which will be receiver
        """
        if channel_name in self.channels and communicator in self.channels[channel_name]:
            del self.channels[channel_name][self.channels[channel_name].index[communicator]]

    def send_msg(self, channel_name, message=None):
        """
        Sends a message to a channel for all methods, functions register for it.

        :param channel_name: a name of communication line
        :param message: message to be send
        """
        for func in self.channels[channel_name]:
            func(message)
