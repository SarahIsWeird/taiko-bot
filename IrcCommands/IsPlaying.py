import re
from Utils import config
from Utils import pp
from Utils import apiReq
from Utils import roundString

#Called when pm'd with
#	/np during a map
def run(user, msg, irc, conf, api):    
	diffnameRegex = re.compile(r'\[.*\[(.*)\]\]') # The regex finding the difficulty name, see 'diffname ='.
	setidRegex = re.compile(r'/b/([0-9]*)')       # The regex finding the set id, see 'setid ='.

	setid = setidRegex.search(msg).group(1)
	diffname = diffnameRegex.search(msg).group(1) # Search for [...], e.g. [Oni]
	isTaiko = bool(re.search(r'<Taiko>', msg))    # Determines whether the beatmap is in taiko mode or not.
													# This will not filter out converts!

	modsVal = 0 # The binary number given to pp.calcPP() containing the enabled mods.
	mods = ''   # The string used for message building.

	for mod in pp.mods: # Loop through the mods and change the modsVal according to the enabled mods.
		if msg.find('+' + mod) != -1:
			modsVal += pp.mods[mod]
			mods = ' '.join([mods, f'+{mod}'])

	# Console logging
	print(f'{user} issued a request for beatmap set id {setid}, difficulty [{diffname}]{mods}, the beatmap was ', end='')
	if isTaiko:
		print('in taiko mode.')
	else:	
		print('not in taiko mode.')
							
	requestedBeatmap = None # Set to None to check if set later on.

	foundTaikoMap = False   # Was there a taiko map in the set?
		
	beatmapSet = api.getBeatmap(setid, modsVal)
		
	for beatmap in beatmapSet: # Loop through all the beatmaps in the set
		if beatmap['mode'] != '1': # Speed up the process for mixed-mode beatmap sets
			continue
			
		if beatmap['mode'] == '1': # 'mode' == 1 means the beatmap mode is osu!taiko.
			foundTaikoMap = True
			
		if beatmap['version'] != diffname: # Skip the difficulties with the wrong difficulty name.
			continue
			
		requestedBeatmap = beatmap
		conf.save(user, [beatmap, modsVal, 100.0, 0])
		
	if requestedBeatmap == None and foundTaikoMap == True:
		print(f'Beatmap set id {setid} with difficulty name [{diffname}] could not be found. Is there an error?')
		irc.msg(user, 'I\'m sorry, but the beatmap could not be found. Perhaps Bancho had an error?')
		return
	elif foundTaikoMap == False:
		print(f'Beatmap set id {setid} did not contain a Taiko difficulty.')
		irc.msg(user, 'The map you requested doesn\'t appear to be a taiko map. Converts are not (yet) supported, sorry.')
		return
		
	# Metadata collection for marginally easier to read code.
	artist = requestedBeatmap['artist']
	title = requestedBeatmap['title']
	diffName = requestedBeatmap['version']
	creator = requestedBeatmap['creator']
	stars = float(requestedBeatmap['difficultyrating'])
	starsRounded = roundString.roundString(stars, 2)
	maxCombo = int(requestedBeatmap['count_normal'])
	od = pp.scaleHPOD(float(requestedBeatmap['diff_overall']), modsVal)
	hp = pp.scaleHPOD(float(requestedBeatmap['diff_drain']), modsVal)
	bpm = pp.scaleBPM(requestedBeatmap['bpm'], modsVal) # Not converted to int because we only use it for printing
		
	# The first line shown to the user containing general info about the difficulty.
	irc.msg(user, f'{artist} - {title} [{diffName}] by {creator}, {starsRounded}* {mods} OD{od} HP{hp} BPM: {bpm} FC: {maxCombo}')
		
	ppString = '' # The string shown to the user as the second line in the end.
		
	# Calculate the pp for the accuracies in the tuple
	for acc in (95.0, 96.0, 97.0, 98.0, 99.0, 100.0):
		ppVal = roundString.roundString(pp.calcPP(stars, maxCombo, maxCombo, pp.getHundreds(maxCombo, 0, acc), 0, acc, od, modsVal), 2)
		e = ' | ' # Separator
		if acc == 95.0: # Avoid a trailing ' | '.
			e = ''
		ppString = f'{ppString}{e}{acc}%: {ppVal}pp'

	# The second line.
	irc.msg(user, ppString)
	print(f'OD{od} {starsRounded}* FC: {maxCombo}x')
	print(ppString + '\n')

	conf.save(user, [requestedBeatmap, modsVal, 100, 0])