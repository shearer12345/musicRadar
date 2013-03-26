musicRadar
==========

An optical-based physical, tangible beat sequencer.

Depends
=======

musicRadar depends on OpenCV and FluidSynth

OpenCV
------

See http://pranith.wordpress.com/2012/11/29/opencv-2-4-2-in-ubuntu/ for instructions

    sudo apt-add-repository ppa:bobby-prani/opencv-2.4.2
    sudo apt-get update
    sudo apt-get install python-opencv

FluidSynth
----------

See https://pypi.python.org/pypi/fluidsynth

    sudo apt-get install fluidsynth
    sudo pip install fluidsynth

Usage
=====

Launch musicRadar:
    python musicRadar.py

1. add colours object to the camera's field of view to trigger samples
2. ...
