#!/usr/bin/env bash

yes_no() {
    # Prompt for confirmation. $1: confirmation message.

    local arg1="$1"
    local response

    # Prompt the user for input
    read -r -p "$arg1 (y/[n])? " response

    # Check the response
    if [[ "${response}" =~ ^[Yy]$ ]]; then
        return 0  # Success
    else
        return 1  # Failure
    fi
}
