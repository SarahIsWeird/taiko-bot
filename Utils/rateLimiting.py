from datetime import datetime, timedelta
from . import config

burst = timedelta(seconds=3)
minute = timedelta(minutes=1)

minuteLimit = 4

rlSnip = '$rl_' # Distinguish between user data and rate-limit data.

def setBurstTime(secs: int):
	burst = timedelta(seconds=secs) #pylint: disable=unused-variable

def setMinuteLimit(count: int):
	minuteLimit = count #pylint: disable=unused-variable

# Handles rate limits for a user.
# Return values:  0: Not rate limited.
# 				 -1:    Burst limited.
# 				 -2:   Minute limited.
def rateLimit(conf, user):
	try:
		lastCalls = conf.load(rlSnip + user)
	except KeyError: # User not found, aka first time calling.
		conf.save(rlSnip + user, [datetime.now()])
		return 0
	
	# Burst handling

	mostRecentCall = lastCalls[-1]
	
	if datetime.now() - mostRecentCall < burst: # The user had too calls much back to back.
		return -1
	
	# Minute handling

	if len(lastCalls) < minuteLimit:
		lastCalls += [datetime.now()]
		conf.save(rlSnip + user, lastCalls)
		return 0
	
	leastRecentCall = lastCalls[0]

	if datetime.now() - leastRecentCall < minute:
		return -2 # The user is rate limited!
	
	del lastCalls[0]
	lastCalls += [datetime.now()]

	return False