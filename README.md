# network-simulator-mptcp
simulasi jaringan mptcp client-server

# apa itu MPTCP?
MPTCP atau multipath-tcp adalah modifisikasi dari TCP yang biasa dengan menggunakan simultan beberapa interfaces jaringan atau IP, dengan begitu dapat membagi data ke beberapa subflow atau inferface yang terhubung tersebut. 

# kenapa menggunakan mptcp?
alasan harus menggunakan mptcp karena perangkat yang mendukung sudah memadai, seperti smartphone yang sekarang sudah dibekali oleh dua interface yaitu untuk jenis komunikasi LTE dan koneksi jaringan Wifi, atau pada perangkat server yang terhubung ke banyak switch dan rak server membutuhkan kecepatan transfer yang lebih serta meminimalisir kegagalan jika ada interface yang tiba tiba terputus

# check mptcp level kernel in ubuntu 
```bash
sudo sysctl net.mptcp
```

# cek congestion control pada mptcp level kernel
```bash
sudo sysctl net | grep congestion
```