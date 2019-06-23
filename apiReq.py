import urllib.request, json, config

class API():
	apiUrl = 'https://osu.ppy.sh/api/'

	def __init__(self, conf: config.Config):
		self.apiKey = conf.get('apiKey')

	def getBeatmapJson(self, id: int):
		response = urllib.request.urlopen(f'{self.apiUrl}get_beatmaps?k={self.apiKey}&b={id}')
		return response.read().decode('utf-8')

	def getBeatmap(self, id: int):
		return json.loads(self.getBeatmapJson(id))