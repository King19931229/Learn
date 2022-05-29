import random

arr = []
count = random.randint(1, 1024)

group_x_dim = 8
group_y_dim = 1
group_z_dim = 1

group_x_num = 0
group_y_num = 0
group_z_num = 0

global_ = []

def prepare(arr, count, group_count):
	for i in range(count):
		arr.append(random.randint(1, 100))

	right_sum = 0
	for i in range(count):
		right_sum += arr[i]
	
	for i in range(group_count):
		global_.append(0)

	print(right_sum, arr)

def algorithm_0(local_, gid, id):
	s = 1
	while(s < group_x_dim):
		for i in range(group_x_dim):
			if i % (2 * s) == 0 and i + s < count:
				local_[i] += local_[i + s]
		# sync
		s *= 2

	global_[gid] = local_[0]

def algorithm_1(local_, gid, id):
	s = 1
	while(s < group_x_dim):
		for i in range(int(group_x_dim / (s * 2))):
			id = 2 * i * s
			if id + s < group_x_dim:
				local_[id] += local_[id + s]
		# sync
		s *= 2

	global_[gid] = local_[0]

def algorithm_2(local_, gid, id):
	s = int(group_x_dim / 2)
	while(s >= 1):
		for i in range(group_x_dim):
			if i < s:
				local_[i] += local_[i + s]
		# sync
		s = int(s / 2)

	global_[gid] = local_[0]

def run(gx, gy, gz, x, y, z):
	gid = gx * group_y_num * group_z_num + gy * group_z_num + gz
	id = gid * group_x_dim * group_y_dim * group_z_dim + x * group_y_dim * group_z_dim + y * group_z_dim + z
	dx = gx * group_x_dim + x
	dy = gy * group_y_dim + y
	dz = gz * group_z_dim + z

	if x == 0 and y == 0 and z == 0:
		local_ = []
		for _tid in range(group_x_dim):
			if id + _tid < count:
				local_.append(arr[id + _tid])
			else:
				local_.append(0)
		algorithm_2(local_, gid, id)

def run_half(gx, gy, gz, x, y, z):
	gid = gx * group_y_num * group_z_num + gy * group_z_num + gz
	id = gid * group_x_dim * group_y_dim * group_z_dim + x * group_y_dim * group_z_dim + y * group_z_dim + z
	dx = gx * group_x_dim + x
	dy = gy * group_y_dim + y
	dz = gz * group_z_dim + z

	if x == 0 and y == 0 and z == 0:
		local_ = []
		for _tid in range(group_x_dim):
			idx = 2 * gid * group_x_dim + _tid
			if idx < count:
				local_.append(arr[idx])
			else:
				local_.append(0)
			if idx + group_x_dim < count:
				local_[_tid] += arr[idx + group_x_dim]

		algorithm_2(local_, gid, id)

def dispatch(x, y, z, run_func):
	global group_x_num, group_y_num, group_z_num
	group_x_num = x
	group_y_num = y
	group_z_num = z
	for i in range(group_x_num):
		for j in range(group_y_num):
			for k in range(group_z_num):
				for ii in range(group_x_dim):
					for jj in range(group_y_dim):
						for kk in range(group_z_dim):
							run_func(i, j, k, ii, jj, kk)

group_count = int((count + group_x_dim - 1) / group_x_dim)
# prepare(arr, count, group_count)
# dispatch(group_count, 1, 1, run)

group_count = int((group_count + 1) / 2)
prepare(arr, count, group_count)
dispatch(group_count, 1, 1, run_half)

sum = 0
for i in range(group_count):
	sum += global_[i]
print(sum)