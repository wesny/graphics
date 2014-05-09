def create_matrix(ncols = 4):
	return [[0.0 for j in range(4)] for i in range(ncols)]

def create_identity_matrix():
	matrix = create_matrix()
	for i in range(4):
		matrix[i][i] = 1.0
	return matrix

def multiply_matrices(m1,m2):
	product = [[0 for x in range(4)] for y in range(len(m2))]
	for row in range(4):
		for col in range(len(m2[0])):
			product[row][col] = (m1[row][0]*m2[0][col] + 
								 m1[row][1]*m2[1][col] + 
								 m1[row][2]*m2[2][col] + 
								 m1[row][3]*m2[3][col])
	return product

def multiply_point_matrix(m1,m2):
	print m1
	print m2
	product = [[0.0 for x in range(4)] for y in range(len(m2))]
	for row in range(4):
		product[row] = (m1[row][0]*m2[0] +
						m1[row][1]*m2[1] +
						m1[row][2]*m2[2] +
						m1[row][3]*m2[3])
	return product
