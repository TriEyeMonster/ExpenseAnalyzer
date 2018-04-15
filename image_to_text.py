import pytesseract
from PIL import Image

image = Image.open('/Users/wguan17/Desktop/123.jpg')
image.load()
text = pytesseract.image_to_string(image)
print text