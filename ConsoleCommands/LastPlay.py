from Utils import irccon
from Utils import apiReq
from Utils import config
from Utils import pp
from Utils import roundString

def run(consoleInput, conf, api, ircName):
	lastPlay = api.getUserRecent(ircName)[0]

	fulls = int(lastPlay['count300'])
	hundreds = int(lastPlay['count100'])
	misses = int(lastPlay['countmiss'])
	mods = int(lastPlay['enabled_mods'])
	combo = int(lastPlay['maxcombo'])

	beatmap = api.getBeatmap(lastPlay['beatmap_id'], mods)[0]
	conf.save(ircName, [beatmap, mods])

	artist = beatmap['artist']
	title = beatmap['title']
	diffName = beatmap['version']
	stars = float(beatmap['difficultyrating'])
	od = float(beatmap['diff_overall'])
	maxcombo = int(beatmap['count_normal'])

	acc = (hundreds * 0.5 + fulls) / maxcombo * 100
	accStr = roundString.roundString(acc, 2)

	peppyPoints = roundString.roundString(pp.calcPP(stars, maxcombo, maxcombo - misses, hundreds, misses, acc, od, mods), 2)
				
	modStr = pp.getModString(mods)

	print(f'<3 {artist} - {title} [{diffName}]{modStr} | {accStr}%, {misses} misses, FC: {maxcombo}')
	print(f'<3 Highest Combo: {combo} | {peppyPoints}pp')