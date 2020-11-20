import requests
from PIL import Image

url = 'https://startup.likelion.org/img/likelion_logo.png'
r = requests.get(url, stream=True).raw


img = Image.open(r)
img.show()
# img.save('src.png')
print(img.get_format_mimetype)


