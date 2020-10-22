#Create a simulator object
set ns [new Simulator]

#membuat file trace
set file [open fileTrace.tr w]
$ns trace-all $file

#init node
set n0 [$ns node]
set n1 [$ns node]

#Define different colors for data flows (for NAM)
$n0 color 1 Blue
$n1 color 2 Red

$ns duplex-link $ns0 $n1 1Mb 10Ms DropTail
$ns duplex-link $ns0 $n1 1Mb 5Ms DropTail
$ns duplex-link $ns0 $n1 5Mb 10Ms DropTail

#membuat traffic TCP biasa
set tcp0 [new Agent/TCP]
$tcp0 set class_2
$ns attach-agent $n0 $tcp0
#set sink [new Agent/TCPSink]
#$ns attach-agent
$ns run
