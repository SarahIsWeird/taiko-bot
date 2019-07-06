import socket, re
from time import sleep

# A list of possible triggers to respond to.
triggers = ['PRIVMSG']

# The base IRC client exception class.
class IRCError(Exception):
	def __init__(self, message):
		self.message = message

# The exception thrown when a bad trigger was passed to IRC.addEventHook().
class TriggerNotFoundError(IRCError):
	def __init__(self, message):
		super().__init__(message)

class NotAnEventError(IRCError):
	def __init__(self, message):
		super().__init__(message)

class IRCEvent:
	def __init__(self):
		self.eventName = 'Event'

class IRCQuitEvent(IRCEvent):
	def __init__(self):
		self.eventName = 'QuitEvent'

# The IRC client class. Handles most of the stuff, including to responding to PINGs.
class IRC:
	irc = socket.socket()

	# A list of currently active callback functions.
	messageHooks = []

	nameRegex = re.compile(r':\w*!')
	msgRegex = re.compile(r'')

	recvBufSize = 2048

	eventQueue = []

	# Sets the socket
	def __init__(self):
		self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	# Adds an event hook given a trigger and the callback function.
	def addEventHook(self, trigger: str, hook: callable):
		try:
			triggers.index(trigger) # Searches for the given trigger in the list. This raises the ValueError!
			self.messageHooks.append(hook)
		except ValueError:
			raise TriggerNotFoundError(f'Trigger {trigger} does not exist!')
	
	# Queues an event.
	def queueEvent(self, event):
		if not isinstance(event, IRCEvent):
			raise NotAnEventError(f'{event} is not an instance of IRCEvent!')

		self.eventQueue += [event]
	
	# Processes all events in the event queue.
	def processEvents(self):
		for event in self.eventQueue:
			if isinstance(event, IRCQuitEvent):
				self.disconnect()
				self.disconnect = (lambda: True)
	
	# Looks for an instance of an event in the event queue.
	def isInEventQueue(self, event):
		if not isinstance(event, IRCEvent):
			raise NotAnEventError(f'{event} is not an instance of IRCEvent!')

		for e in self.eventQueue:
			if isinstance(e, type(event)):
				return True
		
		return False
	
	def setRateLimit(self, milliseconds: int):
		self.rateLimit = milliseconds

	# Sends a normal IRC message to the server.
	def send(self, msg):

		self.irc.send(msg + '\r\n')
	
	# Sends a private IRC message to a channel or user.
	def msg(self, recipient, msg):
		if self.rateLimit:
			sleep(self.rateLimit / 1000)
			
		self.irc.send(bytes('PRIVMSG ' + recipient + ' ' + msg + '\r\n', 'utf-8'))
	
	# Sets up the server connection.
	def server(self, server, port = 6667):
		print(f'Connecting to {server}:{port}...')
		self.irc.connect((server, port))
		print('Connected.')
	
	# Authenticate with the server
	def auth(self, nick, password = None):
		if password != None:
			self.irc.send(bytes(f'PASS {password}\r\n', 'utf-8'))
		
		self.irc.send(bytes(f'USER {nick} {nick} {nick} :{nick}\r\n', 'utf-8'))
		self.irc.send(bytes(f'NICK {nick}\r\n', 'utf-8'))
	
	# Joins a channel (Unused in this bot, and should never be used!)
	def join(self, channel):
		self.irc.send(bytes(f'JOIN {channel}\r\n', 'utf-8'))
		print(f'Joined {channel}.')
	
	# Sets the buffer size of the receive buffer.
	def setRecvBufSize(self, size: int):
		self.recvBufSize = size
	
	# Receives the text stream from the IRC server.
	# It will search for PINGs and automatically send a response PONG.
	def receive(self) -> list:
		try:
			text = self.irc.recv(self.recvBufSize)
		except KeyboardInterrupt:
			self.disconnect()
			quit()
		except:
			if self.isInEventQueue(IRCQuitEvent()):
				self.disconnect()
				quit()
			else:
				raise IRCError('Something went wrong with receiving. (Code 0x01)')

		self.processEvents()

		# Respond to PINGs
		if text.find(bytes('PING', 'utf-8')) != -1:
			self.irc.send(bytes('PONG ' + str(text.split()[1]) + '\r\n', 'utf-8'))
		
		splitText = str(text).split('\\n')
		
		lines = []

		for line in splitText:
			# Filtering, sometimes lines start with b' for some reason, which messes up the detection.
			if line.startswith('b\''):
				line = line[2:]
			if line.find('PRIVMSG') != -1:
				user = self.nameRegex.search(line).group(0)[1:][:-1]

				lines.append({'type': 'PRIVMSG', 'user': user, 'msg':  ''.join([ x for x in line.split(':') if line.index(x) > 1 ])})

				# Call all hooks
				for hook in self.messageHooks:
					hook(self, lines[-1])
			# TODO: Maybe add other types of messages aswell?

		return splitText
	
	# Disconnects from the server.
	def disconnect(self): #pylint: disable=method-hidden
		self.irc.send(bytes('QUIT\r\n', 'utf-8'))
		self.irc.close()
		print('Disconnected.')