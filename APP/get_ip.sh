#！/bin/bash
if [ $IP ];then
  echo var url=\"$IP\"\; > ./static/js/ip.js 
else
  echo "no ip" > ./1.txt
fi



