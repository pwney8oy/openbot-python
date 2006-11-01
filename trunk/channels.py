class Channels:
    def __init__(self):
        self.chans = {}
        self.identify = {}
        self.invalid_chan = lambda chan: "The Bot isn't in %s"% (chan)

    def users_grade(self, channel, grade):
        """"Returns an unsorted list of the persons that have
        a mode (grade) set in the channel.
        """
        if self.chans.has_key(channel):
            return self.chans[channel][grade].keys()
        else:
            self.invalid_chan(channel)

    def get_users(self, channel):
        """Returns an unsorted list of the channel's users.
        Sometimes returns some clones.
        """
        if self.chans.has_key(channel):
            return self.chans[channel][""]

    def channels(self):
        """Returns an unsorted list of the channels
        """
        return self.chans.keys()

    def users(self, channel):
        """Returns an unsorted list of the channel's users.
        """
        if self.chans.has_key(channel):
            return self.get_users(channel).keys()
        else:
            self.invalid_chan(channel)

    def get_users_channels(self, nick):
        """Return an unsorted list where nick is
        """
        channels = []
        for chan in self.chans.keys():
            users = self.chans[chan]
            for user in users[""]:
                if nick in user:
                    channels.append(chan)
        return channels

    def opers(self, channel):
        """Returns an unsorted list of the channel's operators.
        """
        return self.users_grade(channel, "o")

    def halfop(self, channel):
        """Returns an unsorted list of the persons that have halfop
        mode set in the channel.
        """
        return self.users_grade(channel, "h")

    def voiced(self, channel):
        """Returns an unsorted list of the persons that have voice
        mode set in the channel.
        """
        return self.users_grade(channel, "v")

    def identified(self):
        """Returns an unsorted list of the persons that have idenfied.
        """
        return self.identify

    def has_user(self, channel, nick):
        """Check whether the channel has a user.
        """
        return nick in self.get_users(channel)

    def is_in(self, channel):
        return self.chans.has_key(channel)

    def is_oper(self, channel, nick):
        """Check whether a user has operator status in the channel.
        """
        return nick in self.users_grade(channel, "o")

    def is_halfop(self, channel, nick):
        """Check whether a user has half-operator status in the channel.
        """
        return nick in self.users_grade(channel, "h")

    def is_voiced(self, channel, nick):
        """Check whether a user has voice mode set in the channel.
        """
        return nick in self.users_grade(channel, "v")

    def is_identified(self, nick):
        """Check whether a user has identified.
        """
        return nick in self.identify

    def add_channel(self, channel):
        """Just add a channel in self.chans.
        """
        self.chans[channel] = {"":{}, "o":{}, "h":{}, "v":{}, "i":{}}

    def add_user(self, channel, nick):
        """Just add an user in a channel without any modes.
        """
        self.chans[channel][""][nick] = 1

    def remove_user(self, channel, nick):
        """Remove an user from a channel.
        """
        if channel == ".all.":
            for chan in self.chans.keys():
                chan = self.chans[chan]
                for user in chan[""], chan["o"], chan["h"], chan["v"], chan["i"]:
                    if nick in user:
                        del user[nick]
        else:
            chan = self.chans[channel]
            for user in chan[""], chan["o"], chan["h"], chan["v"], chan["i"]:
                if nick in user:
                    del user[nick]

    def change_nick(self, before, after):
        channels = []
        for chan in self.chans.keys():
            if before in chan:
                channels.append(chan)
        for channel in channels:
            self.add_user(channel, after)
            if is_oper(channel, before):
                self.set_mode(channel, after, "o")
            if is_halfop(channel, before):
                self.set_mode(channel, after, "h")
            if is_voiced(channel, before):
                self.set_mode(channel, after, "v")
            if is_identified(before):
                self.set_mode(channel, after, "i")
        self.remove_user(".all.", before)

    def set_mode(self, channel, nick, mode):
        """Set mode on the channel.
        """
        if mode in ("o", "h", "v"):
            if self.chans.has_key(channel):
                self.chans[channel][mode][nick] = 1
            else:
                self.invalid_chan(channel)
        elif mode == "i":
            self.identify[nick] = 1
        else:
            return "Invalid mode!"
        
    def clear_mode(self, channel, nick, mode):
        """Clear a mode on the channel.
        """
        if mode in ("o", "h", "v", "i"):
            if self.chans.has_key(channel):
                del self.chans[channel][mode][nick]
            else:
                self.invalid_chan(channel)
        else:
            return "Invalid mode!"
