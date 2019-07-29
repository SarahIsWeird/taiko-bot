#!/usr/bin/env python3
import datetime
import locale
import re
import sys
import threading

from Utils import apiReq
from Utils import config
from Utils import irccon
from Utils import pp
from Utils import rateLimiting
from Utils import CommandHandler
from Utils import ConsoleCommandHandler
from Utils import roundString

QUIT = False

conf = config.Config('bot.conf')

locale.setlocale(locale.LC_TIME, '')

api = apiReq.API(conf)

# IRC Setup

ircName = conf.get('username')

irc = irccon.IRC()
irc.server(conf.get('ircServer'), conf.get('port'))
irc.auth(ircName, conf.get('pw'))
irc.setRecvBufSize(conf.get('recv_buf'))
irc.setRateLimit(conf.get('rate_limit'))

# Rate limiting setup

rateLimiting.setBurstTime(conf.get('burst_time'))
rateLimiting.setMinuteLimit(conf.get('minute_count'))

# The main hook of the bot. This is called when a PRIVMSG is received.
# The function finds issued commands and responds correspondingly.
def msgHook(ircClient: irccon.IRC, line):
	user = line['user']
	msg: str = line['msg']

	# NEVER EVER REMOVE THIS!!!!! We can't have ANY messages sent to a channel!
	if msg.find('#') != -1:
		return
	
	if rateLimiting.rateLimit(conf, user):
		irc.msg(user, 'Whoa! Slow down there, bud!')
		print(f'Rate limited user {user}.')
		return

	CommandHandler.handle(user, msg, ircClient, conf, api)


class ConsoleThread(threading.Thread):
	def run(self):
		print('<3 Welcome to Sarah\'s bot console! :D Here\'s a list of commands you can use:')
		print('<3  beatmap | bm: Test the beatmap feature!')
		print('<3 lastplay | lp: Calls /beatmap/ with your last played map!')
		print('<3     with |  w: Sets the accuracy and misses for the last queried map.')
		print('<3     quit |  q: Quit! D:')
		print('<3 Enter \'cancel\' at anytime to stop the current command!')
		print('')

		while True:
			consoleInput = input('').strip()

			if consoleInput == 'quit' or consoleInput == 'q':
				irc.queueEvent(irccon.IRCQuitEvent())
				return
			
			ConsoleCommandHandler.handle(consoleInput, conf, api, ircName)

# Add the hook on a PRIVMSG to the client.
irc.addEventHook('PRIVMSG', msgHook)

consoleThread = ConsoleThread()
consoleThread.start()

while True:
	irc.receive()
