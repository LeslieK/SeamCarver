import png, itertools
import numpy as np


class Picture(object):
	"reads a png image from a filename"
	#BORDER_ENERGY = 195075
	BORDER_ENERGY = 195705
	
	
	def __init__(self, pngfilename):
		"reads in a .png image"
		_CH = 3		# number of channels (R,G,B = 3; R,G,B,A = 4)
		_r = png.Reader(filename=pngfilename)
		res = _r.asDirect()
	# 	res = (width, height, iterator-over-pixels, 
	# 	    	{'alpha': False, 'bitdepth': 8, greyscale': True,
	#        	'interlace': 0, 'planes': 1, size':(255, 1)})

		self.num_cols = res[0]
		self.num_rows = res[1]

		if res[3]['alpha']:
			_CH = 4

		self.num_channels = _CH

		# 2-d numpy array
		# boxed row, flat pixel; _CH = 3   [ [R,G,B, R,G,B, ..., R,G,B], ..., ]
		# boxed row, flat pixel; _CH = 4   [ [R,G,B,A, R,G,B,A, ..., R,G,B,A], ..., ]
		self.image_2d = np.vstack(itertools.imap(np.int16, res[2]))

		# 2-d numpy array, dtype = float
		self.energyArray = np.ndarray((self.num_rows, self.num_cols), dtype=np.long)

		# scratch energy array: scratchpad to do math operations (square, diff) to build energy array
		# width of _scratch does not include left/right boundary pixels
		_scratch = np.ndarray((2, (self.num_cols - 2) * _CH), dtype=np.int32)

		# set top and bot rows
		self.energyArray[[0, self.num_rows - 1], :] = Picture.BORDER_ENERGY
		self.energyArray[:, [0, self.num_cols - 1]] = Picture.BORDER_ENERGY
		
		# row 0 of image
		_row_prev = self.image_2d[0]
		if (self.num_rows == 1):
			return

		# row 1 of image
		_row_curr = self.image_2d[1]
		if (self.num_rows == 2):
			return
		
		# for images with more than 2 rows
		_curr = 1
		for _row_next in self.image_2d[2:]:
			"populate energy array"
			# calculate gradient of current row
			# store vertical diff in _scratch[0]
			_scratch[0] = (_row_prev - _row_next)[_CH:-_CH]	# drop border cols
			_scratch[0] = _scratch[0] ** 2
			
			# calculate horizontal diff in _scratch[1]
			_scratch[1] = _row_curr[2*_CH:] - _row_curr[:-2 * _CH] 
			_scratch[1] = _scratch[1] ** 2

			# add vertical and horizontal gradients
			_scratch[0] = _scratch[0] + _scratch[1]

			# BOR  RGB RGB BOR  _scratch[0]:  vert: deltaR^2, deltaG62, deltaB^2, ...
			#  0    1   2   3   
			# RBG  RGB RGB RGB  _scratch[1]   horiz: deltaR^2, deltaG62, deltaB^2, ...
			ecol = 1
			for j in range(0, len(_scratch[0]/_CH), _CH):
				self.energyArray[_curr][ecol] = sum(_scratch[0, [j, j+1, j+2]])
				ecol += 1
			_row_prev = _row_curr
			_row_curr = _row_next
			_curr += 1


