'''
Created on 26 Mar 2013

@author: shearer
'''
#!/usr/bin/env python

import time

from fluidsynth import fluidsynth

settings = fluidsynth.FluidSettings()
settings.quality = "low"

synth = fluidsynth.FluidSynth(settings)
synth.load_soundfont('/usr/share/sounds/sf2/FluidR3_GM.sf2')

driver = fluidsynth.FluidAudioDriver(settings, synth)

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

ticks = sequencer.ticks + 10
sequencer

sequencer.send(c_scale[0], ticks)
sequencer.send(c_scale[4], ticks)
sequencer.send(c_scale[7], ticks)
sequencer.send(c_scale[0], (ticks + int(sequencer.ticks_per_second * 4.0)))


ticks += beat_length

sequencer.send(c_scale[0], ticks)
sequencer.send(c_scale[5], ticks)
sequencer.send(c_scale[9], ticks)

ticks += beat_length

sequencer.send(c_scale[0], ticks)
sequencer.send(c_scale[4], ticks)
sequencer.send(c_scale[7], ticks)

ticks += beat_length

sequencer.send(c_scale[2], ticks)
sequencer.send(c_scale[5], ticks)
sequencer.send(c_scale[7], ticks)
sequencer.send(c_scale[11], ticks)

ticks += beat_length

sequencer.send(c_scale[0], ticks)
sequencer.send(c_scale[4], ticks)
sequencer.send(c_scale[7], ticks)

time.sleep(16)
