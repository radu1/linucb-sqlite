import matplotlib.pyplot as plt
import warnings
warnings.simplefilter("ignore")

f = open ("results_varyN_varyK.txt")
lines = []
for l in f.readlines():
  l = l.strip().split(' ')
  lines.append([int(l[0]), int(l[1]), float(l[2]), float(l[3])])

N_vals = range(5, 86, 20)
K_vals = range(5, 86, 20)

markers = ['o', 'p', '.', 'x', 'd']

for N in list(reversed(N_vals)):
  y_vals_P = []
  y_vals_S = []
  for line in lines:
    if line[0] == N:
      y_vals_P.append(line[2])
      y_vals_S.append(line[3])

  plt.plot(K_vals, y_vals_P, marker=markers[N_vals.index(N)], color='blue', label= "N=%d, Python" % (N))
  plt.plot(K_vals, y_vals_S, marker=markers[N_vals.index(N)], color='red', label= "N=%d, SQLite" % (N))

plt.gca().xaxis.set_ticks(K_vals)
plt.gca().yaxis.set_ticks([0, 0.25, 0.5, 0.75, 1])
plt.title("Fixing the bugdet N, Varying the number of arms K")
plt.xlabel("Number of arms K")
plt.ylabel("Time (seconds)")
plt.legend(loc='upper left')
plt.savefig("plots/plot_varyK.pdf")

plt.clf()

for K in list(reversed(K_vals)):
  y_vals_P = []
  y_vals_S = []
  for line in lines:
    if line[1] == K:
      y_vals_P.append(line[2])
      y_vals_S.append(line[3])

  plt.plot(N_vals, y_vals_P, marker=markers[K_vals.index(K)], color='blue', label= "K=%d, Python" % (K))
  plt.plot(N_vals, y_vals_S, marker=markers[K_vals.index(K)], color='red', label= "K=%d, SQLite" % (K))

plt.gca().xaxis.set_ticks(N_vals)
plt.gca().yaxis.set_ticks([0, 0.25, 0.5, 0.75, 1])
plt.title("Fixing the number of arms K, Varying the bugdet N")
plt.xlabel("Bugdet N")
plt.ylabel("Time (seconds)")
plt.legend(loc='upper left')
plt.savefig("plots/plot_varyN.pdf")

