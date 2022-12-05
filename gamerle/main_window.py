from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class MainWindow(QMainWindow):
	def __init__(self, submitGuess, skipRound, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.setWindowTitle('Gamerle')
		self.setStyleSheet('background: #252525')

		self._width = 800
		self._height = 800
		self.setFixedSize(self._width, self._height)
		self._coverImgHeight = 500

		self.submitGuess = submitGuess
		self.skipRound = skipRound

		# center the window
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

		# create and style score label
		self.scoreLabel = QLabel('Bodovi: 0', self)
		self.scoreLabel.setStyleSheet(
			'''
			font-size: 18pt;
			min-width: 150px;
			'''
		)
		self.scoreLabel.adjustSize()
		self.scoreLabel.move(10, 10)

		# create and style skip button
		self.skipBtn = QPushButton('Preskoči', self)
		self.skipBtn.setStyleSheet(
			'''
			font-size: 18pt;
			min-width: 115px;
			'''
		)
		self.skipBtn.adjustSize()
		self.skipBtn.move(self._width - self.skipBtn.width() - 10, 10)
		self.skipBtn.clicked.connect(self.skipRound)

		# create and style game title label
		self.titleLabel = QLabel('GAMERLE', self)
		self.titleLabel.setStyleSheet(
			'''
			font-size: 32pt;
			font-weight: bold;
			min-width: 250px;
			'''
		)
		self.titleLabel.setAlignment(Qt.AlignCenter)
		self.titleLabel.adjustSize()
		self.titleLabel.move(self._width//2 - self.titleLabel.width()//2, 10)

		# create cover image widget with default loading image as the placeholder
		self.coverLabel = QLabel(self)
		pixmap = QPixmap('loading.png').scaledToHeight(self._coverImgHeight)
		self.coverLabel.setPixmap(pixmap)
		self.coverLabel.resize(pixmap.width(), self._coverImgHeight)
		self.coverLabel.move(self._width//2 - self.coverLabel.width()//2, 100)

		# create and style popup label
		self.popupLabel = QLabel('Točno!', self)
		self.popupLabel.setStyleSheet(
			f'''
			font-size: 18pt;
			font-weight: bold;
			background-color: transparent;
			min-width: {self._width};
			'''
		)
		self.popupLabel.setAlignment(Qt.AlignCenter)
		self.popupLabel.adjustSize()
		self.popupLabel.move(self._width//2 - self.popupLabel.width()//2, self._height//2 - self.popupLabel.height()//2 - 50)
		shadow = QGraphicsDropShadowEffect()
		shadow.setBlurRadius(15)
		self.popupLabel.setGraphicsEffect(shadow)
		self.popupLabel.setHidden(True)

		# create and style tries left label
		self.triesLabel = QLabel('Broj pokušaja: 4', self)
		self.triesLabel.setStyleSheet('font-size: 16pt;')
		self.triesLabel.adjustSize()
		self.triesLabel.move(self._width//2 - self.triesLabel.width()//2, 630)

		# create and style input field
		self.input = QLineEdit(self)
		self.input.setStyleSheet(
			'''
			font-size: 18pt;
			padding: 5px;
			min-width: 500px;
			'''
		)
		self.input.setAlignment(Qt.AlignCenter)
		self.input.adjustSize()
		self.input.move(self._width//2 - self.input.width()//2, 670)
		self.input.setPlaceholderText('Upiši ime igre')
		self.input.returnPressed.connect(self.onKeyPressedReturn)

		# create and style submit button
		self.submitBtn = QPushButton('Unesi', self)
		self.submitBtn.setStyleSheet(
			'''
			font-size: 18pt;
			padding: 5px;
			min-width: 100px;
			'''
		)
		self.submitBtn.adjustSize()
		self.submitBtn.move(self._width//2 - self.submitBtn.width()//2, 730)
		self.submitBtn.clicked.connect(self.onKeyPressedReturn)
	

	
	# fires when the Return (Enter) key is pressed while focused on the input widget
	def onKeyPressedReturn(self):
		self.submitGuess(self.input.text())

	# updates the displayed score
	def setScore(self, score):
		self.scoreLabel.setText(f'Bodovi: {score}')
		self.scoreLabel.adjustSize()

	# updates the displayed tries left
	def setTries(self, tries):
		self.triesLabel.setText(f'Broj pokušaja: {tries}')
		self.triesLabel.adjustSize()

	# clears the text in the input field
	def clearInput(self):
		self.input.clear()

	# updates the image shown 
	def updateImage(self, img): # type(img) == PIL.ImageQt
		pixmap = QPixmap.fromImage(img).scaledToHeight(self._coverImgHeight)
		self.coverLabel.setPixmap(pixmap)
		self.coverLabel.resize(pixmap.width(), self._coverImgHeight)
		self.coverLabel.move(self._width//2 - self.coverLabel.width()//2, 100)

	# popups a message to the screen
	def popupMessage(self, msg):
		self.popupLabel.setText(msg)
		self.popupLabel.setHidden(False)	

	# hides the popup message
	def hidePopup(self):
		self.popupLabel.setHidden(True)	
	
	# resets widgets to start a new game
	def newGame(self, img):
		self.updateImage(img)
		self.setTries(4)
		self.clearInput()
		self.input.setFocus()

if __name__ == '__main__':
	app = QApplication([])
	app.setStyleSheet('* { color: white; }')
	win = MainWindow(lambda x: print(x), lambda: print('skip'))
	win.show()
	app.exec_()