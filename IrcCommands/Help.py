#Called when pm'd with
#	!help
def run(user, msg, ircClient, conf, api):
    ircClient.msg(user, 'A list of commands can be found in the [GitHub wiki](https://github.com/SarahIsWeird/taiko-bot/wiki/Commands).')
    print(f'Printed command list for {user}.')