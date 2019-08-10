import IrcCommands
import datetime
from Utils import rateLimiting

#   When new command is created in IrcCommands folder, do the following
#     1. Add the import in IrcCommands/__init__.py
#     4. Add trigger:<IrcCommands.File> to CommandSwitch
def handle(user, msg, ircClient, conf, api):
	commandSwitch = {
		'is listening' : IrcCommands.IsListening,
		'is playing' : IrcCommands.IsPlaying,
		'!with' : IrcCommands.With,
		'!mods' : IrcCommands.Mods,
		'!discord' : IrcCommands.Discord,
		'!help' : IrcCommands.Help,
		'default' : IrcCommands.Default
	}
	actualCommand = parseCommand(msg, commandSwitch.keys())
	commandFile = commandSwitch[actualCommand]

	now = datetime.datetime.now()
	time = now.strftime('%r')
	
	# If no command is specified (i.e. when someone is chatting with me),
	# stop the rate limiting. This makes use of the smart boolean evaluation
	# (rateLimit() isn't called if the actualCommand isn't 'default'.)
	if not actualCommand == 'default' and rateLimiting.rateLimit(conf, user):
		ircClient.msg(user, 'Whoa! Slow down there, bud!')
		print(f'Rate limited user {user}.')
		return

	commandFile.run(user, msg, ircClient, conf, api, time)

def parseCommand(msg, commandList):
	for command in commandList:
		if command in msg:
			return command
	return 'default'