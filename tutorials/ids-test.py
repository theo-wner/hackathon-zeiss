from PIL import Image
import requests
from io import BytesIO

url = 'http://169.254.75.124/camera/image'

response = requests.get(url, stream=True)

image_data = response.content

img = Image.open(BytesIO(image_data))

img.show()
