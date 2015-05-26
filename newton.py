#newton fractal, saves screenshot
#look at fractaltree.py for explanations
import pygame, math, sys
from scipy.io import wavfile
from scipy import fft

#get soundfile as first command line argument
#or, write filename as string, ie soundfile = "A.wav"
soundfile = sys.argv[1]

#image size
imgx = 500
imgy = 500

#iitialize pygame
pygame.init()
window = pygame.display.set_mode((imgx, imgy))#,pygame.FULLSCREEN)
pygame.display.set_caption("Newton Fractal")
screen = pygame.display.get_surface()
screen.fill((0,0,0))
pygame.mouse.set_visible(False)

#initialize font
font = pygame.font.SysFont("timesnewroman", 24)

#draw text
screen.blit(font.render('Fourier transforming .wav file', 0, (255,255,255), (0,0,0)),[450,400])
pygame.display.flip()

#read and process .wav file
sampFreq, sound = wavfile.read(soundfile)
sound = sound/(2.**15)
s1 = sound[:,0]
Sound = fft(s1)

power = []
for val in Sound:
	power.append(abs(val))

screen.blit(font.render('Sorting fourier coefficients', 0, (255,255,255), (0,0,0)),[450,400])
pygame.display.flip()

#sorts into ascending order
#NOTE: every value is repeated once (by the natue of fourier transforming) ie power[0] = power[1], power[2] = power[3], etc.
power.sort(reverse = True)


screen.fill([0,0,0])
screen.blit(font.render('Creating Newton Fractal!', 0, (255,255,255), (0,0,0)),[450,400])
pygame.display.flip()

#drawing surface
xa = -1.0
xb = 1.0
ya = -1.0
yb = 1.0

maxIt = 20 # max iterations allowed
h = 1e-6 # step size for numerical derivative
eps = 1e-3 # max error allowed

#complex function that generates fractal
#arbitrary (to an extent)
#seeded by power
def f(z):

	[a,b,c,d,e] = [power[0]%25,power[2]%25,power[4]%25,power[6]%25,power[8]%25]

	return (z**a + z**b + z**c)/(z**d + e)

# iterate through every single pixel, draw circle
# wikipedia Newton Fractal for details of algorithm (well known fractal)
for y in range(imgy):
    zy = y * (yb - ya) / (imgy - 1) + ya #real part of z
    for x in range(imgx):
        zx = x * (xb - xa) / (imgx - 1) + xa #imaginary part of z
        z = complex(zx, zy) #complex number
        for i in range(maxIt):
            #complex derivative
            dz = (f(z + complex(h, h)) - f(z)) / complex(h, h)
            z0 = z - f(z) / dz # Newton iteration
            if abs(z0 - z) < eps: # stop when close enough to any root
                break
            z = z0
        pygame.draw.circle(screen, (i*power[i] % 4 * 64, i*power[i] % 8 * 32, i*power[i] % 16 * 16), (x,y), 0, 0)

pygame.display.flip()
pygame.image.save(screen,soundfile[0:len(soundfile)-4] + "_Newton.jpg")

#wait for user to press escape before entering
go = True
while go:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			go = False