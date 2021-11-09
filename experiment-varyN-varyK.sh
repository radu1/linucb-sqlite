#!/bin/bash

rm results_varyN_varyK.txt
touch results_varyN_varyK.txt

R=2 # number of runs

for N in {5..85..20}
  do 
  for K in {5..85..20}
    do
    echo "Run with N=$N K=$K"
    python3 prep.py $N $K
    
    #echo "************************************************"
    #echo "Python"
    #echo "************************************************"
    t_start=$(date +%s.%N)
    for i in `seq 1 $R`:
    do
      python3 linucb.py
    done
    t_end=$(date +%s.%N)
    time=$(echo "($t_end-$t_start)/$R" | bc -l)
    echo "  Python $time seconds"

    aux="$N $K $time"

    #echo "************************************************"
    #echo "SQLite"
    #echo "************************************************"
    t_start=$(date +%s.%N)
    for i in `seq 1 $R`:
    do
    # https://askcodez.com/non-interactive-sqlite3-lutilisation-de-script-bash.html
./sqlite <<EOF
.read linucb.sql
EOF
done
    t_end=$(date +%s.%N)
    time=$(echo "($t_end-$t_start)/$R" | bc -l)
    echo "  SQLite $time seconds"

echo "$aux $time" >> results_varyN_varyK.txt

done
done


mkdir -p plots
# plot
python3 plot-varyN-varyK.py
