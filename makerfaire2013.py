'''
Created on 6 Sep 2012

@author: shearer
'''

bpm = 210
cam = 0

resolution = (320,240)
    
#Region params
sampleWidth = 10
edgeLeft1 = resolution[0] * 0.22
edgeRight1 = resolution[0] * 0.7
edgeTop1 = resolution[1] * 0.15
edgeBottom1 = resolution[1] * 0.75
brightness = 0.15
contrast = 0.05
saturation = 0.5
gain = 0.5
exposure = 1.0
hue = 0
if cam == 2:
    sampleWidth = 1
    edgeLeft1 = resolution[0] * 0.25
    edgeRight1 = resolution[0] * 0.78
    edgeTop1 = resolution[1] * 0.08
    edgeBottom1 = resolution[1] * 0.67
    brightness = 0.1
    contrast = 0.05
    saturation = 0.5
    gain = 0.5
    exposure = 1.0
    hue = 0
   
import sys, time, math

import numpy as np
try:
    import cv2
    from cv2.cv import CV_CAP_PROP_FRAME_WIDTH, CV_CAP_PROP_FRAME_HEIGHT, CV_CAP_PROP_BRIGHTNESS, CV_CAP_PROP_CONTRAST, CV_CAP_PROP_SATURATION, CV_CAP_PROP_GAIN, CV_CAP_PROP_EXPOSURE, CV_CAP_PROP_HUE
    
    f = cv2.moveWindow #test
except ImportError:
    print 'Cannot import cv2. See http://pranith.wordpress.com/2012/11/29/opencv-2-4-2-in-ubuntu/ for instructions. Try "sudo apt-add-repository ppa:bobby-prani/opencv-2.4.2 \ sudo apt-get update \ sudo apt-get install python-opencv". Exiting!'
    sys.exit(0) 

try: 
    from fluidsynth import fluidsynth    
except ImportError as e:
    print 'Cannot import fluidsynth. Try "sudo pip install fluidsynth". More details at https://pypi.python.org/pypi/fluidsynth. Exiting!'
    print 'Full error is: ', e
    sys.exit(0)    


def colorFind(hsvinput, color=124, tightness=20, threshold=50, satMin=50, valueMin=50, satMax=255, valueMax=255, ksize=(5,5), sigmaX=4.0, sigmaY=4.0):
    '''TODO what do this do?'''
    mask1 = cv2.inRange(hsv1, np.array((color-tightness, satMin, valueMin)), np.array((color+tightness, satMax, valueMax)))
    mask2 = cv2.inRange(hsv1, np.array((255.0+color-tightness, satMin, valueMin)), np.array((255.0+color+tightness, satMax, valueMax)))
    mask = cv2.add(mask1, mask2)
    mask = cv2.GaussianBlur(src=mask, ksize=kernelSize, sigmaX=sigmaX, sigmaY=sigmaY)
    mask = cv2.resize(mask, (1, height1))
    mask = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5)))
    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5)))
    ret, mask = cv2.threshold(src=mask, thresh=threshold, maxval=255, type=cv2.THRESH_BINARY)
    #mask = cv2.resize(mask, (width1, height1))
    return mask


def fluid_init():
    global settings
    global synth
    global driver
    settings = fluidsynth.FluidSettings()
    settings.quality = "low"
    synth = fluidsynth.FluidSynth(settings)
    soundFontFile = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
    try:
        synth.load_soundfont(soundFontFile)
    except fluidsynth.FluidError:
        print "Couldn't load soundfont file: '", "/usr/share/sounds/sf2/dFluidR3_GM.sf2'"
        print "Try 'sudo apt-get install fluid-soundfont-gm'"
        sys.exit(0)    
    
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

    
def fluid_test(delay=0.2, instrument=9):
    global synth
    
    scale = (0, 1, 2, 3, 4, 5, 6, 7, 8, 60, 62, 64, 65, 67, 69, 71, 72)

    for note in scale:
        synth.noteon(0, note, 127)
        time.sleep(delay)
        synth.noteoff(0, note)
    time.sleep(delay)
    
def checkBar():
    
    global sequencer, startTicks
    global beatsPerBar, ticksPerBar
    global bar, beat, beatInBar
    global nextBarStartTicks, nextBeatStartTicks
    global barTimeNormalised
    ticksNow = sequencer.ticks
    ticksElapsed = ticksNow - startTicks
    
#    print 'ticksNow', ticksNow
#    print 'ticksElapsed', ticksElapsed
    
    bar = int(math.ceil(ticksElapsed / ticksPerBar))
    beat = int(math.ceil( (ticksElapsed / sequencer.ticks_per_beat))) 
    beatInBar =  beat % beatsPerBar
    
    nextBarStartTicks = (bar +1) * ticksPerBar
    nextBeatStartTicks = (beat + 1) * sequencer.ticks_per_beat
    
    barTimeNormalised = float(( ticksNow - (ticksPerBar * bar))) / float(ticksPerBar)
    
    
    #print 'barTime=', barTimeNormalised, 'bar=', bar, 'beatInBar', beatInBar#, 'beat=', beat, 'nextBarStarts=', nextBarStartTicks, 'nextBeatStarts=', nextBeatStartTicks
    
if __name__ == '__main__':
#    cv2.namedWindow('window1', cv2.WINDOW_AUTOSIZE)

    cam1 = cv2.VideoCapture(cam)
    cam1.set(CV_CAP_PROP_FRAME_WIDTH, resolution[0])
    cam1.set(CV_CAP_PROP_FRAME_HEIGHT, resolution [1])
    #videoCapture = cv2.VideoCapture(index, resolution)
    
    cam1.set(CV_CAP_PROP_BRIGHTNESS, brightness)
    cam1.set(CV_CAP_PROP_CONTRAST, contrast)
    cam1.set(CV_CAP_PROP_SATURATION, saturation)
    cam1.set(CV_CAP_PROP_GAIN, gain)
    cam1.set(CV_CAP_PROP_EXPOSURE, exposure)
    cam1.set(CV_CAP_PROP_HUE, hue)

#    cam2 = cv2.VideoCapture(0)
#    cam2.set(CV_CAP_PROP_FRAME_WIDTH, resolution[0])
#    cam2.set(CV_CAP_PROP_FRAME_HEIGHT, resolution [1])
#    #videoCapture = cv2.VideoCapture(index, resolution)
#    
#    cam2.set(CV_CAP_PROP_BRIGHTNESS, brightness)
#    cam2.set(CV_CAP_PROP_CONTRAST, contrast)
#    cam2.set(CV_CAP_PROP_SATURATION, saturation)
#    cam2.set(CV_CAP_PROP_GAIN, gain) #doesn't work of PSEye
#    cam2.set(CV_CAP_PROP_EXPOSURE, exposure) #doesn't work of PSEye
#    cam2.set(CV_CAP_PROP_HUE, hue)
#    
    topCut1 = 0
    bottomCut1 = 98
    
    cropWidth2 = 20
    topCut2 = 0
    bottomCut2 = 98
        
    kernelSize = (9, 9) #must be positive and odd
    
    sigmaX = 4.0
    sigmaY = 4.0

    tightness = 25
        
    satMin = 40
    satMax = 255
    valueMin = 40
    valueMax = 200

    fluid_init() #initialiser fluidsynth
    
    #make windows    
    rollingX = 0
    rollingY = 0
    
    #CAM1 DISPLAY
    fullFrame1 = 'fullframe1'
    cv2.namedWindow(fullFrame1)
    cv2.moveWindow(fullFrame1, rollingX, rollingY)
    rollingX += resolution[0]
        
    cutFrame1 = 'cutframe1'
    cv2.namedWindow(cutFrame1)
    cv2.moveWindow(cutFrame1, rollingX, rollingY)
    rollingX += sampleWidth
    
    smoothedFrame1 = 'smoothedFrame1'
    cv2.namedWindow(smoothedFrame1)
    cv2.moveWindow(smoothedFrame1, rollingX, rollingY)
    rollingX += sampleWidth
    
    redFrame1 = 'redFrame1'
    cv2.namedWindow(redFrame1)
    cv2.moveWindow(redFrame1, rollingX, rollingY)
    rollingX += sampleWidth
    
    yellowFrame1 = 'yellowFrame1'
    cv2.namedWindow(yellowFrame1)
    cv2.moveWindow(yellowFrame1, rollingX, rollingY)
    rollingX += sampleWidth
                    
    greenFrame1 = 'greenFrame1'
    cv2.namedWindow(greenFrame1)
    cv2.moveWindow(greenFrame1, rollingX, rollingY)
    rollingX += sampleWidth
    
    cyanFrame1 = 'cyanFrame1'
    cv2.namedWindow(cyanFrame1)
    cv2.moveWindow(cyanFrame1, rollingX, rollingY)
    rollingX += sampleWidth
    
    blueFrame1 = 'blueFrame1'
    cv2.namedWindow(blueFrame1)
    cv2.moveWindow(blueFrame1, rollingX, rollingY)
    rollingX += sampleWidth
    
    magentaFrame1 = 'magentaFrame1'
    cv2.namedWindow(magentaFrame1)
    cv2.moveWindow(magentaFrame1, rollingX, rollingY)
    rollingX += sampleWidth
  
#    #CAM2 DISPLAY
#    rollingX = 0
#    rollingY += resolution[1]
#    
#    fullFrame2 = 'fullframe2'
#    cv2.namedWindow(fullFrame2)
#    cv2.moveWindow(fullFrame2, rollingX, rollingY)
#    rollingX += resolution[0]
#        
#    cutFrame2 = 'cutframe2'
#    cv2.namedWindow(cutFrame2)
#    cv2.moveWindow(cutFrame2, rollingX, rollingY)
#    rollingX += cropWidth2
#    
#    smoothedFrame2 = 'smoothedFrame2'
#    cv2.namedWindow(smoothedFrame2)
#    cv2.moveWindow(smoothedFrame2, rollingX, rollingY)
#    rollingX += cropWidth2
#    
#    redFrame2 = 'redFrame2'
#    cv2.namedWindow(redFrame2)
#    cv2.moveWindow(redFrame2, rollingX, rollingY)
#    rollingX += cropWidth2
#    
#    yellowFrame2 = 'yellowFrame2'
#    cv2.namedWindow(yellowFrame2)
#    cv2.moveWindow(yellowFrame2, rollingX, rollingY)
#    rollingX += cropWidth2
#                    
#    greenFrame2 = 'greenFrame2'
#    cv2.namedWindow(greenFrame2)
#    cv2.moveWindow(greenFrame2, rollingX, rollingY)
#    rollingX += cropWidth2
#    
#    cyanFrame2 = 'cyanFrame2'
#    cv2.namedWindow(cyanFrame2)
#    cv2.moveWindow(cyanFrame2, rollingX, rollingY)
#    rollingX += cropWidth2
#    
#    blueFrame2 = 'blueFrame2'
#    cv2.namedWindow(blueFrame2)
#    cv2.moveWindow(blueFrame2, rollingX, rollingY)
#    rollingX += cropWidth2
#    
#    magentaFrame2 = 'magentaFrame2'
#    cv2.namedWindow(magentaFrame2)
#    cv2.moveWindow(magentaFrame2, rollingX, rollingY)
#    rollingX += cropWidth2
    
    activeImage1 = cv2.imread('loading.jpg')
    
    noteOnSetList = [set([]), set([])]
    channelList = [9, 11]
    #channel =0
    #channel = 3

    scalePent = (61, 63, 66, 68, 70,
             73, 75, 78, 80, 83, 
             85, 87, 90, 92, 95,
             97)
    
    scaleWhole = (61, 63, 65, 66, 68, 70, 72,
                  73, 75, 77, 79, 80, 82, 84,
                  85, 87, 89, 91, 92, 94, 95,
                  97)
    
    #scaleCr
    scale = scalePent#scaleWhole
    sequencer = fluidsynth.FluidSequencer()
    sequencer.beats_per_minute = bpm
    beat_length = sequencer.ticks_per_beat
    
    print "BPM:", sequencer.beats_per_minute
    print "TPB:", sequencer.ticks_per_beat
    print "TPS:", sequencer.ticks_per_second
    
    tps = sequencer.ticks_per_second
    print type(tps), tps
    
    dest = sequencer.add_synth(synth)
    
    #fluidTestSequencer(sequencer)
    
    c_scale = []

    for note in range(60, 72):
        event = fluidsynth.FluidEvent()
        event.dest = dest[0]
        event.note(0, note, 127, int(beat_length*0.9))
        c_scale.append(event)
        
    startTicks = sequencer.ticks
    beatsPerBar = 4
    bar = -1
    beat = -1
    beatInBar = -1
    nextBarStartTicks = -1
    nextBeatStartTicks = -1
    barTimeNormalised = -1
    
    ticksPerBar = beatsPerBar * sequencer.ticks_per_beat
    
    while True:
    
        checkBar()
        
        ret, activeImage1 = cam1.read()
             
        imageHeight1 = activeImage1.shape[0]
        imageWidth1 = activeImage1.shape[1]
           
        #TODO recolouring not working
        recolouredImage1 = cv2.cvtColor(src=activeImage1, code=cv2.cv.CV_BGR2RGB)
        cv2.imshow(fullFrame1, recolouredImage1)
        
        #barTimeNormalised = 0.0
        barTimeNormalised = max(barTimeNormalised, 0.001)
        barTimeNormalised = 0.5
        
        x1 = (barTimeNormalised * edgeLeft1) + (1.0-barTimeNormalised)*edgeRight1
        x2 = x1 + sampleWidth
        y1 = edgeTop1
        y2 = edgeBottom1
        
        rect1 = recolouredImage1[y1:y2, x1:x2]
        cv2.imshow(cutFrame1, rect1)  
        
        smoothed1 = cv2.GaussianBlur(src=rect1, ksize=kernelSize, sigmaX=sigmaX, sigmaY=sigmaY)
        cv2.imshow(smoothedFrame1, smoothed1)
        
        height1, width1, depth1 = rect1.shape
        
        hsv1 = cv2.cvtColor(rect1, cv2.cv.CV_RGB2HSV)
        preMult = 255.0/360.0
        red, yellow, green, cyan, blue, magenta= 0 * preMult, 60 * preMult, 120 * preMult, 180 * preMult, 240 * preMult, 300 * preMult
        
        thresh = 10
        redMask = colorFind(hsv1, color=red, tightness=40, threshold=thresh, satMin=150, valueMin=150, satMax=255, valueMax=255, ksize=(5,5), sigmaX=4.0, sigmaY=4.0)
        yellowMask = colorFind(hsv1, color=yellow, tightness=40, threshold=thresh, satMin=150, valueMin=150, satMax=255, valueMax=255, ksize=(5,5), sigmaX=4.0, sigmaY=4.0)
        greenMask =  colorFind(hsv1, color=green, tightness=20, threshold=thresh, satMin=50, valueMin=50, satMax=255, valueMax=255, ksize=(5,5), sigmaX=4.0, sigmaY=4.0)
        cyanMask = colorFind(hsv1, color=cyan, tightness=15, threshold=thresh, satMin=150, valueMin=150, satMax=255, valueMax=255, ksize=(5,5), sigmaX=4.0, sigmaY=4.0)
        blueMask = colorFind(hsv1, color=blue, tightness=17, threshold=thresh, satMin=150, valueMin=150, satMax=255, valueMax=255, ksize=(5,5), sigmaX=4.0, sigmaY=4.0)
        magentaMask = colorFind(hsv1, color=magenta, tightness=20, threshold=thresh, satMin=150, valueMin=150, satMax=255, valueMax=255, ksize=(5,5), sigmaX=4.0, sigmaY=4.0)
        
        cv2.imshow(redFrame1, redMask)
        cv2.imshow(yellowFrame1, yellowMask)
        cv2.imshow(greenFrame1, greenMask)
        cv2.imshow(cyanFrame1, cyanMask)
        cv2.imshow(blueFrame1, blueMask)
        cv2.imshow(magentaFrame1, magentaMask)
    
        noteToBeOnSetList = [set([]), set([])]
        noteToTurnOnSetList = [set([]), set([])]
        noteToTurnOffSetList = [set([]), set([])]

        noteRangeList = [4, 5]
        noteMinList = [40, 0]
    
        lastNote = -50
        lastNoteThresh = 0
        drums = 0
        melody = 1
        for index, value in enumerate(redMask):
            for index2, value in enumerate(value):
                if value > 0:
                    r = noteRangeList[melody]
                    m = noteMinList[melody]
                    note = int((float(index) * (r/400.0))+m)
                    note = scale[note % len(scale)]
                    if (lastNote < 0 or abs(note - lastNote) < lastNoteThresh): #prevent notes too near
                        lastNote = note
                        #print index, note
                        #noteToBeOnSetList[melody].add(note)
                        break
    
        lastNote = -50
        #this is getting hit today
        for index, value in enumerate(yellowMask):
            for index2, value in enumerate(value):
                if value > 0:
                    r = noteRangeList[melody]
                    m = noteMinList[melody]
                    note = 50#int((float(index) * (r/100.0))+m)
                    print note, 
                    note = scale[note % len(scale)]
                    print note
                    #print index, note
                    if (lastNote < 0 or abs(note - lastNote) < lastNoteThresh): #prevent notes too near
                        lastNote = note
                        noteToBeOnSetList[melody].add(note)
                        break 
        #3
        lastNote = -50
        for index, value in enumerate(greenMask):
            for index2, value in enumerate(value):
                if value > 0:
                    r = noteRangeList[drums]
                    m = noteMinList[drums]
                    note = int((float(index) * (r/400.0))+m)
                    #note = scale[note]
                    if (lastNote < 0 or abs(note - lastNote) < lastNoteThresh): #prevent notes too near
                        lastNote = note
                        #print index, note
                        #noteToBeOnSetList[drums].add(note)
                        #break
                    
        lastNote=-50
        #4 this gets hit for ORANGE - mainDrum
        for index, value in enumerate(cyanMask):
            for index2, value in enumerate(value):
                if value > 0:
                    r = noteRangeList[drums]
                    m = noteMinList[drums]
                    note = int((float(index) * (r/200.0))+m)
                    #note = scale[note]
                    if (lastNote < 0 or abs(note - lastNote) < lastNoteThresh): #prevent notes too near
                        lastNote = note
                        print m, note
                        #note = m 
                        #print index, note
                        noteToBeOnSetList[drums].add(note)
                        #break
                    
        #5 #this gets hit for YELLOW - mainMelodic               
        for index, value in enumerate(blueMask):
            for index2, value in enumerate(value):
                if value > 0:
                    r = noteRangeList[melody]
                    m = noteMinList[melody]
                    note = int((float(index) * (r/100.0))+m)
                    print note, 
                    note = scale[note % len(scale)]
                    print note
                    #print index, note
                    if (lastNote < 0 or abs(note - lastNote) < lastNoteThresh): #prevent notes too near
                        lastNote = note
                        noteToBeOnSetList[melody].add(note)
                        break

        #6
        lastNote = - 50
        for index, value in enumerate(magentaMask):
            for index2, value in enumerate(value):
                if value > 0:
                    r = noteRangeList[drums]
                    m = noteMinList[drums]
                    note = int((float(index) * (r/400.0))+m)
                    #note = scale[note]
#print index, note
                    if (lastNote < 0 or abs(note - lastNote) < lastNoteThresh): #prevent notes too near
                        lastNote = note
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