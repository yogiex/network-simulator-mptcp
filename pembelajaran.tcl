#       
#      n0_1==========n1_1
#     /                 \
#    /                   \
#   n0                  n1
#   \                   /
#    \                 /
#    no_2==========n1_2


#Create a simulator object
set ns [new Simulator]

#membuat file trace
set file [open fileTrace.tr w]
$ns trace-all $file

#procedur finis
proc finish {}{
    exec nam sctp.nam &
    exit 0
}

#init node n0
set n0 [$ns node]
set n0_1 [$ns node]
set n0_2 [$ns node]

#coloring node
$n0 color red
$n0_1 color red
$n0_2 color red

#multihome interface
$ns multihome-add-interface $n0 $n0_1
$ns multihome-add-interface $n0 $n0_2

#init node n1
set n1 [$ns node]
set n1_1 [$ns node]
set n1_2 [$ns node]

#coloring node
$n0 color blue
$n0_1 color blue
$n0_2 color blue

#multihome interface
$ns multihome-add-interface $n1 $n1_1
$ns multihome-add-interface $n1 $n1_2


#create link 
$ns duplex-link $ns0_1 $n1_1 1Mb 100Ms DropTail
$ns duplex-link $ns0_2 $n1_2 1Mb 100Ms DropTail

#sctp agent n0
set sctp0 [new Agent/SCTP]
$ns multihome-attach-agent $n0 $sctp0

#sctp agent n1
set sctp1 [new Agent/SCTP]
$ns multihome-attach-agent $n1 $sctp1

#connect sctp agent
$ns connect $sctp0 $sctp1

#create FTP connection over TCP
set ftp0 [new Application/FTP]
$ftp0 attach-agent $sctp0

$sctp0 set-primary-destination $n1_0

#setting primari destination 
$ns at 7.5 "$sctp0 set-primary-destination $n1_1"
$ns at 7.5 "$sctp0 print cwnd_"

#pembagian waktu pada saat program dijalankan
$ns at 0.5 "$ftp0 start"
$ns at 9.5 "$ftp0 stop"
$ns at 10.0 "finish"

$ns run
