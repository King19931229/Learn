from PIL import Image
im = Image.open("test.jpg")
pix = im.load()
width = im.size[0]
height = im.size[1]

bit_width = 1
band_count = (1 << bit_width) - 1
band_width = int(255 / band_count)

def find_closest_palette_color(rgb):
	new_rgb = tuple([max(min(int( round(e / band_width)) * band_width, 255), 0) for e in rgb])
	return new_rgb

def get_pixel(im, x, y):
	if x < 0 or x >= width or y < 0 or y >= height:
		return (0,0,0)
	r,g,b = im.getpixel((x, y))
	return (r,g,b)

ref_im = im.copy()

for y in range(height):
	for x in range(width):
		old_rgb = get_pixel(im, x, y)
		new_rgb = find_closest_palette_color(old_rgb)
		ref_im.putpixel((x, y), (new_rgb[0], new_rgb[1], new_rgb[2]))

for y in range(height):
	for x in range(width):
		old_rgb = get_pixel(im, x, y)
		new_rgb = find_closest_palette_color(old_rgb)
		quant_error = (old_rgb[0] - new_rgb[0], old_rgb[1] - new_rgb[1], old_rgb[2] - new_rgb[2])

		im.putpixel((x, y), (new_rgb[0], new_rgb[1], new_rgb[2]))

		if x + 1 < width:
			old_rgb = get_pixel(im, x + 1, y)
			new_rgb = (	int(old_rgb[0] + quant_error[0] * 7.0 / 16.0),\
						int(old_rgb[1] + quant_error[1] * 7.0 / 16.0),\
						int(old_rgb[2] + quant_error[2] * 7.0 / 16.0))
			im.putpixel((x + 1, y), (new_rgb[0], new_rgb[1], new_rgb[2]))

		if x - 1 >= 0 and y + 1 < height:
			old_rgb = get_pixel(im, x - 1, y + 1)
			new_rgb = (	int(old_rgb[0] + quant_error[0] * 3.0 / 16.0),\
						int(old_rgb[1] + quant_error[1] * 3.0 / 16.0),\
						int(old_rgb[2] + quant_error[2] * 3.0 / 16.0))
			im.putpixel((x - 1, y + 1), (new_rgb[0], new_rgb[1], new_rgb[2]))

		if y + 1 < height:
			old_rgb = get_pixel(im, x, y + 1)
			new_rgb = (	int(old_rgb[0] + quant_error[0] * 5.0 / 16.0),\
						int(old_rgb[1] + quant_error[1] * 5.0 / 16.0),\
						int(old_rgb[2] + quant_error[2] * 5.0 / 16.0))
			im.putpixel((x, y + 1), (new_rgb[0], new_rgb[1], new_rgb[2]))

		if x + 1 < width and y + 1 < height:
			old_rgb = get_pixel(im, x + 1, y + 1)
			new_rgb = (	int(old_rgb[0] + quant_error[0] * 1.0 / 16.0),\
						int(old_rgb[1] + quant_error[1] * 1.0 / 16.0),\
						int(old_rgb[2] + quant_error[2] * 1.0 / 16.0))
			im.putpixel((x + 1, y + 1), (new_rgb[0], new_rgb[1], new_rgb[2]))

ref_im.save("ref.bmp")
im.save("result.bmp")