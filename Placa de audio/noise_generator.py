# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 11:29:57 2019

@author: Pato
"""


# The required imports...
import pyaudio
import random

# Set up a basic user screen...
# This assumes the default 80x24 Terminal window size...
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n$VER: Noise_Generator.py_Version_0.00.10_(C)2012_B.Walker_G0LCU.\n")
print("A DEMO, kids level, simple white noise generator for the MacBook Pro 13 inch.\n")
print("Also works on Windows Vista and Debian Linux from Python 2.6.x to 2.7.x.")
print("Pyaudio IS required for this to work on the platforms quoted...\n")
print("This DEMO lasts for a few seconds only but it is easy to make it continuous.")
print("It is also easily possible to vary the noise BW.\n")
print("Issued as Public Domain, you may do with this code as you please.\n\n\n\n\n\n\n\n\n\n\n")

# Open the stream required, mono mode only...
# Written _longhand_ so that youngsters can understand how it works...
stream=pyaudio.PyAudio().open(format=pyaudio.paInt8,channels=1,rate=22050,output=True)

# Now generate the _white_noise_ at the speakers/headphone output for a few seconds...
for n in range(0,220000,1): stream.write(chr(int(random.random()*256)))

# Close the open _channel(s)_...
stream.close()
pyaudio.PyAudio().terminate()

# End of Noise_Generator.py program...
# Enjoy finding simple solutions to often very difficult problems... ;o)