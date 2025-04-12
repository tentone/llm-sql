#!/bin/bash

# This script installs the required dependencies for the project, on linux (ubuntu based)

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit
fi

APPIMAGE_PATH="$HOME/AnythingLLMDesktop.AppImage"
SERVICE_NAME="anythingllmdesktop"
SERVICE_FILE="$HOME/.config/systemd/user/${SERVICE_NAME}.service"

echo " - Updating repositories"
apt update

echo " - Installing python"
apt install -y python3 python3-pip
pip3 install --upgrade pip
pip3 install poetry

echo " - Installing AnythingLLM"
curl -fsSL https://cdn.anythingllm.com/latest/installer.sh | sh

echo " - Register service for AnythingLLM"
mkdir -p ~/.config/systemd/user
cat > "$SERVICE_FILE" <<EOL
[Unit]
Description=AnythingLLM Desktop AppImage
After=network.target

[Service]
ExecStart=$APPIMAGE_PATH
Restart=always
Environment=DISPLAY=:0
Environment=XAUTHORITY=$HOME/.Xauthority

[Install]
WantedBy=default.target
EOL

echo " - Starting service '$SERVICE_NAME'"
systemctl --user daemon-reexec
systemctl --user daemon-reload
systemctl --user enable "$SERVICE_NAME"
systemctl --user start "$SERVICE_NAME"



echo " - Done!"


