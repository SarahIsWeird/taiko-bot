import urllib.request, json 
from . import config
from . import pp

# The API class enabling calls to the osu! API.
# For more info on this, please refer to the GitHub wiki for the osu! API linked in the README.md file.
class API():
	# The osu! API url
	apiUrl = 'https://osu.ppy.sh/api/'

	# Sets the config key.
	def __init__(self, conf: config.Config):
		self.apiKey = conf.get('apiKey')

	# Gets the JSON as a string with all information for a given beatmap.
	def getBeatmapJson(self, id: int, mods = pp.mods['noMod']):
		if not mods == pp.mods['DoubleTime']: # Mods that don't change the difficulty make the API return '0' for a request.
			mods = pp.mods['noMod']			  # NoMod doesn't have this behaviour, though.

		response = urllib.request.urlopen(f'{self.apiUrl}get_beatmaps?k={self.apiKey}&b={id}&mods={mods}')
		return response.read().decode('utf-8')

	# Same as getBeatmapJson(), but converts the string to a python JSON object for easier use.
	def getBeatmap(self, id: int, mods = pp.mods['noMod']):
		return json.loads(self.getBeatmapJson(id, mods))
	
	# Gets the JSON as a string with all information of the last play(s) of a given player.
	def getUserRecentJson(self, user: str or int, limit: int = 1):
		if isinstance(user, str):
			userType = 'string'
		else:
			userType = 'id'

		response = urllib.request.urlopen(f'{self.apiUrl}get_user_recent?k={self.apiKey}&u={user}&m=1&limit={limit}&type={userType}')
		return response.read().decode('utf-8')
	
	def getUserRecent(self, user: str or int, limit: int = 1):
		return json.loads(self.getUserRecentJson(user, limit))