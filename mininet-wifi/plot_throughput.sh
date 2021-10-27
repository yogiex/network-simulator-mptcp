#!/bin/bash
cat balia.txt | grep sec | head -n 60| tr - " " | awk '{print $4,$8}' > new_balia
cat lia.txt | grep sec | head -n 60 | tr - " " | awk '{print $4,$8}' > new_lia
cat olia.txt | grep sec | head -n 60 | tr - " " | awk '{print $4,$8}' > new_olia
cat wvegaz.txt | grep sec | head -n 60 | tr - " " | awk '{print $4,$8}' > new_wvegaz

gnuplot <<- EOF
        set title ""
        set ylabel "troughput (Mbps)"
        set xlabel "time"
	    set term png
	    set output "throughput.png"
	    plot "new_balia" title "balia" with linespoints, "new_lia" title "lia" with linespoints, plot "new_olia" title "olia" with linespoints, plot "new_wvegaz" title "wvegaz" with linespoints,
EOF