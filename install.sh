#!/bin/bash

# This script installs the required dependencies for the project, on linux (ubuntu based)

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit
fi


echo " - Updating repositories"
apt update

echo " - Installing python"
apt install -y python3 python3-pip
pip3 install --upgrade pip
pip3 install poetry




echo " - Done!"


