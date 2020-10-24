#Create a simulator object
set ns [new Simulator]

#membuat file trace
set file [open fileTrace.tr w]
$ns trace-all $file

#init node n0
set n0 [$ns node]
set n0_1 [$ns node]
set n0_2 [$ns node]

#coloring node
$n0 color red
$n0_1 color red
$n0_2 color red
#multihome interface
$ne multihome-add-interface $n0 $n0_1
$ne multihome-add-interface $n0 $n0_2

#init node n1
set n1 [$ns node]
set n1_1 [$ns node]
set n1_2 [$ns node]

#coloring node
$n0 color blue
$n0_1 color blue
$n0_2 color blue

#multihome interface
$ne multihome-add-interface $n1 $n1_1
$ne multihome-add-interface $n1 $n1_2


#Define different colors for data flows (for NAM)
$n0 color 1 Blue
$n1 color 2 Red

$ns duplex-link $ns0 $n1 1Mb 10Ms DropTail
$ns duplex-link $ns0 $n1 1Mb 5Ms DropTail


#membuat traffic TCP biasa
set tcp0 [new Agent/TCP]
$tcp0 set class_2
$ns attach-agent $n0 $tcp0
#set sink [new Agent/TCPSink]
#$ns attach-agent
$ns run
