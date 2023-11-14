#!/bin/bash

while true
do
    start=$(date +%s.%N)

    chrome_tab_id=$(xdotool search -class "chromium-browser" | head -n 1)
    xdotool windowactivate --sync $chrome_tab_id key F5

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