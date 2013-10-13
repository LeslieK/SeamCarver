from decimal import Decimal
_INF = Decimal('infinity')
_SENTINEL = -1
_BORDER_ENERGY = 195705
import numpy as np

class SeamCarver(object):
	"removes seams from an image"
	def __init__(self, picture):
		self._img = picture.image_3d
		self._height = picture.num_rows
		self._width = picture.num_cols
		self._num_channels = picture.num_channels
		self._energy = picture.energyArray

		self.image2render = picture.image_3d.copy().astype(np.uint8)

		#self._copyIMG = picture.image_3d.copy()
		#self._copyIMG = np.empty_like(self._energy)
		#self._copyIMG[:] = self._energy

		self._R = self._img[:, :, 0]
		self._G = self._img[:, :, 1]
		self._B = self._img[:, :, 2]

		self._copyENERGY = self._energy.copy()
		# self._copyENERGY = np.empty_like(self._energy)
		# self._copyENERGY[:] = self._energy
		
		# virtual source and sink vertices
		self._num_pixels = self._height * self._width
		self._source = self._num_pixels
		self._sink = self._source + 1

		# graph data structures
		# self._edgeTo = [_SENTINEL for _ in range(self._num_pixels + 2)]	# add 2 for source, sink pixels
		# self._distTo = [_INF for _ in range(self._num_pixels + 2)]
		self._edgeTo = []
		self._distTo = []


	def width(self):
		return self._width

	def height(self):
		return self._height

	def energy(self, col, row):
		"return energy of pixel in (col, row)"
		if self._isValid(col, row):
			return self._energy[row][col]

	def findVerticalSeam(self):
		"return vertical seam in image"
		# vertical seam = sequence of cols; seam[0] is col of row 0
		# row-indexed seam
		seam = [-1 for _ in range(self._height)]
		self._buildGraph()
		row = self._height - 1
		v = self._edgeTo[self._sink]
		while (v != self._source):
			seam[row] = v % self._width  # seam[row] = col
			v = self._edgeTo[v]
			row -= 1
		self._edgeTo = []
		self._distTo = []
		return np.array(seam)

	def findHorizontalSeam(self):
		"return horizontal seam in image"
		self._exchDims()
		self._energy = self._energy.transpose()
		# seam is an numpy array
		seam = self.findVerticalSeam()
		self._energy = self._energy.transpose()
		self._exchDims()
		return seam

	def removeVerticalSeam(self, seam):
		"remove vertical seam of pixels from image"
		_CH = self._num_channels

		for row in range(len(seam)):
			# shift left
			self._R[row, range(seam[row], self._width - 1)] = self._R[row, range(seam[row] + 1, self._width)]
			self._G[row, range(seam[row], self._width - 1)] = self._G[row, range(seam[row] + 1, self._width)]
			self._B[row, range(seam[row], self._width - 1)] = self._B[row, range(seam[row] + 1, self._width)]
			self._energy[row, range(seam[row], self._width - 1)] = self._energy[row, range(seam[row] + 1, self._width)]

		# update image dimension, number of pixels
		self._width = self._width - 1
		self._num_pixels = self._width * self._height
		self._source = self._num_pixels
		self._sink = self._source + 1
		#self._img = self._img[:, 0:-self._num_channels]
		self._R = self._R[:, 0:-1]
		self._G = self._G[:, 0:-1]
		self._B = self._B[:, 0:-1]
		self._energy = self._energy[:, 0:-1]

		# update energy array
		self._updateEnergy(seam)

	def _updateEnergy(self, seam):
		'''re-calculate energy values for vertical seam'''
		self._energy[:, [0, self._width - 1]] = _BORDER_ENERGY
		self._energy[[0, self._height-1], :] = _BORDER_ENERGY
		for row in range(len(seam)):
			# find grad of pixel in sea position (row i, col seam[i])
			if row == 0 or row == self._height-1:
				continue
			for col in [seam[row], seam[row] - 1]:
				if col == 0 or col == (self._width - 1):
					continue
				left = col - 1
				right = col + 1
				gradH = (self._R[row][left] - self._R[row][right])**2 + (self._G[row][left] - self._G[row][right])**2 + (self._B[row][left] - self._B[row][right])**2
				gradV = (self._R[row-1][col] - self._R[row+1][col])**2 + (self._G[row-1][col] - self._G[row+1][col])**2 + (self._B[row-1][col] - self._B[row+1][col])**2
				self._energy[row][col] = gradH + gradV


	def removeHorizontalSeam(self, seam):
		"remove horizontal seam of pixels"
		self._exchDims()
		self._R = self._R.transpose()
		self._G = self._G.transpose()
		self._B = self._B.transpose()
		self._energy = self._energy.transpose()
		self._img = self._img.transpose()

		self.removeVerticalSeam(seam)

		self._R = self._R.transpose()
		self._G = self._G.transpose()
		self._B = self._B.transpose()
		self._energy = self._energy.transpose()
		self._img = self._img.transpose()
		self._exchDims()
					

	# def _onEdge(self, col, row):
	# 	"True if pixel is on left, top, or right edge"
	# 	return col == 0 or col == self._width - 1 or row == 0

	def _exchDims(self):
		"exchange self._width and self._height"
		swap = self._width
		self._width = self._height
		self._height = swap

	# def _toLinear(self, col, row):
	# 	"converts pixel from (col, row) to single index"
	# 	if self._isValid(col, row):
	# 		return row * self._width + col

	def _toGrid(self, num):
		"converts pixel from single index to (col, row)"
		if self._isValid(num):
			row = num / self._width
			col = num % self._width
			return (col, row)

	def _isValid(self, col, row=None):
		if row is None:
			if (col < 0) or (col > self._width * self._height - 1):
				return False
			else:
				return True
		else:
			if (col < 0) or (col > self._width-1) or (row < 0) or (row > self._height-1):
				return False
			else:
				return True

	def _buildGraph(self):
		"pixels are nodes; edges define precedence constraints in a seam"
		# graph data structures
		self._edgeTo = [_SENTINEL for _ in range(self._num_pixels + 2)]	# add 2 for source, sink pixels
		self._distTo = [_INF for _ in range(self._num_pixels + 2)]
		
		# for row 0 pixels: distTo[] is 0; edgeTo[] is _source vertex 
		for i in range(0, self._width):
			self._distTo[i] = 0
			self._edgeTo[i] = self._source
		# distTo[] is 0 for source pixel
		self._distTo[self._source] = 0

		# for each vertex (pixel), calculate edgeTo[], distTo[]
		# start at row 1
		for v in range(self._width, self._num_pixels):
			if (v % self._width == 0):
				# pixel is on left edge
				self._edgeTodistTo(v, edgeL=True)
			elif (v % self._width == self._width - 1):
				# pixel is on right edge
				self._edgeTodistTo(v, edgeR=True)
			else:
				self._edgeTodistTo(v)
		# edgeTo[sink] is vertex in last row with min energy
		index, min_energy = min(enumerate(self._distTo[self._num_pixels - self._width:self._num_pixels]), key=lambda (x, y): y)
		self._distTo[self._sink] = min_energy
		self._edgeTo[self._sink] = (self._height - 1) * self._width + index



	def _edgeTodistTo(self, v, edgeL=False, edgeR=False):
		# calculates pixel connected to v (edgeTo[v]) with min energy (distTo[v])
		if edgeL:
			# left edge
			vC = v - self._width
			vRD = v - self._width + 1
			vLU = vC
		elif edgeR:
			# right edge
			vLU = v - self._width - 1
			vC = v - self._width
			vRD = vC
		else:
			# pixels connect to v
			vLU = v - self._width - 1
			vC = v - self._width
			vRD = v - self._width + 1
		
		(colU, rowU) = self._toGrid(vLU)
		(colC, rowC) = self._toGrid(vC)
		(colD, rowD) = self._toGrid(vRD)
		
		# read energy directly from energy array
		eLU = self._energy[rowU][colU]
		eC = self._energy[rowC][colC]
		eRD = self._energy[rowD][colD]
		#print (eLU, vLU), (eC, vC), (eRD, vRD)
		# find min distance and its associated vertex
		dist, from_vertex = min((self._distTo[vLU] + eLU, vLU), (self._distTo[vC] + eC, vC), (self._distTo[vRD] + eRD, vRD))
		#e, vertex = min([(eC, vC), (eLU, vLU), (eRD, vRD)])
		self._edgeTo[v] = from_vertex
		self._distTo[v] = dist





		

