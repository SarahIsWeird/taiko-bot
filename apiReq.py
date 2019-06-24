import urllib.request, json, config

# The API class enabling calls to the osu! API.
# For more info on this, please refer to the GitHub wiki for the osu! API linked in the README.md file.
class API():
	# The osu! API url
	apiUrl = 'https://osu.ppy.sh/api/'

	# Sets the config key.
	def __init__(self, conf: config.Config):
		self.apiKey = conf.get('apiKey')

	# Gets the JSON as a string with all information for a given beatmap.
	def getBeatmapJson(self, id: int):
		response = urllib.request.urlopen(f'{self.apiUrl}get_beatmaps?k={self.apiKey}&b={id}')
		return response.read().decode('utf-8')

	# Same as getBeatmapJson(), but converts the string to a python JSON object for easier use.
	def getBeatmap(self, id: int):
		return json.loads(self.getBeatmapJson(id))