#!/bin/bash

rm results.txt
touch results.txt

R=1000 # number of runs

Nmin=10
Nstep=10
Nmax=40

Kmin=10
Kstep=10
Kmax=40

dmin=2
dstep=2
dmax=8

for N in `seq $Nmin $Nstep $Nmax`; do
  for K in `seq $Kmin $Kstep $Kmax`; do
    for d in `seq $dmin $dstep $dmax`; do
      echo "Run with N=$N K=$K d=$d"
      python3 prep.py $N $K $d
      
      t_start=$(date +%s.%N)
      for i in `seq 1 $R`; do
        python3 linucb.py
      done
      t_end=$(date +%s.%N)
      time=$(echo "($t_end-$t_start)/$R" | bc -l)
      echo "  Python $time seconds"
      aux="$N $K $d $time"

      t_start=$(date +%s.%N)
      for i in `seq 1 $R`; do
# https://askcodez.com/non-interactive-sqlite3-lutilisation-de-script-bash.html
./sqlite <<EOF
.read linucb.sql
EOF
      done
      t_end=$(date +%s.%N)
      time=$(echo "($t_end-$t_start)/$R" | bc -l)
      echo "  SQLite $time seconds"
      echo "$aux $time" >> results.txt
   done # for d
  done # for K
done # for N

mkdir -p plots
python3 plot.py $Nmin $Nmax $Nstep $Kmin $Kmax $Kstep $dmin $dmax $dstep
