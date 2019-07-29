from Utils import pp
from Utils import config
from Utils import roundString

#Called when pm'd with
#	!mods <mods..>
def run(user, msg, irc, conf, api):	
	try:
		mods = pp.getModVal(msg)
		userBeatmap = conf.load(user)
	except KeyError:
		irc.msg(user, 'Please select a beatmap first! (Type /np)')
		print(f'User {user} issued !with without a beatmap selected.')
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
	creator = lastBm['creator']
	stars = float(lastBm['difficultyrating'])
	starsRounded = roundString.roundString(stars, 2)
	maxCombo = int(lastBm['count_normal'])
	od = float(lastBm['diff_overall'])
	hp = pp.scaleHPOD(float(lastBm['diff_drain']), mods)
	bpm = pp.scaleBPM(lastBm['bpm'], mods)
	
	hundreds = pp.getHundreds(maxCombo, misses, acc)
	
	modString = pp.getModString(mods)
		
	irc.msg(user, f'{artist} - {title} [{diffName}] by {creator}, {starsRounded}* {modString} OD{od} HP{hp} BPM: {bpm} FC: {maxCombo}')

	ppString = ''

	# Calculate the pp for the accuracies in the tuple
	for acc in (95.0, 96.0, 97.0, 98.0, 99.0, 100.0):
		ppVal = roundString.roundString(pp.calcPP(stars, maxCombo, maxCombo, pp.getHundreds(maxCombo, 0, acc), 0, acc, od, mods), 2)
		e = ' | ' # Separator
		if acc == 95.0: # Avoid a trailing ' | '.
			e = ''
		ppString = f'{ppString}{e}{acc}%: {ppVal}pp'

	od = pp.scaleHPOD(od, mods)

	# The second line.
	irc.msg(user, ppString)
	print(f'OD{od} HP{hp} {starsRounded}* FC: {maxCombo}x')
	print(ppString + '\n')

	conf.save(user, [lastBm, mods, acc, misses])