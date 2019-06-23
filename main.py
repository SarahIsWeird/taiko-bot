#!/usr/bin/env python3
import re, irccon, apiReq, config, pp

conf = config.Config('bot.conf')

api = apiReq.API(conf)

def send(sock, s: str):
	sock.send(bytes(s + '\r\n', 'utf-8'))
	print('*ME* ' + s)

def roundString(s: str, digits: int):
	n = round(float(s), digits)
	return str(n)

irc = irccon.IRC()
irc.server(conf.get('ircServer'), conf.get('port'))
irc.auth(conf.get('username'), conf.get('pw'))

def msgHook(ircClient: irccon.IRC, line):
	user = line['user']
	msg: str = line['msg']

	if msg.find('#') == -1 and msg.find('is playing') != -1:
		diffnameRegex = re.compile(r'\[.*\[(.*)\]\]')
		setidRegex = re.compile(r'/b/([0-9]*)')
		setid = setidRegex.search(msg).group(1)
		diffname = diffnameRegex.search(msg).group(1) # Search for [...], e.g. [Oni]
		isTaiko = bool(re.search(r'<Taiko>', msg))

		print(f'{user} issued a request for beatmap set id {setid}, difficulty [{diffname}],\n the beatmap was ', end='')
		if isTaiko:
			print('in taiko mode.')
		else:
			print('not in taiko mode.')
							
		requestedBeatmap = None

		foundTaikoMap = False
		
		beatmapSet = api.getBeatmap(setid)
		
		for beatmap in beatmapSet: # Loop through all the beatmaps in the set
			if beatmap['mode'] != '1': # Speed up the process for mixed-mode beatmap sets
				continue
			
			if beatmap['mode'] == '1':
				foundTaikoMap = True
			
			if beatmap['version'] != diffname:
				continue
			
			requestedBeatmap = beatmap
		
		if requestedBeatmap == None and foundTaikoMap == True:
			print(f'Beatmap set id {setid} with difficulty name [{diffname}] could not be found. Is there an error?')
			irc.msg(user, 'I\'m sorry, but the beatmap could not be found. Perhaps Bancho had an error?')
			return
		elif foundTaikoMap == False:
			print(f'Beatmap set id {setid} did not contain a Taiko difficulty.')
			irc.msg(user, 'The map you requested doesn\'t appear to be a taiko map. Converts are not (yet) supported, sorry.')
			return
		
		artist = requestedBeatmap['artist']
		title = requestedBeatmap['title']
		diffName = requestedBeatmap['version']
		creator = requestedBeatmap['creator']
		stars = float(requestedBeatmap['difficultyrating'])
		starsRounded = roundString(stars, 2)
		maxCombo = int(requestedBeatmap['count_normal'])
		od = float(requestedBeatmap['diff_overall'])
		bpm = requestedBeatmap['bpm'] # Not converted to int because we only use it for printing
		
		irc.msg(user, f'{artist} - {title} [{diffName}] by {creator}, {starsRounded}* OD{od} BPM: {bpm} FC: {maxCombo}')
		# irc.msg(user, f'{starsRounded}*, FC: {maxCombo}, OD: {od}')
		
		ppString = ''
		
		for acc in (90.0, 95.0, 98.0, 99.0, 100.0):
			ppVal = roundString(pp.calcPP(stars, maxCombo, maxCombo, pp.getHundreds(maxCombo, 0, acc), 0, acc, od, pp.mods['noMod']), 2)
			e = ' | '
			if acc == 90.0:
				e = ''
			ppString = f'{ppString}{e}{acc}%: {ppVal}pp'

		irc.msg(user, ppString)
		return
	else:
		print(f'{user}: {msg}')

irc.addEventHook('PRIVMSG', msgHook)

while True:
	text = irc.receive()

	'''for line in text:
		splitLine = line.split(':')

		if len(splitLine) < 3:
			continue

		info = splitLine[1].split(' ')

		msg = splitLine[2]
		user = info[0].split('!')[0]
		cmd = info[1]

		if cmd == 'QUIT':
			continue

		elif cmd == 'PRIVMSG': # Example split line: ['', 'M1rr0R!cho@ppy.sh PRIVMSG SarahIsWeird ', 'hoi']
			if splitLine[2].find('quit') != -1 and user == 'SarahIsWeird':
				irc.disconnect()
				quit()
			
			# Example /np line: ['', 'Emre1504!cho@ppy.sh PRIVMSG SarahIsWeird ', '\\x01ACTION is playing [https',
			# '//osu.ppy.sh/b/1858055 Hello Sleepwalkers - Shinwa Houkai [Oni]] <Taiko>\\x01']
			print(f'{user}: {msg}')'''