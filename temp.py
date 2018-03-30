from PIL import Image

im = Image.open("img2_label0_rnd1.jpg")

im1 = im.copy()

im.show()
im1.rotate(45).show()

size = 128, 128

im2 = Image.alpha_composite(im1, im)


im2.save(file + ".thumbnail", "JPEG")