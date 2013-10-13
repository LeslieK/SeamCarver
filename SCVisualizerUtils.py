import png, collections

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

def printVerticalSeam(sc):
	"vertical seam is a list of cols"
	seam = sc.findVerticalSeam()
	totalSeamEnergy = 0
	for row in range(sc.height()):
		for col in range(sc.width()):
			lmarker = ' '
			rmarker = ' '
			if col == seam[row]:
				lmarker = '['
				rmarker = ']'
				totalSeamEnergy += sc.energy(col, row)
			print '{:s}{:>6d}{:s}'.format(lmarker, sc.energy(col, row), rmarker),
		print
	print "\nTotal seam energy: {:d}".format(totalSeamEnergy)


def printHorizontalSeam(sc):
	"horizontal seam is a list of rows"
	seam = sc.findHorizontalSeam()
	totalSeamEnergy = 0
	for row in range(sc.height()):
		for col in range(sc.width()):
			lmarker = ' '
			rmarker = ' '
			if row == seam[col]:
				lmarker = '['
				rmarker = ']'
				totalSeamEnergy += sc.energy(col, row)
			print '{:s}{:>6d}{:s}'.format(lmarker, sc.energy(col, row), rmarker),
		print
	print "\nTotal seam energy: {:d}".format(totalSeamEnergy) 

def printVerticalSeamEnergy(sc):
	"vertical seam is a list of cols"
	seam = sc.findVerticalSeam()
	totalSeamEnergy = 0
	for row in range(sc.height()):
		for col in range(sc.width()):
			if col == seam[row]:
				totalSeamEnergy += sc.energy(col, row)
	print "\nTotal seam energy: {:d}".format(totalSeamEnergy)

def printHorizontalSeamEnergy(sc):
	"horizontal seam is a list of rows"
	seam = sc.findHorizontalSeam()
	totalSeamEnergy = 0
	for row in range(sc.height()):
		for col in range(sc.width()):
			if row == seam[col]:
				totalSeamEnergy += sc.energy(col, row)
	print "\nTotal seam energy: {:d}".format(totalSeamEnergy)


def distToArray(sc):
	"displays distTo in matrix format"
	print "sc._distTo array\n"
	for r in range(sc.height()):
		for c in range(sc.width()):
			print '{:>8d}'.format(sc._distTo[r * sc.width() + c]),
		print

def toGreyscale(sc):
	"return greyscale img of energy array"
	maxv = np.max(sc._energy)
	return np.round(sc._energy/ float(maxv) * 255)
	# in notebook: 
	# imshow(e, cmap=pyplot.cm.binary)

#e = SCVisualizerUtils.toGreyscale(sc)
#plt.savefig("energyArrayGreyscale.png")
#plt.imshow(e, cmap=pyplot.cm.Greys_r)
#plt.show()



def writeGrayscaleToPNG(sc, filename_out, seam=None, horizontal=True):
	"converts sc.energy array to png image of grayscale values"
	
	normal_energy = [int(round(x * 255)) for x in _normalize(sc._energy)]
	if seam:
		# write energy png with seam overlay
		_RED = 255
		if horizontal:
			# horizontal seam
			for col, row in enumerate(seam):
				index = row * sc.width() + col
				normal_energy[index] = _RED
		else:
			# vertical seam
			for row, col in enumerate(seam):
				index = row * sc.width() + col
				normal_energy[index] = _RED
	# write png 
	w = png.Writer(width=sc.width(), height=sc.height(), bitdepth=8, greyscale=True)
	with open(filename_out, 'wb') as f:
		w.write_array(f, normal_energy)


def overlayEnergyIMG(img, width, v_list_of_seams, h_list_of_seams):
	"img is a numpy array"
	# overlay vertical seams
	for seam in v_list_of_seams:
		# replace img pixels with seam
		img[range(len(seam)), seam] = 255
		col += 1
		# plot seam on canvas
		# show canvas

	# overlay horizontal seams	 						
	for seam in h_list_of_seams:
		img[seam, range(len(seam))] = 255
		row += 1
		# draw seam on canvas
		# show canvas

def overlayIMG(sc, v_list_of_seams, h_list_of_seams):
	"overlay pixel img with seams"
	R = sc._copyIMG[:, 0::sc._num_channels]
	G = sc._copyIMG[:, 1::sc._num_channels]
	B = sc._copyIMG[:, 2::sc._num_channels]
	# overlay vertical seams
	for seam in v_list_of_seams:
		for row, col in enumerate(seam):
			R[row][col] = 255
			G[row][col] = 0
			B[row][col] = 0
		col += 1
		plt.imshow(sc._copyIMG)
		plt.show()
		
	# overlay horizontal seams	 						
	for seam in h_list_of_seams:
		for col, row in enumerate(seam):
			R[row][col] = 255
			G[row][col] = 0
			B[row][col] = 0
		row += 1
		plt.imshow(sc._copyIMG)
		plt.show()

# def overlayIMG(img, width, v_list_of_seams, h_list_of_seams):
# 	"overlay pixel img with seams"
# 	# overlay vertical seams
# 	for seam in v_list_of_seams:
# 		for row, col in enumerate(seam):
# 			index = row * width + col
# 			# replace img pixels with seam 
# 			img[index*3] = 255
# 			img[index*3+1] = 0
# 			img[index*3+2] = 0
# 		col += 1	

# 	# overlay horizontal seams	 						
# 	for seam in h_list_of_seams:
# 		for col, row in enumerate(seam):
# 			index = row * width + col
# 			# replace img pixels with seam 
# 			#print"row: {}  col: {}  index: {}".format(row, col, index)
# 			img[index*3] = 255
# 			img[index*3+1] = 0
# 			img[index*3+2] = 0
# 		row += 1
# 		# draw seam on canvas
# 		# show canvas

def writeIMG(img, width, height, filename, greyscale=False):
	"write img to a PNG file"
	w = png.Writer(width=width, height=height, greyscale=greyscale, bitdepth=8)
	with open(filename, 'wb') as f:
		print 'writing file...'
		w.write_array(f, img)


def toDictionary(seam):
	"converts a seam to a dictionary; k = seam value, v = index in seam"
	d = collections.defaultdict(list)
	for i in range(len(seam)):
		d[seam[i]].append(i)
	return d






