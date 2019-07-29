#Called when pm'd with
#	!discord
def run(user, msg, ircClient, conf, api):
    ircClient.msg(user, 'The place to talk about the bot or just chat: https://discord.gg/hKXQdm2')
    print(f'Printed discord invite for {user}.')