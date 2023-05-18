# This code reduces the size of the source image for commonStyle icons and balloonTemplates.
from PIL import Image

image_path = input("Введите полный путь к фотографии: ")
img = Image.open(image_path)
image_commonStyle = img.resize((50, 42))
image_balloonTemplate = img.resize((500, 375))
image_commonStyle.save('image_commonStyle.jpg')
image_balloonTemplate.save('image_balloonTemplate.jpg')
