import requests
from bs4 import BeautifulSoup

class GameGenerator:
	@staticmethod
	def generateGrid():
		url = 'https://www.sudokuweb.org/'
		res = requests.get(url)
		soup = BeautifulSoup(res.content, 'html.parser')

		table = soup.find(lambda tag: tag.name == 'table')
		rows = table.findAll(lambda tag: tag.name == 'tr')

		grid = [[0 for _ in range(9)] for _ in range(9)]

		for i, row in enumerate(rows):
			cells = row.findAll(lambda tag: tag.name == 'td')
			for j, cell in enumerate(cells):
				span = cell.span
				grid[i][j] = (int(span.text), 'true' in span['class'])

		return grid