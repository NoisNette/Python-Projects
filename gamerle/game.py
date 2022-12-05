from random import choice
from threading import Timer
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui

from igdb_helper import IGDBHelper
from image_helper import ImageHelper
from main_window import MainWindow

class Game:
	def __init__(self):
		self._igdbHelper = IGDBHelper()

		self.loadGames()

		self.initGui()

		self.score = 0
		self.newGame()


	# loads video-games
	def loadGames(self):
		path = 'games.txt'
		self._games = []

		with open(path, 'r') as f:
			lines = f.readlines()
			for line in lines:
				gameRaw = line.strip().split(';')
				valid = gameRaw[1].split(',')
				game = { 'id': gameRaw[0], 'name': valid[0], 'valid': gameRaw[1].split(',') }
				self._games.append(game)

	# initializes the app and window objects
	def initGui(self):
		self._app = QApplication([])
		self.window = MainWindow(self.submitGuess, self.skipRound)
		
		QtGui.QFontDatabase.addApplicationFont('fonts/Montserrat-Regular.ttf')
		QtGui.QFontDatabase.addApplicationFont('fonts/Montserrat-Bold.ttf')
		font = QtGui.QFont('Montserrat')
		self._app.setFont(font)
		self._app.setStyleSheet('* { color: white; }')

	# pops up a message to the window
	def popupMessage(self, msg):
		self.window.popupMessage(msg)
		t = Timer(2.0, self.window.hidePopup)
		t.start()

	# callback function for when the guess is submitted
	def submitGuess(self, guessRaw):
		guess = guessRaw.lower().strip()

		if not guess:
			self.popupMessage('Upiši ime igre!')
			return

		if guess in ([self.game['name']] + self.game['valid']):
			self.score += 1
			self.window.setScore(self.score)
			self.window.updateImage(ImageHelper.toImageQt(self.game['img']))

			t = Timer(2, self.newGame)
			t.start()
		
		else:
			self.tries -= 1
			self.window.setTries(self.tries)
			img = ImageHelper.getBlurredImage(self.game['img'], self.tries-1)
			self.window.updateImage(ImageHelper.toImageQt(img))
			self.window.clearInput()

		if self.tries == 0:
			self.popupMessage(f'Ime igre: {self.game["name"].upper()}')
			self.newGame()

	# callback function for when the current round is skipped
	def skipRound(self):
		self.newGame()

	# chooses a new *non-used* video-game to guess
	def chooseNewGame(self):
		game = choice(self._games)
		tryAgain = True
		while tryAgain:
			try:
				coverUrl = self._igdbHelper.getCoverUrl(game['id'])
				img = ImageHelper.getImage(coverUrl)
				tryAgain = False
			except KeyError or IndexError:
				tryAgain = True

		self.game = { 'name': game['name'], 'valid': game['valid'], 'img': img }

	# remove game from list of available games
	def removeGame(self):
		gameName = self.game['name']
		self._games = [game for game in self._games if game['name'] != gameName]

	# starts another round with a new video-game
	def newGame(self):
		if len(self._games) == 0:
			self.popupMessage('IGRA ZAVRŠENA')
			return

		self.chooseNewGame()
		self.removeGame()

		img = ImageHelper.getBlurredImage(self.game['img'], 3)
		self.window.newGame(ImageHelper.toImageQt(img))
		self.tries = 4
	
	# starts a new game
	def start(self):
		img = ImageHelper.getBlurredImage(self.game['img'], 3)
		self.window.newGame(ImageHelper.toImageQt(img))
		self.window.show()
		self._app.exec_()


if __name__ == '__main__':
	game = Game()
	game.start()