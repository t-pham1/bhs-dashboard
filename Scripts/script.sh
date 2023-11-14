#!/bin/bash

while true
do
    start=$(date +%s.%N)

    echo "GATHERING DATA AND UPDATING SPREADSHEET...\n"
    # nmap 10.1.50-53.1-40 -v -sn | grep down | sed 's/Nmap.*for //' | sed 's/ .*$//' > nodes_down.txt
    nbtscan 10.1.10.1-255 -s ',' | sed 's/<.*,//' | sed 's/,,/,/g' > workstations_up.txt
    nbtscan 10.1.50.1-40 -s ',' > 50.txt; nbtscan 10.1.51.1-40 -s ',' > 51.txt; nbtscan 10.1.52.1-40 -s ',' > 52.txt; nbtscan 10.1.53.1-40 -s ',' > 53.txt; nbtscan 10.1.54.1-20 -s ',' > 54.txt
    cat 50.txt 51.txt 52.txt 53.txt 54.txt | sed 's/,<.*>//' > nodes_up.txt
    cat workstations_up.txt nodes_up.txt > online.txt
    python3 nbtscan_to_csv.py

    echo "UPDATING MYSQL DATABASE WITH NEW SPREADSHEET...\n"
    sudo cp -r /home/tommy/Snipe-IT/Scripts/spreadsheet.csv /var/lib/mysql/snipeitdb
    python3 csv_to_mysql.py
    echo "SUCCESSFULLY UPDATED DATABASE!\n"

    xdotool key F5

    mv 50.txt 51.txt 52.txt 53.txt 54.txt nodes_up.txt workstations_up.txt online.txt nbtscan

    end=$(date +%s.%N)

    runtime=$(python -c "print(str(round(${end} - ${start}, 2)))")
    echo "Runtime: $runtime seconds"
    echo "Rerunning..."
    echo '5'; sleep 1
    echo '4'; sleep 1
    echo '3'; sleep 1
    echo '2'; sleep 1
    echo "1\n\n\n"; sleep 1
done
