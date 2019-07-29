from Utils import pp
from Utils import roundString
from Utils import config

def run(consoleInput, conf, api, ircName):
	splitInput = consoleInput.split(' ')

	try:
		mods = pp.getModVal(consoleInput)

		userBeatmap = conf.load(ircName)
	except KeyError:
		print('Please select a beatmap first!')
		return
	except:
		print('Usage: mods <mod1> [mod2] [mod3]...')
		return

	lastBm = userBeatmap[0]
	acc = userBeatmap[2]
	misses = userBeatmap[3]

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