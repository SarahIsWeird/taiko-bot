class ConfigError(Exception):
	pass

class MissingKeyError(ConfigError):
	def __init__(self, message):
		self.message = message

class MissingValueError(ConfigError):
	def __init__(self, message):
		self.message = message

class Config:
	options = {}
	path = ''

	def __init__(self, path: str):
		print(f'Loading configuration file ({path})...')

		try:
			configFile = open(path, 'rt')
			self.path = path

			row = 0
			for line in configFile:
				line = line.strip()
				row = row + 1

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
	
	def get(self, key):
		return self.options[key]