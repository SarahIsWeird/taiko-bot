from Utils import pp
from Utils import roundString
from Utils import config

def run(consoleInput, conf, api, ircName):
	splitInput = consoleInput.split(' ')

	try:
		acc = float(splitInput[1])
		misses = int(splitInput[2])

		userBeatmap = conf.load(ircName)
	except KeyError:
		print('Please select a beatmap first!')
		return
	except:
		print('Usage: with <acc> <misses>')
		return

	lastBm = userBeatmap[0]
	mods = userBeatmap[1]

	artist = lastBm['artist']
	title = lastBm['title']
	diffName = lastBm['version']
	stars = float(lastBm['difficultyrating'])
	maxCombo = int(lastBm['count_normal'])
	od = float(lastBm['diff_overall'])
				
	hundreds = pp.getHundreds(maxCombo, misses, acc)

	peppyPoints = roundString.roundString(pp.calcPP(stars, maxCombo, maxCombo - misses, hundreds, misses, acc, od, mods), 2)

	modString = pp.getModString(mods)

	print(f'{artist} - {title} [{diffName}]{modString} | {acc}%, {misses} misses: {peppyPoints}')

	conf.save(ircName, [lastBm, mods, acc, misses])