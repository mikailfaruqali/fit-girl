from PIL import Image, ImageDraw

# Create 256x256 icon with lightning bolt
img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Blue circle
draw.ellipse([20, 20, 236, 236], fill='#3498db')

# White lightning bolt
lightning = [(128, 60), (100, 128), (128, 128), (108, 196), (152, 112), (120, 112)]
draw.polygon(lightning, fill='white')

# Save as ICO
img.save('icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
print("✓ Icon created: icon.ico")
