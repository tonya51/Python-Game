import pygame, sys, time, random, os, math
from pygame.locals import *

pygame.init()

# BUTTONS
# Main menu buttons
BUTTON_SIZE = [270, 54]
BUTTON_POS = [428, 110]
# Options menu buttons
BUTTON_OPT_SIZE = [230, 46]
BUTTON_OPT_POS = [463, 221]
# Arrow buttons in help menu
BUTTON_ARR_POS = [453, 550]
BUTTON_ARR_SIZE = [100, 58]
# Help button
BUTTON_HELP_SIZE = [90, 22]
BUTTON_HELP_POS = [550, 15]

# OTHER OBJECTS
# Planets
PLANET_SIZE = [50,50]
# Droids
DROID_SIZE = [183,200]
DROID_POS = [0,95]
# C3PO's bubble
BUBBLE3_SIZE = [250,138]
BUBBLE3_POS = [-230,100]
# R2D2's bubble
BUBBLE2_SIZE = [150,83]
BUBBLE2_POS = [180,160]
# Health bar
BAR_POS = [836,5]
BAR_SIZE = [300, 43]

# TEXT
TEXT_SCORE_POS = [20,0]
TEXT_SPEED_POS = [270,0]
LETTER_COL = (255,238,90)
TEXT_QUESTION_POS = [390,485]
TEXT_QUESTION_COL = (58,6,6)
BINARY_Q_POS = [435, 430, 420, 410, 405, 400, 390, 380, 370]
TEXT_R2_POS = [813,503]
TEXT_R2_COL = (28,39,68)
TEXT_FINAL_POS = [800, 430, 350]
TEXT_FINAL_COL = (255,210,6)
TEXT_HS_POS = [840, 160]
TEXT_HS_COL = (53, 205, 0)
TEXT_BOARD_POS = [342, 64, 160, 560]#x|yyy#560]] #y+100
# Fonts
FONT = pygame.font.Font('fonts/Starjedi.ttf', 30)
FONT_Q = pygame.font.Font('fonts/Starjedi.ttf', 26)
FONT_R2 = pygame.font.Font('fonts/Starjedi.ttf', 25)
FONT_FINAL = pygame.font.Font('fonts/Star_Jedi_Rounded.ttf', 90)
FONT_HS = pygame.font.Font('fonts/ERASMD.ttf', 90)
FONT_BOARD = pygame.font.Font('fonts/Starjedi.ttf', 60)
FONT_ESC = pygame.font.Font('fonts/ERASBD.ttf', 24)

WIDTH = 1156
HEIGHT = 650
MAX_SCORE = 15
FINAL_LEVEL = 8
OPTIONS = [180, 120, 60]
NUMBER_SEQUENCE = [0, 1, 0]
TOTAL_HELP_PAGES = 3
PLANETS = 20

class Button(pygame.sprite.Sprite):
    def __init__(self, createX, createY, img, dimX, dimY):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(createX, createY, dimX, dimY)
        self.image = pygame.image.load(img).convert_alpha()
        self.transImage = pygame.transform.scale(self.image, (dimX, dimY))
        self.dimX = dimX
        self.dimY = dimY
        self.litUp = 0

    def drawIt(self, surf):
        surf.blit(self.transImage, self.rect)

    def lightUp(self, surf, lightSwitch, img):
        if lightSwitch==1:
            self.image = pygame.image.load(img+'on.png').convert_alpha()
        else:
            self.image = pygame.image.load(img+'.png').convert_alpha()
        self.litUp = lightSwitch
        self.transImage = pygame.transform.scale(self.image, (self.dimX, self.dimY))

class Planet(pygame.sprite.Sprite):
    def __init__(self, createX, createY, dirX, surf, number, generalSpeed):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(createX, createY, PLANET_SIZE[0], PLANET_SIZE[1])
        self.number = number
        self.image = pygame.image.load('images/planets/planet'+str(number)+'.png').convert_alpha()
        self.transImage = pygame.transform.scale(self.image, (PLANET_SIZE[0], PLANET_SIZE[1]))
        self.speedX = generalSpeed
        self.dirX = dirX
        self.litUp = 0

    def move(self, surf):
        self.rect.left += self.dirX * self.speedX
        surf.blit(self.transImage, self.rect)

    def lightUp(self, surf, lightSwitch, imgPlanet, dimX=PLANET_SIZE[0], dimY=PLANET_SIZE[1]):
        if lightSwitch==0:
            self.image = pygame.image.load('images/planets/planet'+str(imgPlanet)+'.png').convert_alpha()
        else:
            self.image = pygame.image.load('images/planets/planet'+str(imgPlanet)+'l.png').convert_alpha()
        self.litUp = lightSwitch
        self.transImage = pygame.transform.scale(self.image, (dimX, dimY))
            
class Droid(pygame.sprite.Sprite):
    def __init__(self, createX, createY, dimX=DROID_SIZE[0], dimY=DROID_SIZE[1]):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(createX, createY, dimX, dimY)
        self.image = pygame.image.load('images/droids/r2&3po2.png').convert_alpha()
        self.transImage = pygame.transform.scale(self.image, (dimX, dimY))

    def drawIt(self, surf):
        surf.blit(self.transImage, self.rect)

class SpeechBubble(pygame.sprite.Sprite):
    def __init__(self, createX, createY, img, dimX, dimY):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(createX, createY, dimX, dimY)
        self.image = pygame.image.load(img).convert_alpha()
        self.transImage = pygame.transform.scale(self.image, (dimX, dimY))
        self.dimX = dimX
        self.dimY = dimY

    def changeBubble(self, tick):
        if tick == 0:
            self.image = pygame.image.load('images/droids/sb'+str(random.randint(1,4))+'.png').convert_alpha()
        elif tick == 1:
            self.image = pygame.image.load('images/droids/sbc.png').convert_alpha()
        else:
            self.image = pygame.image.load('images/droids/sbr'+str(tick)+'.png').convert_alpha()
        self.transImage = pygame.transform.scale(self.image, (self.dimX, self.dimY))        

    def drawIt(self, surf):
        surf.blit(self.transImage, self.rect)

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, createX, createY, img, dimX, dimY, maxTime):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(createX, createY, dimX, dimY)
        self.image = pygame.image.load(img).convert_alpha()
        self.transImage = pygame.transform.scale(self.image, (dimX, dimY))
        self.maxTime = maxTime
        
    def drawIt(self, surf, sec):
        self.image = pygame.image.load('images/bars/bar'+str(self.maxTime)+'/bar('+str(self.maxTime-sec)+').png')
        self.transImage = pygame.transform.scale(self.image, (BAR_SIZE[0], BAR_SIZE[1]))
        surf.blit(self.transImage, self.rect)

class Text(pygame.sprite.Sprite):
    def __init__(self, createX, createY, font, showText, color):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.color = color
        self.rect = pygame.Rect(createX, createY, 1, 1)
        self.text = self.font.render(showText, 0, self.color)

    def renderText(self, showText):
        self.text = self.font.render(showText, 0, self.color)
        
    def drawIt(self, surf, createX):
        if createX != 0:
            self.rect.left = createX
        surf.blit(self.text, self.rect)

def checkArea(area, x, y):
    if x>area.rect.left and x<area.rect.right and y>area.rect.top and y<area.rect.bottom:
        return True

def generateBinaryNumber(minBinary, maxBinary, suc, numberSequence, level):    
    if level == 1 and suc >= 0 and suc <= 3:
        sBinary = [0]
        sBinary[0] = NUMBER_SEQUENCE[numberSequence+(suc%2)]
    elif (level == 1 and suc >= 6 and suc <= 11) or (level == 2 and suc >= 15 and suc <= 18):
        sBinary = [1, 0]
        sBinary[1] = NUMBER_SEQUENCE[numberSequence+(suc%2)]
    else:
        n = random.randint(minBinary, maxBinary)
        sBinary = [random.randint(0,1) for i in range(n)]
        if n > 1 and sBinary[0] == 0:
            sBinary[0] = 1
    return sBinary

def getDecimalAnswer(binary):
    d = 0
    for i in range(len(binary)):
        d = d + binary[i]*pow(2,len(binary)-1-i)
    #print(d)
    return d

def checkTooMany(sumPlanets):
    x = random.randint(0,9)
    while sumPlanets[x] >= 3:
        x += 1
        if x == 10:
            x = 0
    return x

def adjustMinMaxBin(successes, level, minBinary, maxBinary):
    if level != FINAL_LEVEL:
        if successes >= 0 and successes <= 0.2*MAX_SCORE-1:
            minBinary = level
            maxBinary = level
        elif successes >= 0.2*MAX_SCORE and successes <= 0.4*MAX_SCORE-1:
            minBinary = level
            maxBinary = level + 1
        elif successes >= 0.4*MAX_SCORE and successes <= 0.6*MAX_SCORE-1:
            minBinary = level + 1
            maxBinary = level + 1
        elif successes >= 0.6*MAX_SCORE and successes <= 0.8*MAX_SCORE-1:
            minBinary = level + 1
            maxBinary = level + 2
        elif successes >= 0.8*MAX_SCORE and successes <= MAX_SCORE-1:
            minBinary = level + 2
            maxBinary = level + 2
    else:
        minBinary = FINAL_LEVEL
        maxBinary = FINAL_LEVEL+1
    #print('Suc = ',successes,' / Level = ',level,' / ',minBinary,'~',maxBinary)
    return [minBinary, maxBinary]

def viewScores():
    hs = open("hs.txt", "r")
    scoreList = hs.read()
    scoreList = scoreList.split()
    hs.close()
    return scoreList

def updateScores(score):
    sl = viewScores()
    scoreListNum = [0 for i in range(5)]
    for i in range(5):
        scoreListNum[i] = int(sl[i])
    if score > scoreListNum[0]:
        scoreListNum[0] = score
    scoreListNum.sort()

    for i in range(5):
        sl[i] = str(scoreListNum[i])

    hs = open("hs.txt", "w+")
    hs.write(sl[0]+' '+sl[1]+' '+sl[2]+' '+sl[3]+' '+sl[4])
    hs.close()
    return scoreListNum[4]
