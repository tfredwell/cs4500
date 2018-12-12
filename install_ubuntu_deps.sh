#!/usr/bin/env bash

echo "This installs the dependencies for wxpython on ubuntu based machines"
echo "This will prompt you to use root to install it"
sudo apt install libwxgtk3.0-dev \
    libwxgtk3.0-gtk3-dev \
    build-essential \
    libgtk-3-dev \
    libgstreamer1.0-dev \
    libgstreamer1.0 \
    libgstreamer-plugins-base1.0-dev \
    libwebkitgtk-3.0-dev
