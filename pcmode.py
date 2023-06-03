#! /usr/bin/env python3
# Sets up different types of editing modes.

import subprocess
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs.dialogs import Messagebox
import time
import argparse
import pyudev


CODE_DESKTOP = 0
GRAPHICS_DESKTOP = 1
MUSIC_DESKTOP = 2

jackRunning = False
udev = pyudev.Context()
codeStarted = False
graphicsStarted = False


def switchVirtualDesktop(number):
    # Switch to a different virtual desktop in Ubuntu.
    subprocess.run(['wmctrl', '-s', str(number)])

    
def runProgram(program, *args):
    # Run a program with the given arguments.
    return subprocess.Popen([program, *args], stdin=None, stdout=None, stderr=None)

def isDeviceConnected(deviceName):
    # Check if a device is connected.
    for device in udev.list_devices():
        if device.get('ID_MODEL') == deviceName:
            return True
    return False
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['code', 'graphics', 'music'], help='The mode to run.')
    args = parser.parse_args()
    if args.mode == 'code':
        codeMode()
    elif args.mode == 'graphics':
        graphicsMode()
    elif args.mode == 'music':
        musicMode()

def codeMode():
    switchVirtualDesktop(CODE_DESKTOP)
    if codeStarted:
        return
    runProgram('code')
    runProgram('gnome-terminal')
    runProgram('firefox')

def graphicsMode():
    switchVirtualDesktop(GRAPHICS_DESKTOP)
    if graphicsStarted:
        return
    runProgram('aseprite')

def musicMode():
    global jackRunning
    switchVirtualDesktop(MUSIC_DESKTOP)
    if not jackRunning:
        Messagebox.ok(title='Plug in Piano', message='Please connect your digital piano.')
        #if not isDeviceConnected('Yamaha Corp. Digital Piano'):
        #    Messagebox.ok(title='Error', message='Please connect your digital piano.')
        #    return
        
        jack = subprocess.Popen(['pasuspender', '--', 'jackd', '-r', '-d', 'alsa'], stdin=None, stdout=None, stderr=None)
        time.sleep(0.5)
        if jack.poll() is None:
            jackRunning = True
        else:
            Messagebox.ok(title='Error', message='Jack failed to start. Please check your audio settings.')
            return
        runProgram('qjackctl')
        runProgram('qsynth')
        runProgram('musescore.mscore')
        runProgram('audacity')

if __name__ == '__main__':
    main()
