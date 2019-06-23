import socket, re

triggers = ['PRIVMSG']

class IRCError(Exception):
	pass

class TriggerNotFoundError(IRCError):
	def __init__(self, message):
		self.message = message

class IRC:
	irc = socket.socket()

	messageHooks = []

	nameRegex = re.compile(r':\w*!')
	msgRegex = re.compile(r'')

	def __init__(self):
		self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	def addEventHook(self, trigger: str, hook: callable):
		try:
			triggers.index(trigger)
			self.messageHooks.append(hook)
		except ValueError:
			raise TriggerNotFoundError(f'Trigger {trigger} does not exist!')
	
	def send(self, msg):
		self.irc.send(msg + '\r\n')
	
	def msg(self, recipient, msg):
		self.irc.send(bytes('PRIVMSG ' + recipient + ' ' + msg + '\r\n', 'utf-8'))
	
	def server(self, server, port = 6667):
		print(f'Connecting to {server}:{port}...')
		self.irc.connect((server, port))
		print('Connected.')
	
	def auth(self, nick, password = None):
		if password != None:
			self.irc.send(bytes(f'PASS {password}\r\n', 'utf-8'))
		
		self.irc.send(bytes(f'USER {nick} {nick} {nick} :{nick}\r\n', 'utf-8'))
		self.irc.send(bytes(f'NICK {nick}\r\n', 'utf-8'))
	
	def join(self, channel):
		self.irc.send(bytes(f'JOIN {channel}\r\n', 'utf-8'))
		print(f'Joined {channel}.')
	
	def receive(self) -> list:
		text = self.irc.recv(2048)

		if text.find(bytes('PING', 'utf-8')) != -1:
			self.irc.send(bytes('PONG ' + str(text.split()[1]) + '\r\n', 'utf-8'))
		
		splitText = str(text).split('\\n')
		
		lines = []

		for line in splitText:
			if line.startswith('b\''):
				line = line[2:]
			if line.find('PRIVMSG') != -1:
				user = self.nameRegex.search(line).group(0)[1:][:-1]

				lines.append({'type': 'PRIVMSG', 'user': user, 'msg':  ''.join([ x for x in line.split(':') if line.index(x) > 1 ])})

				for hook in self.messageHooks:
					hook(self, lines[-1])
			# TODO: Maybe add other types of messages aswell?

		return splitText
	
	def disconnect(self):
		self.irc.send(bytes('QUIT\r\n', 'utf-8'))
		self.irc.close()