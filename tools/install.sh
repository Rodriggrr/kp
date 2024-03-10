#!/bin/bash

amarelo='\033[0;33m'
vermelho='\033[0;31m'
verde='\033[0;32m'
reset='\033[0m'

echo "Checking and installing the necessary dependencies..."

# Install python3-pip
echo -n "Python3-pip... "
sudo apt-get install python3-pip >> /dev/null 2>&1
echo "OK"

# Install the termcolor package
echo -n "Termcolor... "
pip install termcolor >> /dev/null 2>&1
echo "OK"

# Set the installation directory
INSTALL_DIR=~/.local/bin

# Check the installation directory
echo -n "Checking the installation directory... "
if [ ! -d $INSTALL_DIR ]; then
    echo -n "Nonexistent, creating... "
    mkdir -p $(eval echo $INSTALL_DIR)
fi
echo "OK"

# download kp
echo -n "Downloading kp... "
curl -fsSL https://raw.githubusercontent.com/Rodriggrr/kp/main/kp.py > $INSTALL_DIR/kp
echo "OK"

# CHMOD the file
chmod +x $INSTALL_DIR/kp

# Check for PATH

answer=""

status=$(echo $PATH | grep -o '/.local/bin' | wc -l)

if [ $status = "0" ]; then
	echo "${vermelho}ATENÇÃO: ${INSTALL_DIR} não existe na varíavel PATH. Deseja adicionar? Será necessário reiniciar o terminal. (caso escolha não, o programa não irá funcionar) [Y/n]${reset}"
    read answer

    if [ $answer = "Y" ] || [ $answer = "y" ]; then
        echo "export PATH=\$PATH:${INSTALL_DIR}" >> ~/.bashrc
        echo "export PATH=\$PATH:${INSTALL_DIR}" >> ~/.zshrc
    fi
fi 

# Check if the copy was successful
if [ $? -eq 0 ]; then
    echo "Program $PROGRAM installed successfully in $INSTALL_DIR"
else
    echo "An error occurred while installing the $PROGRAM program"
fi
