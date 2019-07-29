import IrcCommands

#   When new command is created in IrcCommands folder, do the following
#     1. Add the import in IrcCommands/__init__.py
#     4. Add trigger:<IrcCommands.File> to CommandSwitch
def handle(user, msg, ircClient, conf, api):
	commandSwitch = {
		"is listening" : IrcCommands.IsListening,
		"is playing" : IrcCommands.IsPlaying,
		"!with" : IrcCommands.With,
		"!mods" : IrcCommands.Mods,
		"!discord" : IrcCommands.Discord,
		"!help" : IrcCommands.Help,
		"default" : IrcCommands.Default
	}
	actualCommand = parseCommand(msg, CommandSwitch.keys())
	commandFile = commandSwitch[actualCommand]
	commandFile.run(user, msg, ircClient, conf, api)

def parseCommand(msg, commandList):
	for command in commandList:
		if command in msg:
			return command
	return 'default'