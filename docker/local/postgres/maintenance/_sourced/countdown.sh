#!/usr/bin/env bash

countdown(){

    declare desc="A simple countdown."

    local seconds="${1}"

    if ! [[ "$seconds" =~ ^[0-9]+$ ]]; then
        echo -ne "Error: Seconds must be a positive integer. \n"
        return 1
    fi

    local d=$(( $(date +%s) + seconds ))

    while [ "$d" -ge $(date +%s) ]; do
        
        echo -ne "$(date -u --date=@$(($d - $(date +%s))) +%H:%M:%S) \r"

        sleep 0.1
    done
}
