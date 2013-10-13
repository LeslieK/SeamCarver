import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import itertools

import argparse, png, array
from readPNG_2 import Picture
#from SeamCarverLib import SeamCarver
import SeamCarverLib
import SCVisualizerUtils
from copy import copy


parser = argparse.ArgumentParser()
parser.add_argument("filename", help="filename of image", type=str)
parser.add_argument("colsToRemove", help="number of rows to remove from image", type=int)
parser.add_argument("rowsToRemove", help="number of cols to remove from image", type=int)
args = parser.parse_args()

print "build energy array for {}".format(args.filename)
pic = Picture(args.filename)

print "create seam carver"
sc = SeamCarverLib.SeamCarver(pic)
print "finished seam carver, {}x{}".format(sc.width(), sc.height())

num_cols = args.colsToRemove
num_rows = args.rowsToRemove

width = sc.width()
height = sc.height()

vertical_seams = []
horizontal_seams = []

print 'show original image: {} x {}'.format(sc.width(), sc.height())
plt.imshow(sc.image2render)
plt.show()

print 'show greyscale energy'
energyIMG = SCVisualizerUtils.toGreyscale(sc)
plt.savefig("energyArrayGreyscale.png")
plt.imshow(energyIMG, cmap=plt.cm.Greys_r)
plt.show()

print "start finding vertical seam"
# print sc._R
# print
while num_cols > 0:
	#print
	s = sc.findVerticalSeam()
	#SCVisualizerUtils.printVerticalSeam(sc)
	#print
	sc.removeVerticalSeam(s)
	# print sc._R
	# print
	#SCVisualizerUtils.printVerticalSeam(sc)
	vertical_seams.append(s)  		# [ [v_seam], [v_seam], ...]
	num_cols -= 1

print "start finding horizontal seam"
# print sc._R
while num_rows > 0:
	#print
	s = sc.findHorizontalSeam()
	#SCVisualizerUtils.printHorizontalSeam(sc)
	#print
	sc.removeHorizontalSeam(s)
	# print sc._R
	# print
	#SCVisualizerUtils.printHorizontalSeam(sc)
	horizontal_seams.append(s)  	# [ [h_seam], [h_seam], ...]
	num_rows -= 1

print "show resized image"
# make image from R, G, B
resized_img = np.array(range(sc.width()*sc.height()*sc._num_channels), dtype=np.int16).reshape(sc.height(), sc.width(), sc._num_channels)
resized_img[:, :, 0] = sc._R[:, :]
resized_img[:, :, 1] = sc._G[:, :]
resized_img[:, :, 2] = sc._B[:, :]
plt.imshow(resized_img.astype(np.uint8))
plt.savefig("TESTresizedimg.png")
plt.show()

#print 'write reduced color img (no overlay), {}x{}'.format(sc.width(), sc.height())
#SCVisualizerUtils.writeIMG(sc._img, sc.width(), sc.height(), "TEST_color_nooverlay.png", greyscale=False)
# # convert png image to numpy array; in ipython notebook, display image with imshow(<np_array>)
# npREDIMG = mpimg.imread("TEST_color_nooverlay.png")

print 'start color img overlay'
SCVisualizerUtils.overlayIMG(sc, vertical_seams, horizontal_seams)

# print 'write color image with overlay'
# SCVisualizerUtils.writeIMG(pixIMG, width, height, "TEST_color.png", greyscale=False)
# npOVIMG = mpimg.imread("TEST_color.png")

# print 'start energy img overlay'
# SCVisualizerUtils.overlayEnergyIMG(npENERGYIMG, width, vertical_seams, horizontal_seams)

# print 'write energy image with overlay'
# SCVisualizerUtils.writeIMG(energyIMG, width, height, "TEST_energy.png", greyscale=True)
# npENERGYIMG = mpimg.imread("TEST_energy.png")



