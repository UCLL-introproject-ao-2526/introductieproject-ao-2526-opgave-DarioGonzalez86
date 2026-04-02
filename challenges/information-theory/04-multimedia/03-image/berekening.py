from PIL import Image

path = "br.jpg"
img = Image.open(path)
width, height = img.size

print(f"Resolutie: {width} x {height}")
