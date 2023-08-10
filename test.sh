#!/bin/bash

timestamp=$(date +"%Y_%m_%d %H:%M:%S")
result_file="resultatsp2vsp7_$timestamp.csv"

echo "Protocol,Message Length,Message Count,sleep,receivers,Total Time,Average" >> "$result_file"

echo "--------------------IVY------------------" >> "$result_file"
sleep=0
message_count=100000
length=10

for ((receivers=5; receivers<=50; receivers+=5)); do

    result=$(python3 main2.py --protocol ivy --port 10.34.127.255:7650 --ivybus_test_manager 10.34.127.255:1198 --length 10 --message_count 10000 --nbr_receivers $receivers --hosts vm-p2-ubuntu.achil.recherche.enac.fr vm-p4-ubuntu.achil.recherche.enac.fr --usernames achil | tail -n 1)
    total_time=$(echo "$result" | awk '{print $1}')
    average=$(echo "$result" | awk '{print $2}')
    echo "ivy,$length,$message_count,$sleep,$receivers,$total_time,$average" >> "$result_file"
done