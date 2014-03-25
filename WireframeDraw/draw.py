import sys
import math
import matrix
from copy import deepcopy

def main():
	read_file(sys.argv[1])

def read_file(lines):
	global filename
	global edge_matrix, trans_matrix
	global xmax, xmin, ymax, ymin
	global xpix, ypix, grid
	f = open(lines,'r')
	for line in f.readlines():
		l = line.split()
		print l[0]
		if l[0] == "#":
			pass
		if l[0] == "line":
			add_to_edge_matrix(float(l[1]),float(l[2]),float(l[3]),float(l[4]),float(l[5]),float(l[6]))
		if l[0] == "identity":
			trans_matrix = matrix.create_identity_matrix()
		if l[0] == "move":
			move(float(l[1]), float(l[2]), float(l[3]))
		if l[0] == "scale":
			scale(float(l[1]), float(l[2]), float(l[3]))
		if l[0] == "rotate-x":
			rotate_x(int(l[1]))
		if l[0] == "rotate-y":
			rotate_y(int(l[1]))
		if l[0] == "rotate-z":
			rotate_z(int(l[1]))
		if l[0] == "screen":
			xmin = int(l[1])
			ymin = int(l[2])
			xmax = int(l[3])
			ymax = int(l[4])
		if l[0] == "pixels":
			xpix = int(l[1])
			ypix = int(l[2])
			grid = [[[0, 0, 0] for i in range(xpix)] for j in range(ypix)]
		if l[0] == "transform":
			transform()
		if l[0] == "render-parallel":
			render_parallel()
		if l[0] == "render-perspective-cyclops":
			render_perspective_cyclops(float(l[1]),float(l[2]),float(l[3]))
		if l[0] == "render-perspective-stereo":
			render_perspective_stereo(float(l[1]), float(l[2]), float(l[3]), float(l[4]), float(l[5]), float(l[6]))
		if l[0] == "sphere":
			sphere(float(l[1]),float(l[2]),float(l[3]),float(l[4]))
		if l[0] == "pixels":
			pass
		if l[0] == "clear-edges":
			pass
		if l[0] == "clear-pixels":
			pass
		if l[0] == "file":
			filename = l[1]
		if l[0] == "end":
			write_file()

def draw_line(x1,y1,x2,y2):
	if x1 == x2 and y1 == y2:
		draw(x1,y1)
	if abs(x1-x2) >= abs(y1-y2):
		x_major_case(x1, y1, x2, y2)
	else:
		y_major_case(x1, y1, x2, y2)

def x_major_case(x1, y1, x2, y2):
	if x1 > x2:
		x1, y1, x2, y2 = x2, y2, x1, y1
	if y2 >= y1:
		up = True
	else:
		up = False							
	delta_y = abs(y2-y1)
	delta_x = abs(x2-x1)
	acc = int(delta_x/2)
	draw (x1,y1)
	while (x1 < x2):
		x1 += 1
		acc += delta_y
		if acc >= delta_x:
			if up:
				y1 += 1
			else:
				y1 -= 1
			acc -= delta_x
		draw(x1, y1)

def y_major_case(x1, y1, x2, y2):
	if y1 > y2:
		x1, y1, x2, y2 = x2, y2, x1, y1
	if x2 >= x1:
		up = True
	else:
		up = False
	delta_y = abs(y2-y1)
	delta_x = abs(x2-x1)
	acc = int(delta_y/2)
	draw (x1,y1)
	while (y1 < y2):
		y1 += 1
		acc += delta_x
		if acc >= delta_y:
			if up:
				x1 += 1
			else:
				x1 -= 1
			acc -= delta_y
		draw(x1, y1)

def draw(x, y):
	global grid, r, g, b
	pixel = grid[y][x]
	# if pixel[0] != 0 or pixel[1] != 0 or pixel[2] != 0:
	# 	pixel[0] = 255
	# 	pixel[1] = 255
	# 	pixel[2] = 255
	# else:
	pixel[0] = r
	pixel[1] = g
	pixel[2] = b

def add_to_edge_matrix(x1, y1, z1, x2, y2, z2):
	global edge_matrix
	edge_matrix.append([x1, y1, z1, 1])
	edge_matrix.append([x2, y2, z2, 1])

def move(dx, dy, dz):
	global trans_matrix
	new_matrix = matrix.create_identity_matrix()
	new_matrix[0][3] = dx
	new_matrix[1][3] = dy
	new_matrix[2][3] = dz
	trans_matrix = matrix.multiply_matrices(new_matrix, trans_matrix)

def scale(sx, sy, sz):
	global trans_matrix
	new_matrix = matrix.create_identity_matrix()
	new_matrix[0][0] = sx
	new_matrix[1][1] = sy
	new_matrix[2][2] = sz
	trans_matrix = matrix.multiply_matrices(new_matrix, trans_matrix)

def transform():
	global edge_matrix, trans_matrix
	for i in range(len(edge_matrix)):
		edge_matrix[i] = matrix.multiply_point_matrix(trans_matrix, edge_matrix[i])

def write_file():
	global grid
	global filename
	global r, g, b
	global xpix, ypix
	f = open(filename, 'w')
	f.write('P3 %i %i 255 ' % (xpix, ypix))
	for y in range(ypix):
		for x in range(xpix):
			f.write("%i %i %i " % (grid[y][x][0], grid[y][x][1], grid[y][x][2]))
	f.close()

def render_parallel():
	global edge_matrix
	global grid
	new_matrix = convert_points(deepcopy(edge_matrix))
	for i in range(0, len(new_matrix), 2):
		p1 = new_matrix[i]
		p2 = new_matrix[i+1]
		draw_line(p1[0],p1[1], p2[0], p2[1])

def convert_points(matrix):
	global xmax, xmin, ymin, ymax
	global xpix, ypix
	for point in matrix:
		point[0] = int(round(xpix * (point[0] - xmin)/(abs(xmin) + abs(xmax))))
		point[1] = int(round(ypix * (ymax - point[1])/(abs(ymin) + abs(ymax))))
	return matrix

def rotate_x(degrees):
	global trans_matrix
	new_matrix = matrix.create_identity_matrix()
	new_matrix[1][1] = math.cos(math.radians(degrees))
	new_matrix[1][2] = 0 - math.sin(math.radians(degrees))
	new_matrix[2][1] = math.sin(math.radians(degrees))
	new_matrix[2][2] = math.cos(math.radians(degrees))
	trans_matrix = matrix.multiply_matrices(new_matrix, trans_matrix)

def rotate_y(degrees):
	global trans_matrix
	new_matrix = matrix.create_identity_matrix()
	new_matrix[0][0] = math.cos(math.radians(degrees))
	new_matrix[0][2] = math.sin(math.radians(degrees))
	new_matrix[2][0] = 0 - math.sin(math.radians(degrees))
	new_matrix[2][2] = math.cos(math.radians(degrees))
	trans_matrix = matrix.multiply_matrices(new_matrix, trans_matrix)

def rotate_z(degrees):
	global trans_matrix
	new_matrix = matrix.create_identity_matrix()
	new_matrix[0][0] = math.cos(math.radians(degrees))
	new_matrix[0][1] = 0 - math.sin(math.radians(degrees))
	new_matrix[1][0] = math.sin(math.radians(degrees))
	new_matrix[1][1] = math.cos(math.radians(degrees))
	trans_matrix = matrix.multiply_matrices(new_matrix,trans_matrix,)

def sphere(r, x, y, z):
	global edge_matrix
	circlematrix = []
	phi = 0
	while phi <= 2 * math.pi:
		circleset = []
		theta = 0
		while theta <= 2 * math.pi:
			pointlist = []
			pointlist.append(x + r*math.sin(theta)*math.cos(phi))
			pointlist.append(y + r*math.sin(theta)*math.sin(phi))
			pointlist.append(z + r*math.cos(theta))
			circleset.append(pointlist)
			theta += math.pi * 2 / CIRCLELINES
		circlematrix.append(circleset)
		phi += math.pi * 2 / CIRCLELINES
	for i in range(CIRCLELINES):
		for j in range(CIRCLELINES):
			if i != 0:
				add_to_edge_matrix(circlematrix[i][j][0], circlematrix[i][j][1], circlematrix[i][j][2],
								   circlematrix[i-1][j][0], circlematrix[i-1][j][1], circlematrix[i-1][j][2])
			if j != 0:
				add_to_edge_matrix(circlematrix[i][j][0], circlematrix[i][j][1], circlematrix[i][j][2],
								   circlematrix[i][j-1][0], circlematrix[i][j-1][1], circlematrix[i][j-1][2])

def render_perspective_cyclops(ex, ey, ez):
	new_matrix = deepcopy(edge_matrix)
	print edge_matrix
	for i in range(len(new_matrix)):
		new_matrix[i][0] = ex-(ez * (edge_matrix[i][0] - ex) / (edge_matrix[i][2] - ez))
		new_matrix[i][1] = ey-(ez * (edge_matrix[i][1] - ey) / (edge_matrix[i][2] - ez))
	print new_matrix
	new_matrix = convert_points(new_matrix)
	for i in range(0, len(new_matrix), 2):
		p1 = new_matrix[i]
		p2 = new_matrix[i+1]
		draw_line(p1[0],p1[1], p2[0], p2[1])

def render_perspective_stereo(ex1, ey1, ez1, ex2, ey2, ez2):
	global r, g, b
	g = 0
	b = 0
	render_perspective_cyclops(ex1, ey1, ez1)
	r = 0
	g = 127
	b = 127
	render_perspective_cyclops(ex2, ey2, ez2)

######

CIRCLELINES = 36

######

r = 255
g = 255
b = 255
filename = "default.ppm"
trans_matrix = matrix.create_matrix()
edge_matrix = []
xmax = 0
xmin = 0
ymax = 0
ymin = 0
grid = 0
xpix = 0
ypix = 0

######

if __name__ == '__main__':
	main()