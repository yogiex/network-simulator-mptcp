#!/bin/bash
grep -v ARP sent | grep IP | awk '{print $8,$1}' | tr "," " " > sent_1
grep -v ARP received | grep IP | awk '{print $8,$1}' | tr "," " " > received_1

sort sent_1 > sent_sorted
sort received_1 > received_sorted

join sent_sorted received_sorted > combined_1

nl combined_1 | awk '{print $1, $4-$3}' > delay_1

gnuplot <<- EOF
        set title ""
        set ylabel "packet delay (sec)"
        set xlabel "packet number"
	set term png
	set output "latency_1.png"
	plot "delay_1" with linespoints
EOF