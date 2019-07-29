import ConsoleCommands

#   When new command is created in ConsoleCommands folder, do the following
#     1. Add the import in ConsoleCommands/__init__.py
#     4. Add trigger:ConsoleCommands.Package to CommandSwitch
def handle(msg, conf, api, ircName):
	CommandSwitch = {
		"beatmap" : ConsoleCommands.Beatmap, "bm" : ConsoleCommands.Beatmap,
		"lastplay" : ConsoleCommands.LastPlay, "lp" : ConsoleCommands.LastPlay,
		"with" : ConsoleCommands.With, "w" : ConsoleCommands.With,
		"default" : ConsoleCommands.Default
	}
	actualCommand = parseCommand(msg, CommandSwitch.keys())
	commandFile = CommandSwitch[actualCommand]
	commandFile.run(msg, conf, api, ircName)

def parseCommand(msg, commandList):
	for command in commandList:
		if (msg.startswith(command)):
			return command
	return 'default'