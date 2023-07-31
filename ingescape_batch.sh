#!/bin/bash

timestamp=$(date +"%Y%m%d%H%M%S")
result_file="resultats_$timestamp.csv"

echo "Protocol,Message Length,Message Count,sleep,receivers,Total Time,Average" >> "$result_file"

echo "--------------------IVY------------------" >> "$result_file"
receivers=1
for sleep in 0 0.0001 0.00001
do 
    for length in 5 500 1000 2000 3000
    do
        echo "Envoi de batchs de messages sans sleep de $length caracteres avec ivy" >> "$result_file"
        for ((message_count=1000; message_count<=10000; message_count+=1000)); do

            result=$(python3 main.py --protocol ivy --message_count $message_count --port 10.34.127.255:6475 --length $length --log_level FATAL | tail -n 2)
            total_time=$(echo "$result" | awk '{print $9}')
            average=$(echo "$result"| tail -n 1 | awk '{print $4}')
            echo "IVY,$length,$message_count,$sleep,$receivers,$total_time,$average" >> "$result_file"

        done

    done

    echo "--------------------ZeroMQ------------------" >> "$result_file"


    for length in 5 500 1000 2000 3000
    do
        echo "Envoi de batchs de messages sans sleep de $length caracteres avec zeromq" >> "$result_file"
        for ((message_count=1000; message_count<=10000; message_count+=1000)); do

            result=$(python3 main.py --protocol zeromq --message_count $message_count --port 6475 --length $length --log_level FATAL | tail -n 2)
            total_time=$(echo "$result" | awk '{print $9}')
            average=$(echo "$result"| tail -n 1 | awk '{print $4}')
            echo "ZeroMQ,$length,$message_count,$sleep,$receivers,$total_time,$average" >> "$result_file"
        done

    done

    echo "--------------------ingescape------------------" >> "$result_file"
    for length in 5 500 1000 2000 3000
    do
        echo "Envoi de batchs de messages sans sleep de $length caracteres avec ingescape" >> "$result_file"
        for ((message_count=1000; message_count<=10000; message_count+=1000)); do

            result=$(python3 main.py --protocol ingescape --message_count $message_count --port 5670 --length $length --device enp6s18 --log_level FATAL | tail -n 2)
            total_time=$(echo "$result" | awk '{print $9}')
            average=$(echo "$result"| tail -n 1 | awk '{print $4}')
            echo "ingescape,$length,$message_count,$sleep,$receivers,$total_time,$average" >> "$result_file"
        done

        
    done
done

