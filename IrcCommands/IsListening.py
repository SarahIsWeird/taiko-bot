#Called when pm'd with
#	/np when not playing a map
def run(user, msg, ircClient, conf, api):
	ircClient.msg(user, 'Please start playing the beatmap you want and then do /np!')
	print(f'User {user} listened to a beatmap!\n')