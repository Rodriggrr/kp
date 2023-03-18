#!/bin/bash

# Rename the file
mv kp.py kp

# Set the name of the program file
PROGRAM=kp

# Set the installation directory
INSTALL_DIR=/usr/bin

# Copy the program file to the installation directory
cp $PROGRAM $INSTALL_DIR

# Set the program file as executable
chmod +x $INSTALL_DIR/$PROGRAM

# Check if the copy was successful
if [ $? -eq 0 ]; then
    echo "Program $PROGRAM installed successfully in $INSTALL_DIR"
else
    echo "An error occurred while installing the $PROGRAM program"
fi
