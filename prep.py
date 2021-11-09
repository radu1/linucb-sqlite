import sys
from numpy import asarray, dot, identity, outer
from numpy.linalg import inv


N = int(sys.argv[1])
K = int(sys.argv[2])


# x = the arms = a subset of movies from
# https://github.com/anatole33/LinUCB-secure/blob/master/extract_movie_lens/Movies3.txt 
x = [list(map(float, line.strip().split())) for line in open("linucb-movielens/Movies3.txt").readlines()[:K]]

# theta = A random user from
# https://github.com/anatole33/LinUCB-secure/blob/master/extract_movie_lens/Users3.txt
theta = [0.71956295, 0.14697917, 0.2017453]

d = len(theta)
gamma = 0.01
delta = 0.001

# https://proceedings.neurips.cc/paper/2011/file/e1d5be1c7f2f456670de3d53c7b54f4a-Paper.pdf
# bounded zero-mean noise lying in an interval of length at most 2R
# R = 0.01 => noise in [-0.01, 0.01]
R = 0.01

L = 0
for arm in x:
  arm = asarray(arm)
  temp_norm = arm.dot(arm)
  if temp_norm > L:
    L = temp_norm

i = 0
A = gamma * identity(d) + outer(x[i], x[i])
A_inv = inv(A).tolist()

f = open("data.py", "w")
f.write ("x = " + str(x) + "\n")
f.write ("d = " + str(d) + "\n")
f.write ("N = " + str(N) + "\n")
f.write ("K = " + str(K) + "\n")
f.write ("theta = " + str(theta) + "\n")
f.write ("gamma = " + str(gamma) + "\n")
f.write ("delta = " + str(delta) + "\n")
f.write ("R = " + str(R) + "\n")
f.write ("L = " + str(L) + "\n")
f.write ("A_inv = " + str(A_inv) + "\n")
f.close()


f = open("data.sql", "w")
f.write("insert into input values (%d, %d, %d, %f, %f, %f, %f);\n\n" % (d, N, K, gamma, delta, R, L))

f.write("insert into theta values ")
for i in range(d):
  f.write ("(%i, %f)" % (i, theta[i]))
  if i == d-1:
    f.write(";\n\n")
  else:
    f.write(", ")


def matrix_to_sql (f, matrix, name):
  f.write("insert into %s values\n" % (name))
  for i in range(len(matrix)):
    for j in range(len(matrix[i])):
      f.write("\t(%d, %d, %f)" % (i, j, matrix[i][j]))
      if i == len(matrix)-1 and j == len(matrix[i])-1:
        f.write(";\n")
      else:
        f.write(",")
    f.write("\n")


matrix_to_sql(f, x, "x");
matrix_to_sql(f, A_inv, "A_inv");

f.close()



