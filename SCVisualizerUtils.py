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


def overlayEnergyIMG(img, v_list_of_seams, h_list_of_seams):
	"img is numpy energy array"
	# overlay vertical seams
	i = 0
	for seam in v_list_of_seams:
		# replace img pixels with seam
		seam = seam + i 		# for each successive seam, increment seam[row] (i.e, the col) by 1
		img[range(len(seam)), seam] = 255
		i += 1

	# overlay horizontal seams
	i = 0	 						
	for seam in h_list_of_seams:
		seam = seam + i 		# for each successive seam, increment seam[col] (i.e, the row) by 1
		img[seam, range(len(seam))] = 255
		i += 1

def overlayIMG(sc, v_list_of_seams, h_list_of_seams):
	"overlay pixel img with seams"
	R = sc.image2render[:, :, 0]
	G = sc.image2render[:, :, 1]
	B = sc.image2render[:, :, 2]
	# overlay vertical seams
	for seam in v_list_of_seams:
		for row, col in enumerate(seam):
			R[row][col] = 255
			G[row][col] = 0
			B[row][col] = 0
		col += 1
		plt.imshow(sc.image2render)
		plt.show()
		
	# overlay horizontal seams	 						
	for seam in h_list_of_seams:
		for col, row in enumerate(seam):
			R[row][col] = 255
			G[row][col] = 0
			B[row][col] = 0
		row += 1
		plt.imshow(sc.image2render)
		plt.show()

# def overlayIMG(sc, v_list_of_seams, h_list_of_seams):
# 	"overlay pixel img with seams"
# 	R = sc.image2render[:, :, 0]
# 	G = sc.image2render[:, :, 1]
# 	B = sc.image2render[:, :, 2]
# 	# overlay vertical seams
# 	col = 0
# 	for seam in v_list_of_seams:
# 		R[range(len(seam)), seam + col] = 255
# 		G[range(len(seam)), seam + col] = 0
# 		B[range(len(seam)), seam + col] = 0
# 		col += 1
# 		plt.imshow(sc.image2render)
# 		plt.show()
		
# 	# overlay horizontal seams	 
# 	row = 0						
# 	for seam in h_list_of_seams:
# 		R[seam + row, range(len(seam))] = 255
# 		G[seam + row, range(len(seam))] = 0
# 		B[seam + row, range(len(seam))] = 0
# 		row += 1
# 		plt.imshow(sc.image2render)
# 		plt.show()

def writeIMG(img, width, height, filename, greyscale=False):
	"write img to a PNG file"
	w = png.Writer(width=width, height=height, greyscale=greyscale, bitdepth=8)
	with open(filename, 'wb') as f:
		print 'writing file...'
		w.write_array(f, img)






