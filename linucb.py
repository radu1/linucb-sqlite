from math import sqrt, log
from numpy import asarray, dot, outer, identity, matmul, array, transpose
from numpy.random import uniform
from numpy.linalg import inv

from data import x, d, N, K, theta, gamma, delta, R, L, A_inv

# function that returns a reward = scalar product + noise
def pull(i):
  return dot(x[i], theta) + uniform(-R, R)


# print the "real" rewards associated to each arm
#for i in range(K):
#  print (i, dot(x[i], theta)) 


# Initialization: Pull an arm and initialize variables
i = 0
r = pull(i)
s = r
b = r * asarray(x[i])

#print ("time_step  pulled_arm  reward")
#print ("0          %d           %f" % (i, r))

# Exploration-Exploitation: At each round, pull an arm and update variables
for t in range(1, N):
  theta_hat = matmul(A_inv, b)
  omega = R * sqrt(d * log((1+t*L*L/gamma)/delta)) + sqrt(gamma)*log(t)
  
  B_max = None
  for i in range(K):
    B_current = dot(x[i], theta_hat) + omega * sqrt(matmul(matmul(x[i], A_inv), x[i]))
    if B_max == None or B_max < B_current:
      B_max = B_current
      argmax = i
  
  r = pull (argmax)
  s += r
  b = b + r * asarray(x[argmax])
#  print ("%d          %d           %f" % (t, argmax, r))

    
  # https://en.wikipedia.org/wiki/Sherman%E2%80%93Morrison_formula
  u=array([x[argmax]]).T
  A_inv = A_inv - matmul(matmul(matmul(A_inv, u), transpose(u)), A_inv) / (1 + matmul(matmul(transpose(u), A_inv), u))
  
  # check Sherman-Morrison is correctly implemented
  #print(A_inv)
  #A = A + outer(x[argmax], x[argmax])
  #print(inv(A))
 
#print ("Cumulative reward", s)


