import sys
import math
import matrix
import pickle
#globals()['something'] = 'bob'

def main():
	read_file(sys.argv[1])

def read_file(lines):
	global frames,currentframe
	f = open(lines,'r')
	l = f.readlines();
	while(not done):
		print "Frame " + str(currentframe)
		for line in l:
			doline(line)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def doline(line):
	global filename
	global triangle_matrix, trans_matrix
	global xmax, xmin, ymax, ymin
	global xpix, ypix, grid
	l = line.split()
	if len(l) == 0:
		return
	if l[0] == "#":
		pass
	if l[0] == "identity":
		trans_matrix = matrix.create_identity_matrix()
	elif l[0] == "move":
		trans_matrix = move(is_var(l[1]), is_var(l[2]), is_var(l[3]), trans_matrix)
	elif l[0] == "scale":
		trans_matrix = scale(is_var(l[1]), is_var(l[2]), is_var(l[3]), trans_matrix)
	elif l[0] == "rotate-x":
		trans_matrix = rotate_x(is_var(l[1]), trans_matrix)
	elif l[0] == "rotate-y":
		trans_matrix = rotate_y(is_var(l[1]), trans_matrix)
	elif l[0] == "rotate-z":
		trans_matrix = rotate_z(is_var(l[1]), trans_matrix)
	elif l[0] == "screen":
		xmin = int(l[1])
		ymin = int(l[2])
		xmax = int(l[3])
		ymax = int(l[4])
	elif l[0] == "pixels":
		xpix = int(l[1])
		ypix = int(l[2])
		grid = [[[0, 0, 0] for i in range(xpix)] for j in range(ypix)]
	elif l[0] == "render-parallel":
		render_parallel()
	elif l[0] == "render-perspective-cyclops":
		render_perspective_cyclops(float(l[1]),float(l[2]),float(l[3]))
	elif l[0] == "render-perspective-stereo":
		render_perspective_stereo(float(l[1]), float(l[2]), float(l[3]), float(l[4]), float(l[5]), float(l[6]))
	elif l[0] == "sphere-t":
		sphere_t(is_var(l[1]),is_var(l[2]),is_var(l[3]),is_var(l[4]), is_var(l[5]), is_var(l[6]), is_var(l[7]), is_var(l[8]), is_var(l[9]))
	elif l[0] == "box-t":
		box_t(is_var(l[1]), is_var(l[2]), is_var(l[3]), is_var(l[4]), is_var(l[5]), is_var(l[6]), is_var(l[7]), is_var(l[8]), is_var(l[9]))
	elif l[0] == "clear-triangles":
		triangle_matrix = []
	elif l[0] == "clear-pixels":
		grid = [[[0, 0, 0] for i in range(xpix)] for j in range(ypix)]
	elif l[0] == "files":
		filename = l[1]
	elif l[0] == "frames":
		setFrames(int(l[1]), int(l[2]))
	elif l[0] == 'vary':
		vary(l[1], float(l[2]), float(l[3]), float(l[4]), float(l[5]))
	elif l[0] == "end":
		write_file()
		triangle_matrix = []
		grid = [[[0, 0, 0] for i in range(xpix)] for j in range(ypix)]
		trans_matrix = matrix.create_identity_matrix()
	elif l[0] == "save":
		save(l[1])
	elif l[0] == "restore":
		restore(l[1])

def setFrames(start, end):
	global frames, currentframe, done
	if currentframe == -1:
		frames = end
		currentframe = start
	else:
		currentframe += 1
		if currentframe == frames:
			done = True
		vary

def draw_triangle(x1, y1, x2, y2, x3, y3):
	draw_line(x1, y1, x2, y2)
	draw_line(x2, y2, x3, y3)
	draw_line(x1, y1, x3, y3)

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
	try:
		pixel = grid[y][x]
		pixel[0] = r
		pixel[1] = g
		pixel[2] = b
	except:
		print "Out of range"

def move(dx, dy, dz, m):
	new_matrix = matrix.create_identity_matrix()
	new_matrix[0][3] = dx
	new_matrix[1][3] = dy
	new_matrix[2][3] = dz
	return matrix.multiply_matrices(m, new_matrix)

def scale(sx, sy, sz, m):
	new_matrix = matrix.create_identity_matrix()
	new_matrix[0][0] = sx
	new_matrix[1][1] = sy
	new_matrix[2][2] = sz
	return matrix.multiply_matrices(m, new_matrix)

def write_file():
	global grid
	global filename
	global r, g, b
	global xpix, ypix
	f = open(filename + str(currentframe).zfill(3) + '.ppm', 'w')
	f.write('P3 %i %i 255 ' % (xpix, ypix))
	for y in range(ypix):
		for x in range(xpix):
			f.write("%i %i %i " % (grid[y][x][0], grid[y][x][1], grid[y][x][2]))
	f.close()

def render_parallel():
	render_perspective_cyclops(0, 0, 10)

def convert_points(matrix):
	global xmax, xmin, ymin, ymax
	global xpix, ypix
	for point in matrix:
		point[0] = int(round(xpix * (point[0] - xmin)/(abs(xmin) + abs(xmax))))
		point[1] = int(round(ypix * (ymax - point[1])/(abs(ymin) + abs(ymax))))
	return matrix

def rotate_x(degrees, m):
	new_matrix = matrix.create_identity_matrix()
	new_matrix[1][1] = math.cos(math.radians(degrees))
	new_matrix[1][2] = 0 - math.sin(math.radians(degrees))
	new_matrix[2][1] = math.sin(math.radians(degrees))
	new_matrix[2][2] = math.cos(math.radians(degrees))
	return matrix.multiply_matrices(m, new_matrix)

def rotate_y(degrees, m):
	new_matrix = matrix.create_identity_matrix()
	new_matrix[0][0] = math.cos(math.radians(degrees))
	new_matrix[0][2] = math.sin(math.radians(degrees))
	new_matrix[2][0] = 0 - math.sin(math.radians(degrees))
	new_matrix[2][2] = math.cos(math.radians(degrees))
	return matrix.multiply_matrices(m, new_matrix)

def rotate_z(degrees, m):
	new_matrix = matrix.create_identity_matrix()
	new_matrix[0][0] = math.cos(math.radians(degrees))
	new_matrix[0][1] = 0 - math.sin(math.radians(degrees))
	new_matrix[1][0] = math.sin(math.radians(degrees))
	new_matrix[1][1] = math.cos(math.radians(degrees))
	return matrix.multiply_matrices(m, new_matrix)

def transform(trans_m, m):
	for i in range(len(m)):
		x = matrix.multiply_point_matrix(trans_m, m[i])
		m[i] = x
	return m

def is_var(var):
	if var in varys:
		return varys[var]['current']
	else:
		return float(var)

def box_t(sx, sy, sz, rx, ry, rz, mx, my, mz):
	global triangle_matrix
	p0 = [.5, .5, .5, 1]
	p1 = [.5, -.5, .5, 1]
	p2 = [-.5, -.5, .5, 1]
	p3 = [-.5, .5, .5, 1]
	p4 = [.5, .5, -.5, 1]
	p5 = [.5, -.5, -.5, 1]
	p6 = [-.5, -.5, -.5, 1]
	p7 = [-.5, .5,  -.5, 1]
	box_triangles = []
	box_triangles = add_triangle(p0, p2, p1, box_triangles)
	box_triangles = add_triangle(p3, p2, p0, box_triangles)
	box_triangles = add_triangle(p7, p6, p2, box_triangles)
	box_triangles = add_triangle(p7, p2, p3, box_triangles)
	box_triangles = add_triangle(p0, p1, p5, box_triangles)
	box_triangles = add_triangle(p0, p5, p4, box_triangles)
	box_triangles = add_triangle(p7, p5, p6, box_triangles)
	box_triangles = add_triangle(p4, p5, p7, box_triangles)
	box_triangles = add_triangle(p4, p7, p3, box_triangles)
	box_triangles = add_triangle(p3, p0, p4, box_triangles)
	box_triangles = add_triangle(p2, p6, p5, box_triangles)
	box_triangles = add_triangle(p1, p2, p5, box_triangles)
	box_triangles = transform(scale(sx, sy, sz, matrix.create_identity_matrix()), box_triangles)
	box_triangles = transform(rotate_x(rx, matrix.create_identity_matrix()), box_triangles)
	box_triangles = transform(rotate_y(ry, matrix.create_identity_matrix()), box_triangles)
	box_triangles = transform(rotate_z(rz, matrix.create_identity_matrix()), box_triangles)
	box_triangles = transform(move(mx, my, mz, matrix.create_identity_matrix()), box_triangles)
	box_triangles = transform(trans_matrix, box_triangles)
	triangle_matrix = triangle_matrix + box_triangles

def add_triangle(p1, p2, p3, l):
	l.append(p1[:])
	l.append(p2[:])
	l.append(p3[:])
	return l

def sphere_t(sx, sy, sz, rx, ry, rz, mx, my, mz):
	global triangle_matrix
	sphere_matrix = []
	circlematrix = []
	theta = 0
	while theta <= 2 * math.pi:
		circleset = []
		phi = 0
		while phi <= 2 * math.pi:
			pointlist = []
			pointlist.append(math.sin(theta)*math.cos(phi))
			pointlist.append(math.sin(theta)*math.sin(phi))
			pointlist.append(math.cos(theta))
			pointlist.append(1)
			circleset.append(pointlist)
			phi += 2 * math.pi / CIRCLELINES
		circlematrix.append(circleset)
		theta += math.pi * 2 / CIRCLELINES
	for i in range(CIRCLELINES-1):
		for j in range(CIRCLELINES-1):
			if j != 0:
				sphere_matrix = add_triangle(circlematrix[i][j], circlematrix[i+1][j], circlematrix[i+1][j+1], sphere_matrix)
				sphere_matrix = add_triangle(circlematrix[i][j], circlematrix[i][j+1], circlematrix[i+1][j], sphere_matrix)
	sphere_matrix = transform(scale(sx, sy, sz, matrix.create_identity_matrix()), sphere_matrix)
	sphere_matrix = transform(rotate_x(rx, matrix.create_identity_matrix()), sphere_matrix)
	sphere_matrix = transform(rotate_y(ry, matrix.create_identity_matrix()), sphere_matrix)
	sphere_matrix = transform(rotate_z(rz, matrix.create_identity_matrix()), sphere_matrix)
	sphere_matrix = transform(move(mx, my, mz, matrix.create_identity_matrix()), sphere_matrix)
	sphere_matrix = transform(trans_matrix, sphere_matrix)
	triangle_matrix = triangle_matrix + sphere_matrix

def render_perspective_cyclops(ex, ey, ez):
	new_matrix = isvisible(ex, ey, ez, triangle_matrix)
	for i in range(len(new_matrix)):
		new_matrix[i][0] = ex-(ez * (new_matrix[i][0] - ex) / (new_matrix[i][2] - ez))
		new_matrix[i][1] = ey-(ez * (new_matrix[i][1] - ey) / (new_matrix[i][2] - ez))
	new_matrix = convert_points(new_matrix)
	for i in range(0, len(new_matrix), 3):
		p1 = new_matrix[i]
		p2 = new_matrix[i+1]
		p3 = new_matrix[i+2]
		draw_triangle(p1[0],p1[1], p2[0], p2[1], p3[0], p3[1])

def isvisible(ex, ey, ez, tmat):
	m = []
	for i in range(0, len(tmat), 3):
		p1 = tmat[i]
		p2 = tmat[i+1]
		p3 = tmat[i+2]
		t1 = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]]
		t2 = [p3[0] - p2[0], p3[1] - p2[1], p3[2] - p2[2]]
		s = [p1[0] - ex, p1[1] - ey, p1[2] - ez]
		d = dot_product(s, cross_product(t1, t2))
		if d < 0:
			m.append(tmat[i][:])
			m.append(tmat[i+1][:])
			m.append(tmat[i+2][:])
	return m

def render_perspective_stereo(ex1, ey1, ez1, ex2, ey2, ez2):
	global r, g, b
	g = 0
	b = 0
	render_perspective_cyclops(ex1, ey1, ez1)
	r = 0
	g = 127
	b = 127
	render_perspective_cyclops(ex2, ey2, ez2)

def dot_product(l1, l2):
	ans = 0
	for i in range(len(l1)):
		ans += l1[i]*l2[i]
	return ans

def cross_product(l1, l2):
	return_matrix = []
	return_matrix.append(l1[1]*l2[2] - l1[2]*l2[1])
	return_matrix.append(l1[2]*l2[0] - l1[0]*l2[2])
	return_matrix.append(l1[0]*l2[1] - l1[1]*l2[0])
	return return_matrix

def vary(var, start, end, sframe, eframe):
	global varys
	if not var in varys:
		varys[var] = {}
		varys[var]['current'] = start
		varys[var]['end'] = end
		varys[var]['sframe'] = sframe
		varys[var]['eframe'] = eframe
		varys[var]['rate'] = (end - start) / (eframe - sframe)
	else:
		if currentframe >= start and currentframe <= end:
			varys[var]['current'] += varys[var]['rate']

def save(name):
	with open(name, 'wb') as f:
		pickle.dump(trans_matrix, f)

def restore(name):
	global trans_matrix
	with open(name, 'rb') as f:
		trans_matrix = pickle.load(f)

######

CIRCLELINES = 20

######

r = 255
g = 255
b = 255
filename = "default"
trans_matrix = matrix.create_identity_matrix()
triangle_matrix = []
xmax = 0
xmin = 0
ymax = 0
ymin = 0
grid = 0
xpix = 0
ypix = 0
frames = 0
currentframe = -1
varys = {}
done = False

######

if __name__ == '__main__':
	main()