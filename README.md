# BeatPython

A simple game that uses pose estimation to control what's happening. Now you can
beat your python anywhere!

## Dependencies
- mediapipe
- pygame
- opencv

## How to play
You use your left and right hand as swords, like in beat saber. Use your blue
hand to break the blue squares and the red hand to break the red squares.

Squares will disappear after some time. If you break a square with a wrong hand,
you get `-100` points, if right - you get `+(100 - t)` points, where `t` is the time 
from square spawn.

## Known issues
- For some reason it flips the view sometimes on NVIDIA KDE Manjaro.
- There are reports that the game doesn't work on ARM systems
