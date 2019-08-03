#Called when pm'd with
#	!help
def run(user, msg, ircClient, conf, api, time):
    ircClient.msg(user, 'A list of commands can be found in the [GitHub wiki](https://github.com/SarahIsWeird/taiko-bot/wiki/Commands).')
    print(f'{time} Printed command list for {user}.')