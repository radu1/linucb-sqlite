import sys
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter("ignore")

f = open ("results.txt")
lines = []
for l in f.readlines():
  l = l.strip().split(' ')
  lines.append([int(l[0]), int(l[1]), int(l[2]), float(l[3]), float(l[4])])

N_vals = range(int(sys.argv[1]), int(sys.argv[2])+1, int(sys.argv[3]))
K_vals = range(int(sys.argv[4]), int(sys.argv[5])+1, int(sys.argv[6]))
d_vals = range(int(sys.argv[7]), int(sys.argv[8])+1, int(sys.argv[9]))

markers = ['s', 'o', 'x', 'd']
colors = ["magenta", "green"]
font_size = 15
marker_size = 10


###############################
### Plot : Vary N
###############################
plt.rcParams.update({'font.size':font_size})
fixed_d = 4
for K in list(reversed(K_vals)):
  y_vals_P = []
  y_vals_S = []
  for line in lines:
    if line[1] == K and line[2] == fixed_d:
      y_vals_P.append(line[3])
      y_vals_S.append(line[4])
  plt.plot(N_vals, y_vals_P, marker=markers[K_vals.index(K)], markersize=marker_size, fillstyle='none', color=colors[0], label= "P, K=%d, d=%d" % (K, fixed_d), linestyle="--")
  plt.plot(N_vals, y_vals_S, marker=markers[K_vals.index(K)], markersize=marker_size, fillstyle='none', color=colors[1], label= "S, K=%d, d=%d" % (K, fixed_d))

plt.gca().xaxis.set_ticks(N_vals)
plt.title("Varying N for fixed K and d", fontsize=font_size)
plt.xlabel("Bugdet N")
plt.ylabel("Time (seconds)")
plt.legend(loc='upper left', ncol=2)
plt.tight_layout()
plt.savefig("plots/plot_varyN.pdf")
plt.clf()


###############################
### Plot : Vary K
###############################
plt.rcParams.update({'font.size':font_size})
fixed_d = 4
for N in list(reversed(N_vals)):
  y_vals_P = []
  y_vals_S = []
  for line in lines:
    if line[0] == N and line[2] == fixed_d:
      y_vals_P.append(line[3])
      y_vals_S.append(line[4])
  plt.plot(K_vals, y_vals_P, marker=markers[N_vals.index(N)], markersize=marker_size, fillstyle='none', color=colors[0], label= "P, N=%d, d=%d" % (N, fixed_d), linestyle="--")
  plt.plot(K_vals, y_vals_S, marker=markers[N_vals.index(N)], markersize=marker_size, fillstyle='none', color=colors[1], label= "S, N=%d, d=%d" % (N, fixed_d))
  
plt.gca().xaxis.set_ticks(K_vals)
plt.title("Varying K for fixed N and d", fontsize=font_size)
plt.xlabel("Number of arms K")
plt.ylabel("Time (seconds)")
plt.legend(loc='upper left', ncol=2)
plt.tight_layout()
plt.savefig("plots/plot_varyK.pdf")
plt.clf()


###############################
### Plot : Vary d
###############################
plt.rcParams.update({'font.size':font_size})
i = 0 # for marker index
for fixed_N in [N_vals[2], N_vals[0]]:
  for fixed_K in [K_vals[2], K_vals[0]]:
    y_vals_P = []
    y_vals_S = []
    for line in lines:
      if line[0] == fixed_N and line[1] == fixed_K:
        y_vals_P.append(line[3])
        y_vals_S.append(line[4])
    
    plt.plot(d_vals, y_vals_P, marker=list(reversed(markers))[i], markersize=marker_size, fillstyle='none', color=colors[0], label= "P, N=%d, K=%d" % (fixed_N, fixed_K), linestyle="--")
    plt.plot(d_vals, y_vals_S, marker=list(reversed(markers))[i], markersize=marker_size, fillstyle='none', color=colors[1], label= "S, N=%d, K=%d" % (fixed_N, fixed_K))
    i += 1
  
plt.gca().xaxis.set_ticks(d_vals)
plt.title("Varying d for fixed N and K", fontsize=font_size)
plt.xlabel("Vector dimension d")
plt.ylabel("Time (seconds)")
plt.legend(loc='upper left', ncol=2)
plt.tight_layout()
plt.savefig("plots/plot_varyd.pdf")
plt.clf()

