import math
import numpy as np
from PIL import Image
from scipy.fftpack import dct, idct

def dct2Transform(matrix):
	dct = []
	m = len(matrix)
	n = len(matrix[0])
	for i in range(m):
		dct.append([None for _ in range(n)])

	for i in range(m):
		for j in range(n):

			if (i == 0):
				ci = 1 / (m ** 0.5)
			else:
				ci = (2 / m) ** 0.5
			if (j == 0):
				cj = 1 / (n ** 0.5)
			else:
				cj = (2 / n) ** 0.5

			sum = 0
			for k in range(m):
				for l in range(n):

					dct1 = matrix[k][l] * math.cos((2 * k + 1) * i * math.pi / (
						2 * m)) * math.cos((2 * l + 1) * j * math.pi / (2 * n))
					sum = sum + dct1

			dct[i][j] = ci * cj * sum
	return dct

def create_blocks(image, block_size):
   height, width = image.shape[:2]
   padded_height = int(np.ceil(height / block_size) * block_size)
   padded_width = int(np.ceil(width / block_size) * block_size)
   
   padded_image = np.zeros((padded_height, padded_width))
   padded_image[:height, :width] = image
   
   num_blocks_h = padded_height // block_size
   num_blocks_w = padded_width // block_size
   
   blocks = np.split(padded_image, num_blocks_h, axis = 0)
   blocks = [np.split(block, num_blocks_w, axis=1) for block in blocks]
   blocks = np.array(blocks)
   return blocks

def run(im, F, d):
   im = im.convert("L")
   im = np.array(im)
   rows, cols = im.shape
   F_square_subdivision = create_blocks(im, F)

   DCT_computations = []
   for r in F_square_subdivision:
      for block in r:
         res = dct(dct(block.T, norm='ortho').T, norm='ortho')
         for k in range(len(res)):
               for l in range(len(res)):
                  if k+l >= d:
                     res[k][l] = 0
         res = idct(idct(res.T, norm = 'ortho').T, norm = 'ortho')
         res = res.clip(0, 255)
         res = np.round(res).astype(int)
         DCT_computations.append(res)
   indice_riga = 0
   indice_colonna = 0
   padded_height = int(np.ceil(rows / F) * F)
   padded_width = int(np.ceil(cols / F) * F)
   DCT_matrix = np.zeros((padded_height, padded_width))

   for blocco in DCT_computations:
      DCT_matrix[indice_riga:indice_riga+F, indice_colonna:indice_colonna+F] = blocco
      indice_colonna += F
      if indice_colonna == padded_width:
         indice_colonna = 0
         indice_riga += F

   #plt.imshow(DCT_matrix, interpolation='nearest', cmap=cm.Greys_r)
   #plt.show()
   res = Image.fromarray(DCT_matrix)
   res = res.convert("L")
   return res