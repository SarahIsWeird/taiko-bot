import datetime

#Called when pm'd with anything that's not a function
def run(user, msg, ircClient, conf, api, time):
	print(f'{time} {user}: {msg}')