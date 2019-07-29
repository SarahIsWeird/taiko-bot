from Utils import apiReq
from Utils import config
from Utils import roundString
from Utils import pp

def run(consoleInput, conf, api, ircName):
	try:
		bm_id = input('<3 Awesome! First we need a beatmap id: ').strip()
		if bm_id == 'cancel':
			return
		bm_id = int(bm_id)

		bm_acc = input('<3 Now the accuracy: ').strip()
		if bm_acc == 'cancel':
			return
		bm_acc = float(bm_acc)

		bm_misses = input('<3 How many misses? \'cancel\' to cancel').strip()
		if bm_misses == 'cancel':
			return
		bm_misses = int(bm_misses)

		# bm_mods = input('')
	except:
		if bm_id == None:
			print('<3 Please enter a valid beatmap id!')
		elif bm_acc == None:
			print('<3 Please enter a valid accuracy! (No percent sign!)')
		else:
			print('<3 Please enter a valid number of misses!')
		return

	beatmap = api.getBeatmap(bm_id)[0]
	conf.save(ircName, [beatmap, pp.mods['noMod'], bm_acc, bm_misses])

	artist = beatmap['artist']
	title = beatmap['title']
	diffName = beatmap['version']
	stars = float(beatmap['difficultyrating'])
	od = int(beatmap['diff_overall'])
	maxcombo = int(beatmap['count_normal'])

	peppyPoints = roundString.roundString(pp.calcPP(stars, maxcombo, maxcombo - bm_misses, pp.getHundreds(maxcombo, bm_misses, bm_acc), bm_misses, bm_acc, od, pp.mods['noMod']), 2)

	print(f'<3 {artist} - {title} [{diffName}] | {bm_acc}%, {bm_misses} misses, FC: {maxcombo}')
	print(f'<3 {peppyPoints}pp')