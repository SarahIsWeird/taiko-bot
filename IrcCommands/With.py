import re
from Utils import config
from Utils import pp
from Utils import roundString

#Called when pm'd with
#	!with <acc> <misses>
def run(user, msg, irc, conf, api):
	try:
		userBeatmap = conf.load(user)
	except KeyError:
		irc.msg(user, 'Please select a beatmap first! (Type /np)')
		print(f'User {user} issued !with without a beatmap selected.')
		return

	lastBm = userBeatmap[0]
	mods = userBeatmap[1]

	artist = lastBm['artist']
	title = lastBm['title']
	diffName = lastBm['version']
	stars = float(lastBm['difficultyrating'])
	maxCombo = int(lastBm['count_normal'])
	od = pp.scaleHPOD(float(lastBm['diff_overall']), mods)

	arg1Regex = re.compile(r'!with ([^ ]*)? ') # Gets the first argument
	arg2Regex = re.compile(r'!with .*? ([^ ]*)?')

	accFloatRegex = re.compile(r'([0-9]{1,3})[\.\,]([0-9]{1,2})[%]*') # xx[x].yy[%] => Group 1: xx[x]; Group 2: yy
	accIntRegex = re.compile(r'([0-9]{1,3})[%]*') # xx[x][%] -> Group 1: xx[x]

	print(f'User {user} issued a !with command.')

	rawAcc = arg1Regex.search(msg)
	if rawAcc == None: # No first argument?
		irc.msg(user, 'Usage: !with <accuracy> <misses>')
		print(f'Printed usage for !with for {user}. (No arguments)')
		return

	accMatch = accFloatRegex.search(rawAcc.group(0))
	if accMatch == None: # Couldn't find the accuracy (xx[x].yy[%]).
		accMatch = accIntRegex.search(rawAcc.group(0))
		if accMatch == None: # Couldn't find the accuracy (xx[x][%]). -> Odd argument.
			irc.msg(user, 'Usage: !with <accuracy> <misses>')
			print(f'Printed usage for !with for {user}. (Odd accuracy)')
			return
			
		acc = float(accMatch.group(1))
	else:
		acc = float(accMatch.group(1) + '.' + accMatch.group(2)) # Two groups ignoring the floating point cuz localization.

	rawMisses = arg2Regex.search(msg)
	if rawMisses == None: # No second argument?
		irc.msg(user, 'Usage: !with <accuracy> <misses>')
		print(f'Printed usage for !with for {user}. (No second argument)')
		return

	missesMatch = re.search('([0-9]*)', rawMisses.group(1)) # Look if the second argument only contains numbers.
	if missesMatch == None:
		irc.msg(user, 'Usage: !with <accuracy> <misses>')
		print(f'Printed usage for !with for {user}. (Odd misses)')
		return

	misses = int(missesMatch.group(0))

	hundreds = pp.getHundreds(maxCombo, misses, acc)

	peppyPoints = roundString.roundString(pp.calcPP(stars, maxCombo, maxCombo - misses, hundreds, misses, acc, od, mods), 2)

	modString = pp.getModString(mods)

	irc.msg(user, f'{artist} - {title} [{diffName}]{modString} | {acc}%, {misses} misses: {peppyPoints}')
	print(f'{artist} - {title} [{diffName}]{modString} | {acc}%, {misses} misses: {peppyPoints}')

	conf.save(user, [lastBm, mods, acc, misses])