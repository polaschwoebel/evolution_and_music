#!/bin/sh
# This script can be run by either:
#       sh alife.sh m
# or
#       sh alife.sh p
# Ctrl-C will end it

PD_DIR=''

if [ "$1" == 'maire' ] || [ "$1" == 'm' ]; then
    PD_DIR='/Applications/Pd.app/Contents/MacOS/Pd'
elif [ "$1" == 'pola' ] || [ "$1" == 'p' ]; then
    PD_DIR='/Applications/Pd-0.47-1-64bit.app/Contents/MacOS/Pd'
else
    echo 'Please enter the location of the Pure Data application:'
    read PD_DIR
fi

echo 'Starting PureData...'
$PD_DIR pure_data/EVOLUTION_ALL_PATCHES-LIVE-INPUT.pd &
echo 'Press enter to continue once PureData is ready'
read enter
echo 'Starting Python...'
python interactive_evolution.py
