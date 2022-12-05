import requests
from secret import *

class IGDBHelper:
	def __init__(self):
		self.acquireToken()
		self._baseUrl = 'https://api.igdb.com/v4/games'

	# fetches a new valid token from the api
	def acquireToken(self):
		body = {
			'client_id': CLIENT_ID,
			'client_secret': CLIENT_SECRET,
			'grant_type': 'client_credentials'
		}
		res = requests.post('https://id.twitch.tv/oauth2/token', body)
		keys = res.json()

		self._token = 'Bearer ' + keys['access_token']

		self._headers = {
			'Client-ID': CLIENT_ID,
			'Authorization': self._token
		}
	
	# returns a cover image url for a game with the given id
	def getCoverUrl(self, gameId):
		res = requests.post(
			self._baseUrl,
			headers=self._headers,
			data=f'fields cover.*; where id={gameId};'
		)

		data = res.json()
		imageId = data[0]['cover']['image_id']
		url = f'https://images.igdb.com/igdb/image/upload/t_1080p/{imageId}.jpg'

		return url

	# returns the name of the game with the specified id
	def getGameName(self, gameId):
		res = requests.post(
			self._baseUrl,
			headers=self._headers,
			data=f'fields name; where id = {gameId};'
		)

		data = res.json()
		name = data[0]['name']

		return name