#fractal tree
#accepts name of .wav file as first commend line input

import pygame, math, sys
from scipy.io import wavfile
from scipy import fft

#drawTree: given info of current branch, draw current branch and determine info for next two
def drawTree(x1, y1, angle, depth, colour, lvl, width):

    #only perform next level of algorithm if we aren't at the bottom (at depth = 0)
    if depth:

        #wait 10ms
        pygame.time.wait(1)

        #get end point of current branch (also start point)
        #also somewhat arbitrary
        x2 = x1 + int(math.cos(math.radians(angle)) * depth * 20.0)
        y2 = y1 + int(math.sin(math.radians(angle)) * depth * 20.0)


        #draw branch, flip display
        pygame.draw.line(screen, colour, (x1, y1), (x2, y2), width)
        pygame.display.flip()

        #set new colours for each branch
        #basically arbitrary, but mod 255 to fit RGB colour scheme
        newcolour1 = [(colour[0] - power[lvl])%255, 
                      (colour[1] + power[lvl])%255, 
                      (colour[2] - 0.5*power[lvl])%255]

        newcolour2 = [(colour[0] + power[lvl])%255, 
                      (colour[1] - power[lvl])%255, 
                      (colour[2] - 0.5*power[lvl])%255]

        #recursion to draw next two branches
        #angle modification ensures
        drawTree(x2, y2, angle - 10*power[lvl], depth - 1, newcolour1, lvl+1, width+2)
        drawTree(x2, y2, angle + 10*power[lvl], depth - 1, newcolour2, lvl+1, width+2)


#MAIN

#get soundfile as first command line argument
#or, write filename as string, ie soundfile = "A.wav"
soundfile = sys.argv[1]

#get the sampling frequency (int) and sampled sound file data
sampFreq, sound = wavfile.read(soundfile)
#sound is a nx2 numpy array 
#where n = the number of samples = (time length of sound file)/(sampling frequency)

#get the data type of the sound
#need to find out what data types are possible, modify sampled data normalization accordingly
print sound.dtype 

#Normalization (make it so that every element in the sound array is between -1 and 1)
#if snd.type = int16 = 16 bit signed integer -> range from -2^15 to 2^15 - 1
sound = sound/(2.**15)

#There are two columns in the array representing channels, presumably left and right ear
#(research this)
#choose the first column, should probably average both columns or something
s1 = sound[:,0]

#Perform Fast Fourier Transform
Sound = fft(s1)

#get the power spectrum (the magnitudes of the values in the Fourier array)
power = []
for val in Sound:
	power.append(abs(val))

#initialize pygame 
pygame.init()
infoObject = pygame.display.Info()
infoObject = pygame.display.Info()
window = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.display.set_caption("Fractal Tree")
screen = pygame.display.get_surface()
screen.fill((50,50,50))

#start music
pygame.mixer.music.load(soundfile)
pygame.mixer.music.play()

#start recursive algorithm
#drawTree(starting x, starting y, starting angle, maximum depth, starting colour, 
#         starting level, starting width)
#starting values arbitrary for now
drawTree(infoObject.current_w/2., infoObject.current_h, -90, 10, [125,125,125], 0, 2)
pygame.display.flip()
pygame.mixer.music.stop()

#take screenshot
pygame.image.save(screen,soundfile[0:len(soundfile)-4] + "_Tree.jpg")

#wait for user to press esacape before quitting
go = True
while go:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            go = False