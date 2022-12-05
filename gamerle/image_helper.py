from io import BytesIO
from PIL import Image
from PIL.ImageQt import ImageQt
import requests

class ImageHelper:
	# returns an Image object from a given web url
	@staticmethod
	def getImage(image_url):
		res = requests.get(image_url)
		img = Image.open(BytesIO(res.content))

		return img

	# returns a blurred version of the given image with variable blur amount
	@staticmethod
	def getBlurredImage(img, stage): # stage => 0-3 where 0 is least blurry and 3 most blurry
		if stage == 0:
			return img
			
		stages = [
			(img.width, img.height),
			(64, 64),
			(32, 32),
			(16, 16)
		]

		size = stages[stage]
		imgSmall = img.resize(size, resample=Image.BILINEAR)
		blurred = imgSmall.resize(img.size, Image.NEAREST)

		return blurred

	# converts an Image-type image to an ImageQt-type image
	@staticmethod
	def toImageQt(img):
		return ImageQt(img)