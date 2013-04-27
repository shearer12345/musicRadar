'''
Created on 6 Sep 2012

@author: shearer
'''
import sys, time, math

import numpy as np
try:
    import cv2
    f = cv2.moveWindow
except ImportError:
    print 'Cannot import cv2. See http://pranith.wordpress.com/2012/11/29/opencv-2-4-2-in-ubuntu/ for instructions. Try "sudo apt-add-repository ppa:bobby-prani/opencv-2.4.2 \ sudo apt-get update \ sudo apt-get install python-opencv". Exiting!'
    sys.exit(0) 

try: 
    from fluidsynth import fluidsynth
    #TODO test fluidsynth - sudo apt-get install fluidsynth fluid-soundfont-gm
except ImportError:
    print 'Cannot import fluidsynth. Try "sudo pip install fluidsynth". More details at https://pypi.python.org/pypi/fluidsynth. Exiting!'
    sys.exit(0)    


#on linux - sudo apt-get install fluidsynth

def colorFind(hsvinput, color=124, tightness=20, threshold=50, satMin=50, valueMin=50, satMax=255, valueMax=255, ksize=(5,5), sigmaX=4.0, sigmaY=4.0):
    mask1 = cv2.inRange(hsv, np.array((color-tightness, satMin, valueMin)), np.array((color+tightness, satMax, valueMax)))
    mask2 = cv2.inRange(hsv, np.array((255.0+color-tightness, satMin, valueMin)), np.array((255.0+color+tightness, satMax, valueMax)))
    mask = cv2.add(mask1, mask2)
    mask = cv2.GaussianBlur(src=mask, ksize=kernelSize, sigmaX=sigmaX, sigmaY=sigmaY)
    mask = cv2.resize(mask, (1, height))
    mask = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5)))
    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5)))
    ret, mask = cv2.threshold(src=mask, thresh=threshold, maxval=255, type=cv2.THRESH_BINARY)
    #mask = cv2.resize(mask, (width, height))
    return mask


def fluid_init():
    global settings
    global synth
    global driver
    settings = fluidsynth.FluidSettings()
    settings.quality = "low"
    synth = fluidsynth.FluidSynth(settings)
    synth.load_soundfont('/usr/share/sounds/sf2/FluidR3_GM.sf2')
    
    driver = fluidsynth.FluidAudioDriver(settings, synth)
        
    synth.program_change(0, 0) #piano
    synth.program_change(1, 3) #space
    synth.program_change(2, 4) #flute
    synth.program_change(3, 14) #
    synth.program_change(4, 15) #
    synth.program_change(5, 28) #
    synth.program_change(6, 36) #
    synth.program_change(7, 41) #
    synth.program_change(8, 47) #
    synth.program_change(9, 0)# drums
    synth.program_change(13, 52) #
    synth.program_change(10, 71) #
    synth.program_change(11, 84) #
    synth.program_change(12, 112) #
    synth.program_change(12, 123) #

    
def fluid_test(delay=0.5, instrument=0):
    global synth
    
    scale = (0, 1, 2, 3, 4, 5, 6, 7, 8, 60, 62, 64, 65, 67, 69, 71, 72)

    for note in scale:
        synth.noteon(0, note, 127)
        time.sleep(delay)
        synth.noteoff(0, note)
    
def triggerNextBar(startTicks, sequencer, ticksPerBar, c_scale):
    
    global barCounter
    ticksNow = sequencer.ticks
    ticksElapsed = ticksNow - startTicks
    bar = int(math.ceil(ticksElapsed / ticksPerBar))
    print bar
    
    if bar > barCounter:
        barCounter = bar
        print 'adding sequence'
        ticksNextBarStart = (bar * ticksPerBar) + ticksNow
#        sequencer.send(c_scale[0], ticksNextBarStart)

        
#    sequencer.send(c_scale[5], ticks)
#    sequencer.send(c_scale[9], ticks)
    pass

if __name__ == '__main__':
#    cv2.namedWindow('window1', cv2.WINDOW_AUTOSIZE)

    
    #PARAMS
    index = 1
    resolution = (640,480)
    brightness = 0.2
    contrast = 0.4
    saturation = 0.73
    gain = 1.0
    exposure = 1.0
    hue = 0

    cropWidth = 20
    topCut = 0
    bottomCut = 98
        
    kernelSize = (9, 9) #must be positive and odd
    
    sigmaX = 4.0
    sigmaY = 4.0

    tightness = 25
        
    satMin = 40
    satMax = 255
    valueMin = 40
    valueMax = 255


    fluid_init()
    
    rollingX = 0
    rollingY = 0
    
    fullFrame = 'fullframe'
    cv2.namedWindow(fullFrame)
    cv2.moveWindow(fullFrame, rollingX, rollingY)
    rollingX += 640
    
    
    cutFrame = 'cutframe'
    cv2.namedWindow(cutFrame)
    cv2.moveWindow(cutFrame, rollingX, rollingY)
    rollingX += cropWidth
    
    smoothedFrame = 'smoothedFrame'
    cv2.namedWindow(smoothedFrame)
    cv2.moveWindow(smoothedFrame, rollingX, rollingY)
    rollingX += cropWidth
    
    redFrame = 'redFrame'
    cv2.namedWindow(redFrame)
    cv2.moveWindow(redFrame, rollingX, rollingY)
    rollingX += cropWidth
    
    yellowFrame = 'yellowFrame'
    cv2.namedWindow(yellowFrame)
    cv2.moveWindow(yellowFrame, rollingX, rollingY)
    rollingX += cropWidth
                    
    greenFrame = 'greenFrame'
    cv2.namedWindow(greenFrame)
    cv2.moveWindow(greenFrame, rollingX, rollingY)
    rollingX += cropWidth
    
    cyanFrame = 'cyanFrame'
    cv2.namedWindow(cyanFrame)
    cv2.moveWindow(cyanFrame, rollingX, rollingY)
    rollingX += cropWidth
    
    blueFrame = 'blueFrame'
    cv2.namedWindow(blueFrame)
    cv2.moveWindow(blueFrame, rollingX, rollingY)
    rollingX += cropWidth
    
    magentaFrame = 'magentaFrame'
    cv2.namedWindow(magentaFrame)
    cv2.moveWindow(magentaFrame, rollingX, rollingY)
    rollingX += cropWidth
    
    videoCapture = cv2.VideoCapture(index)
    
    videoCapture.set(cv2.cv.CV_CAP_PROP_BRIGHTNESS, brightness)
    videoCapture.set(cv2.cv.CV_CAP_PROP_CONTRAST, contrast)
    videoCapture.set(cv2.cv.CV_CAP_PROP_SATURATION, saturation)
    videoCapture.set(cv2.cv.CV_CAP_PROP_GAIN, gain)
    videoCapture.set(cv2.cv.CV_CAP_PROP_EXPOSURE, exposure)
    videoCapture.set(cv2.cv.CV_CAP_PROP_HUE, hue)
    
    activeImage = cv2.imread('loading.jpg')
    
    noteOnSetList = [set([]), set([])]
    channelList = [9, 11]
    #channel =0
    #channel = 3

    pentScale = (61, 63, 66, 68, 70, 73, 75, 78, 80, 83, 86)
    
    sequencer = fluidsynth.FluidSequencer()
    sequencer.beats_per_minute = 120
    beat_length = sequencer.ticks_per_beat
    
    print "BPM:", sequencer.beats_per_minute
    print "TPB:", sequencer.ticks_per_beat
    print "TPS:", sequencer.ticks_per_second
    
    tps = sequencer.ticks_per_second
    print type(tps), tps
    
    dest = sequencer.add_synth(synth)
    
    c_scale = []

    for note in range(60, 72):
        event = fluidsynth.FluidEvent()
        event.dest = dest[0]
        event.note(0, note, 127, int(beat_length*0.9))
        c_scale.append(event)
        
    startTicks = sequencer.ticks
    notesPerBar = 4
    barCounter = -1
    
    ticksPerBar = notesPerBar * sequencer.ticks_per_beat
    
    print 'ticksPerBar: ', ticksPerBar
    triggerNextBar(startTicks, sequencer, ticksPerBar, c_scale)
    
    
    while True:
    
        triggerNextBar(startTicks, sequencer, ticksPerBar, c_scale)
    
        ret, activeImage = videoCapture.read()
             
        imageHeight = activeImage.shape[0]
        imageWidth = activeImage.shape[1]
           
        
        x1 = (imageWidth / 2) - (cropWidth / 2)
        x2 = (imageWidth / 2) + (cropWidth / 2)
        y1 = 0 + topCut
        y2 = imageHeight - bottomCut
        rect = activeImage[y1:y2, x1:x2]
        
        smoothed = cv2.GaussianBlur(src=rect, ksize=kernelSize, sigmaX=sigmaX, sigmaY=sigmaY)
        
        height, width, depth = rect.shape
        
        hsv = cv2.cvtColor(rect, cv2.cv.CV_BGR2HSV)
        preMult = 255.0/360.0
        red, yellow, green, cyan, blue, magenta= 0 * preMult, 60 * preMult, 120 * preMult, 180 * preMult, 240 * preMult, 300 * preMult
        
        thresh = 40
        redMask = colorFind(hsv, color=red, tightness=40, threshold=thresh, satMin=150, valueMin=150, satMax=255, valueMax=255, ksize=(5,5), sigmaX=4.0, sigmaY=4.0)
        yellowMask = colorFind(hsv, color=yellow, tightness=40, threshold=thresh, satMin=150, valueMin=150, satMax=255, valueMax=255, ksize=(5,5), sigmaX=4.0, sigmaY=4.0)
        greenMask =  colorFind(hsv, color=green, tightness=20, threshold=thresh, satMin=50, valueMin=50, satMax=255, valueMax=255, ksize=(5,5), sigmaX=4.0, sigmaY=4.0)
        cyanMask = colorFind(hsv, color=cyan, tightness=15, threshold=thresh, satMin=150, valueMin=150, satMax=255, valueMax=255, ksize=(5,5), sigmaX=4.0, sigmaY=4.0)
        blueMask = colorFind(hsv, color=blue, tightness=15, threshold=thresh, satMin=150, valueMin=150, satMax=255, valueMax=255, ksize=(5,5), sigmaX=4.0, sigmaY=4.0)
        magentaMask = colorFind(hsv, color=magenta, tightness=20, threshold=thresh, satMin=150, valueMin=150, satMax=255, valueMax=255, ksize=(5,5), sigmaX=4.0, sigmaY=4.0)
        
        cv2.imshow(fullFrame, activeImage)
        cv2.imshow(cutFrame, rect)  
        cv2.imshow(smoothedFrame, smoothed)
        
        cv2.imshow(redFrame, redMask)
        cv2.imshow(yellowFrame, yellowMask)
        cv2.imshow(greenFrame, greenMask)
        cv2.imshow(cyanFrame, cyanMask)
        cv2.imshow(blueFrame, blueMask)
        cv2.imshow(magentaFrame, magentaMask)
    
        noteToBeOnSetList = [set([]), set([])]
        noteToTurnOnSetList = [set([]), set([])]
        noteToTurnOffSetList = [set([]), set([])]

        noteRangeList = [4, 5]
        noteMinList = [40, 0]
    
        drums = 0
        melody = 1
        for index, value in enumerate(redMask):
            for index2, value in enumerate(value):
                if value > 0:
                    r = noteRangeList[melody]
                    m = noteMinList[melody]
                    note = int((float(index) * (r/400.0))+m)
                    note = pentScale[note % len(pentScale)]
                    #print index, note
                    noteToBeOnSetList[melody].add(note)
                    #break
    

        for index, value in enumerate(yellowMask):
            for index2, value in enumerate(value):
                if value > 0:
                    channelListIndex = drums
                    r = noteRangeList[drums]
                    m = noteMinList[drums]
                    note = int((float(index) * (r/400.0))+m)
                    #print index, note
                    noteToBeOnSetList[drums].add(note)
                    break
        
        #3
        for index, value in enumerate(greenMask):
            for index2, value in enumerate(value):
                if value > 0:
                    r = noteRangeList[drums]
                    m = noteMinList[drums]
                    note = int((float(index) * (r/400.0))+m)
                    #note = pentScale[note]
                    #print index, note
                    noteToBeOnSetList[drums].add(note)
                    #break
        #4
        for index, value in enumerate(cyanMask):
            for index2, value in enumerate(value):
                if value > 0:
                    r = noteRangeList[drums]
                    m = noteMinList[drums]
                    note = int((float(index) * (r/400.0))+m)
                    #note = pentScale[note]
#print index, note
                    noteToBeOnSetList[drums].add(note)
                    break
        #5               
        for index, value in enumerate(blueMask):
            for index2, value in enumerate(value):
                if value > 0:
                    r = noteRangeList[melody]
                    m = noteMinList[melody]
                    note = int((float(index) * (r/400.0))+m)
                    note = pentScale[note % len(pentScale)]
                    #print index, note
                    noteToBeOnSetList[melody].add(note)
                    break

        #6
        for index, value in enumerate(magentaMask):
            for index2, value in enumerate(value):
                if value > 0:
                    r = noteRangeList[drums]
                    m = noteMinList[drums]
                    note = int((float(index) * (r/400.0))+m)
                    #note = pentScale[note]
#print index, note
                    noteToBeOnSetList[drums].add(note)
                    break
                            
        #stop all on that shouldn't be and start those that should be

        for channelListIndex, value in enumerate(channelList):
            noteToTurnOffSetList[channelListIndex] = noteOnSetList[channelListIndex] - noteToBeOnSetList[channelListIndex] #those on less those that should be on

            noteToTurnOnSetList[channelListIndex] = noteToBeOnSetList[channelListIndex] - noteOnSetList[channelListIndex] #those that should be less those that are
            
            for note in noteToTurnOffSetList[channelListIndex]:
                #print 'note ' + str(note) + ' off'
                synth.noteoff(channelList[channelListIndex], note)
                
            for note in noteToTurnOnSetList[channelListIndex]:
                #print 'note ' + str(note) + ' on'
                
                #TODO comments to disable this trigger
                synth.noteon(channelList[channelListIndex], note, 127)
                pass
                
            #copy the tobe list to the on list
            noteOnSetList[channelListIndex] = noteToBeOnSetList[channelListIndex]
            
            #synth.noteon(0, note, 127)
            

        
        k = cv2.waitKey(10);
        if k == 27 or k== 1048603: # k == 'f' 
            break
        elif k == 1048686:
            channelList[0] += 1
            if channelList[0] > 15: channelList[0] = 0 
            print 'channel 0 bumped to ' + str(channelList[0])
            for note in noteOnSetList[0]:
                #print 'note ' + str(note) + ' off'
                synth.noteoff(channelList[0], note)
            noteOnSetList[0] = set([])
        elif k == 1048685:
            channelList[1] += 1
            if channelList[1] > 15: channelList[1] = 0 
            print 'channel 1 bumped to ' + str(channelList[1])
            for note in noteOnSetList[1]:
                #print 'note ' + str(note) + ' off'
                synth.noteoff(channelList[1], note)
            noteOnSetList[1] = set([])
        elif k != -1: print k
        
            
cv2.destroyAllWindows()    