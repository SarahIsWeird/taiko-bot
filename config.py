# The base config exception class.
class ConfigError(Exception):
	pass

# The exception thrown when a line doesn't specify a key.
class MissingKeyError(ConfigError):
	def __init__(self, message):
		self.message = message

# The exception thrown when a line doesn't specify a value.
class MissingValueError(ConfigError):
	def __init__(self, message):
		self.message = message

# The config class.
class Config:
	options = {}
	path = ''

	saved = {}

	# Opens a config.
	def __init__(self, path: str):
		print(f'Loading configuration file ({path})...')

		try:
			configFile = open(path, 'rt')
			self.path = path

			row = 0
			for line in configFile:
				# Ignore leading or trailing whitespaces
				line = line.strip()
				row = row + 1

				# Ignore comments or empty lines
				if line.startswith('#') or line == '':
					continue

				split = line.split('=')

				key: str = split[0].strip()
				value: str = split[1].strip()

				if key == '' and value == '': # Skip lines only containing '='.
					continue
				elif key == '':
					raise MissingKeyError(f'Value {value} doesn\'t have a key! Line {row}: \'{line}\'')			
				elif value == '':
					raise MissingValueError(f'Key \'{key}\' doesn\'t have a value! Line {row}: \'{line}\'')
				
				# If the value is a string, remove the single/double quotes,
				if (value.startswith('"') and value.endswith('"')) or (value.startswith('\'') and value.endswith('\'')):
					value = value[1:][:-1]
				else: # else it's a number, so we convert it.
					value = int(value)

				self.options[key] = value
		
		except BaseException as error:
			print(f'Error loading the configuration file: {error}\nQuitting.')
			configFile.close()
			quit() # The config file is crucial for credentials,
				# hence we close the program in case of an exception.
	
	# Fetches a value given a key.
	def get(self, key):
		return self.options[key]
	
	def save(self, key, value):
		self.saved[key] = value
	
	def load(self, key):
		return self.saved[key]