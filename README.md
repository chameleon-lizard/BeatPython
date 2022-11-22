# BeatPython

A simple game that uses pose estimation to control what's happening. Now you can
beat your python anywhere!

## Dependencies
- mediapipe
- pygame
- opencv

## How to play
You use your left and right hand as swords, like in beat saber. Use your blue
hand to break the blur squares and the red hand to break the red squares.

Squares will disappear after some time. If you break a square with a wrong hand,
you get -100 points, if right - you get +(100 - t) points, where t is the time 
from square spawn.

If you move away from the camera, the game will crash, lol. Also, for some reason
it flips my view sometimes on Nvidia KDE Manjaro.

[![Demo CountPages alpha](https://chameleon-lizard.ru/p/game.gif)](https://chameleon-lizard.ru/p/game.gif)

Hello
