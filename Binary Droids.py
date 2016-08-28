import pygame, sys, time, random, os, math, droidGame
from pygame.locals import *
from droidGame import *

#os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (101,31)

pygame.init()
mainClock = pygame.time.Clock()
stage = 0
newStage = 1
level = 1

# Set window and background image
wSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('The Adventures Of The Droids')
image = pygame.image.load('images/bg/xX2GRj6.png').convert_alpha()
transImage = pygame.transform.scale(image, (WIDTH, HEIGHT))
wSurface.blit(transImage, (0,0))

planet = [0 for i in range(PLANETS)]
litUp = [0 for i in range(PLANETS)]
buttons = [0 for i in range(5)]
buttonsOpt = [0 for i in range(3)]
buttonsArr = [0 for i in range(3)]
scoreBoard = [0 for i in range(6)]
generalSpeed = 1
minBinary = 1
maxBinary = 1
successes = 0
maxTime = 180
page = 1
correctAnswer = 0

# Add health bar
bar = HealthBar(BAR_POS[0],BAR_POS[1],'images/bars/bar'+str(maxTime)+'/bar(60).png',BAR_SIZE[0],BAR_SIZE[1], maxTime)

# Add droids and their speech bubbles
wSCenterX = wSurface.get_rect().centerx
wSCenterY = wSurface.get_rect().centery
d1 = Droid(wSCenterX+DROID_POS[0], wSCenterY+DROID_POS[1])
b1 = SpeechBubble(wSCenterX+BUBBLE3_POS[0], wSCenterY+BUBBLE3_POS[1], 'images/droids/sb'+str(random.randint(1,4))+'.png', BUBBLE3_SIZE[0], BUBBLE3_SIZE[1])
b2 = SpeechBubble(wSCenterX+BUBBLE2_POS[0], wSCenterY+BUBBLE2_POS[1], 'images/droids/sbr2.png', BUBBLE2_SIZE[0], BUBBLE2_SIZE[1])

# Add text on screen
# Score
score = 0
textScore = Text(TEXT_SCORE_POS[0], TEXT_SCORE_POS[1], FONT, 'Score: '+str(score), LETTER_COL)
textQuestion = Text(BINARY_Q_POS[0], TEXT_QUESTION_POS[1], FONT_Q, '', TEXT_QUESTION_COL)
# R2D2's bubble message
onWait = 0
textR2 = Text(TEXT_R2_POS[0], TEXT_R2_POS[1], FONT_R2, '', TEXT_R2_COL)
textSpeed = Text(TEXT_SPEED_POS[0], TEXT_SPEED_POS[1], FONT, 'Speed: x '+str(generalSpeed), LETTER_COL)
finalScoreText =  Text(TEXT_FINAL_POS[0], TEXT_FINAL_POS[1], FONT_FINAL, '', TEXT_FINAL_COL)
highScoreText = Text(TEXT_HS_POS[0], TEXT_HS_POS[1], FONT_HS, '', TEXT_HS_COL)
highScore = int(viewScores()[4])

# Create menu buttons
for i in range(5):
    buttons[i] = Button(BUTTON_POS[0], BUTTON_POS[1]+(i*94), 'images/buttons/button'+str(i+1)+'.png', BUTTON_SIZE[0], BUTTON_SIZE[1])

# Create options buttons
for i in range(3):
    buttonsOpt[i] = Button(BUTTON_OPT_POS[0], BUTTON_OPT_POS[1]+(i*81), 'images/buttons/options'+str(i+1)+'.png', BUTTON_OPT_SIZE[0], BUTTON_OPT_SIZE[1])

# Create scores board
scoreBoard[0] = Text(TEXT_BOARD_POS[0], TEXT_BOARD_POS[1], FONT_BOARD, 'score board', TEXT_FINAL_COL)
for i in range(1,6):
    scoreBoard[i] = Text(TEXT_BOARD_POS[0]+153, TEXT_BOARD_POS[2]+((i-1)*70), FONT_BOARD, '', TEXT_FINAL_COL)

# Create arrow help buttons
buttonsArr[0] = Button(BUTTON_ARR_POS[0], BUTTON_ARR_POS[1], 'images/buttons/next0.png', BUTTON_ARR_SIZE[0], BUTTON_ARR_SIZE[1])
buttonsArr[1] = Button(BUTTON_ARR_POS[0]+BUTTON_ARR_SIZE[0]+50, BUTTON_ARR_POS[1], 'images/buttons/next1.png', BUTTON_ARR_SIZE[0], BUTTON_ARR_SIZE[1])
buttonsArr[2] = Button(BUTTON_ARR_POS[0]+65, BUTTON_ARR_POS[1], 'images/buttons/next0.png', BUTTON_ARR_SIZE[0], BUTTON_ARR_SIZE[1])

buttonHelp = Button(BUTTON_HELP_POS[0], BUTTON_HELP_POS[1], 'images/buttons/help.png', BUTTON_HELP_SIZE[0], BUTTON_HELP_SIZE[1])

pygame.mixer.music.set_volume(0.3)

pygame.display.update()

while True:
    if stage == 0:
        
        if newStage == 1:
            image = pygame.image.load('images/bg/xX2GRj6.png').convert_alpha()
            transImage = pygame.transform.scale(image, (WIDTH, HEIGHT))
            newStage = 0
            numberSequence = random.randint(0, 1)
            binary = generateBinaryNumber(1, 1, successes, numberSequence, level)
            strBinary = ''.join([str(binary[i]) for i in range(len(binary))])
            decimal = getDecimalAnswer(binary)
            textQuestion.renderText(strBinary)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                for i in range(5):
                    if checkArea(buttons[i], mouseX, mouseY):
                        stage = i+3
                        newStage = 1
    
        (mouseX, mouseY) = pygame.mouse.get_pos()
        for i in range(5):
            if checkArea(buttons[i], mouseX, mouseY):
                if buttons[i].litUp == 0:
                    buttons[i].lightUp(wSurface, 1, 'images/buttons/button'+str(i+1))
            else:
                if buttons[i].litUp == 1:
                    buttons[i].lightUp(wSurface, 0, 'images/buttons/button'+str(i+1))

        wSurface.blit(transImage, (0,0))

        sumPlanets = [0 for i in range(10)]
        
        for i in range(5):
            buttons[i].drawIt(wSurface)

    elif stage == 1:

        if newStage == 1:
            if level == 1:
                for i in range(PLANETS):
                    x = checkTooMany(sumPlanets)
                    planet[i] = Planet(random.randint(0, WIDTH-70), random.randint(60, HEIGHT-310), pow(-1,random.randint(0,1)), wSurface, x, generalSpeed)     
                    sumPlanets[x] += 1
            image = pygame.image.load('images/bg/'+str(level)+'.jpg').convert_alpha()
            transImage = pygame.transform.scale(image, (WIDTH, HEIGHT))
            newStage = 0
            startTime = pygame.time.get_ticks()
            sec = 0

        if correctAnswer == 1:
            if pygame.time.get_ticks() - p > 300:
                correctAnswer = 0
                b1.changeBubble(0)
                textQuestion.renderText(strBinary)
                if decimal > 9 and decimal < 100:
                    b2.changeBubble(2)
                elif decimal > 99:
                    b2.changeBubble(3)
                    
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
            if event.type == MOUSEBUTTONDOWN:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                for i in range(PLANETS):
                    if checkArea(planet[i], mouseX, mouseY):
                        if decimal < 10:
                            if planet[i].number == decimal:

                                sumPlanets[planet[i].number] -= 1
                                x = checkTooMany(sumPlanets)
                                direction = pow(-1,random.randint(0,1))
                                if direction == 1:
                                    planet[i] = Planet(-50, random.randint(60, HEIGHT-310), direction, wSurface, x, generalSpeed)
                                elif direction == -1:
                                    planet[i] = Planet(WIDTH, random.randint(60, HEIGHT-310), direction, wSurface, x, generalSpeed)   
                                sumPlanets[x] += 1

                                if successes < MAX_SCORE - 1:
                                    successes += 1
                                
                                score += generalSpeed

                                if score >= level*MAX_SCORE:
                                    level += 1
                                    if level < 9:
                                        stage = 3
                                    else:
                                        stage = 2
                                    newStage = 1
                                    successes = 0

                                pygame.mixer.music.load('sounds/Playful R2D2.mp3')
                                pygame.mixer.music.play(0)

                                p = pygame.time.get_ticks()
                                b1.changeBubble(1)
                                textQuestion.renderText('')
                                correctAnswer = 1
                                
                                if sec > level:
                                    startTime += (level + 1)*1000 + 300
                                    sec -= level + 1
                                else:
                                    startTime += sec*1000
                                    sec = 0
                                minBinary = adjustMinMaxBin(successes, level, minBinary, maxBinary)[0]
                                maxBinary = adjustMinMaxBin(successes, level, minBinary, maxBinary)[1]
                                binary = generateBinaryNumber(minBinary, maxBinary, successes, numberSequence, level)
                                strBinary = ''.join([str(binary[i]) for i in range(len(binary))])
                                decimal = getDecimalAnswer(binary)
                            else:
                                pygame.mixer.music.load('sounds/Surprised R2D2.mp3')
                                pygame.mixer.music.play(0)
                                if sec < maxTime:
                                    startTime -= 2000
                                    sec += 1

                        elif decimal < 100:
                            if onWait == 0:
                                if planet[i].number==decimal//10:
                                    textR2.renderText(str(decimal//10))
                                    
                                    sumPlanets[planet[i].number] -= 1
                                    x = checkTooMany(sumPlanets)
                                    direction = pow(-1,random.randint(0,1))
                                    if direction == 1:
                                        planet[i] = Planet(-50, random.randint(60, HEIGHT-310), direction, wSurface, x, generalSpeed)
                                    elif direction == -1:
                                        planet[i] = Planet(WIDTH, random.randint(60, HEIGHT-310), direction, wSurface, x, generalSpeed)
                                    sumPlanets[x] += 1
                                    
                                    onWait = 1
                                else:
                                    pygame.mixer.music.load('sounds/Surprised R2D2.mp3')
                                    pygame.mixer.music.play(0)
                                    if sec < maxTime:
                                        startTime -= 2000
                                        sec += 1

                            elif onWait == 1:
                                textR2.renderText('')
                                onWait = 0
                                if planet[i].number == decimal%10:

                                    sumPlanets[planet[i].number] -= 1
                                    x = checkTooMany(sumPlanets)
                                    direction = pow(-1,random.randint(0,1))
                                    if direction == 1:
                                        planet[i] = Planet(-50, random.randint(60, HEIGHT-310), direction, wSurface, x, generalSpeed)
                                    elif direction == -1:
                                        planet[i] = Planet(WIDTH, random.randint(60, HEIGHT-310), direction, wSurface, x, generalSpeed)
                                    sumPlanets[x] += 1

                                    if successes < MAX_SCORE:
                                        successes += 1
                                
                                    score += generalSpeed

                                    if score >= level*MAX_SCORE:
                                        level += 1
                                        if level < 9:
                                            stage = 3
                                        else:
                                            stage = 2
                                        newStage = 1
                                        successes = 0

                                    pygame.mixer.music.load('sounds/Playful R2D2.mp3')
                                    pygame.mixer.music.play(0)
                                    
                                    p = pygame.time.get_ticks()
                                    b1.changeBubble(1)
                                    textQuestion.renderText('')
                                    correctAnswer = 1
                                    
                                    if sec > level:
                                        startTime += (level + 1)*1000 + 300
                                        sec -= level + 1
                                    else:
                                        startTime += sec*1000
                                        sec = 0
                                    minBinary = adjustMinMaxBin(successes, level, minBinary, maxBinary)[0]
                                    maxBinary = adjustMinMaxBin(successes, level, minBinary, maxBinary)[1]
                                    binary = generateBinaryNumber(minBinary, maxBinary, successes, numberSequence, level)
                                    strBinary = ''.join([str(binary[i]) for i in range(len(binary))])
                                    decimal = getDecimalAnswer(binary)
                                else:
                                    pygame.mixer.music.load('sounds/Surprised R2D2.mp3')
                                    pygame.mixer.music.play(0)
                                    if sec < maxTime:
                                        startTime -= 2000
                                        sec += 1

                        else:
                            if onWait == 0:
                                if planet[i].number == decimal//100:
                                    textR2.renderText(str(decimal//100))
                                    
                                    sumPlanets[planet[i].number] -= 1
                                    x = checkTooMany(sumPlanets)
                                    direction = pow(-1,random.randint(0,1))
                                    if direction == 1:
                                        planet[i] = Planet(-50, random.randint(60, HEIGHT-310), direction, wSurface, x, generalSpeed)
                                    elif direction == -1:
                                        planet[i] = Planet(WIDTH, random.randint(60, HEIGHT-310), direction, wSurface, x, generalSpeed)
                                    sumPlanets[x] += 1
                                    
                                    onWait = 1
                                else:
                                    pygame.mixer.music.load('sounds/Surprised R2D2.mp3')
                                    pygame.mixer.music.play(0)
                                    if sec < maxTime:
                                        startTime -= 2000
                                        sec += 1

                            elif onWait == 1:
                                if planet[i].number==(decimal%100)//10:
                                    textR2.renderText(str(decimal//100)+' '+str((decimal%100)//10))

                                    sumPlanets[planet[i].number] -= 1 
                                    x = checkTooMany(sumPlanets)
                                    direction = pow(-1,random.randint(0,1))
                                    if direction == 1:
                                        planet[i] = Planet(-50, random.randint(60, HEIGHT-310), direction, wSurface, x, generalSpeed)
                                    elif direction == -1:
                                        planet[i] = Planet(WIDTH, random.randint(60, HEIGHT-310), direction, wSurface, x, generalSpeed)
                                    sumPlanets[x] += 1

                                    onWait = 2
                                else:
                                    textR2.renderText('')
                                    pygame.mixer.music.load('sounds/Surprised R2D2.mp3')
                                    pygame.mixer.music.play(0)
                                    if sec < maxTime:
                                        startTime -= 2000
                                        sec += 1
                                    onWait = 0

                            else:
                                textR2.renderText('')
                                onWait = 0
                                if planet[i].number==decimal%10:
                                    sumPlanets[planet[i].number] -= 1
                                    x = checkTooMany(sumPlanets)
                                    direction = pow(-1,random.randint(0,1))
                                    if direction == 1:
                                        planet[i] = Planet(-50, random.randint(60, HEIGHT-310), direction, wSurface, x, generalSpeed)
                                    elif direction == -1:
                                        planet[i] = Planet(WIDTH, random.randint(60, HEIGHT-310), direction, wSurface, x, generalSpeed)
                                    sumPlanets[x] += 1

                                    if successes < MAX_SCORE:
                                        successes += 1
                                
                                    score += generalSpeed

                                    if score >= level*MAX_SCORE:
                                        level += 1
                                        if level < 9:
                                            stage = 3
                                        else:
                                            stage = 2
                                        newStage = 1
                                        successes = 0

                                    pygame.mixer.music.load('sounds/Playful R2D2.mp3')
                                    pygame.mixer.music.play(0)
                                    
                                    p = pygame.time.get_ticks()
                                    b1.changeBubble(1)
                                    textQuestion.renderText('')
                                    correctAnswer = 1
                                    
                                    if sec > level:
                                        startTime += (level + 1)*1000 + 300
                                        sec -= level + 1
                                    else:
                                        startTime += sec*1000
                                        sec = 0
                                    minBinary = adjustMinMaxBin(successes, level, minBinary, maxBinary)[0]
                                    maxBinary = adjustMinMaxBin(successes, level, minBinary, maxBinary)[1]
                                    binary = generateBinaryNumber(minBinary, maxBinary, successes, numberSequence, level)
                                    strBinary = ''.join([str(binary[i]) for i in range(len(binary))])
                                    decimal = getDecimalAnswer(binary)
                                else:
                                    pygame.mixer.music.load('sounds/Surprised R2D2.mp3')
                                    pygame.mixer.music.play(0)
                                    if sec < maxTime:
                                        startTime -= 2000
                                        sec += 1
                                
                        textScore.renderText('Score: '+str(score))

                if (decimal > 9 and decimal < 100 and onWait == 0) or (decimal > 99 and onWait < 2):
                    if checkArea(buttonHelp, mouseX, mouseY):
                        score -= 1
                        if score >= 0:
                            pygame.mixer.music.load('sounds/Proud R2D2.mp3')
                            pygame.mixer.music.play(0)
                        if decimal < 100:
                            if onWait == 0:
                                textR2.renderText(str(decimal//10))
                                onWait = 1
                            else:
                                textR2.renderText('')
                                onWait = 0
                                b1.changeBubble(0)
                                binary = generateBinaryNumber(minBinary, maxBinary, successes, numberSequence, level)
                                strBinary = ''.join([str(binary[i]) for i in range(len(binary))])
                                decimal = getDecimalAnswer(binary)
                                textQuestion.renderText(strBinary)
                        else:
                            if onWait == 0:
                                textR2.renderText(str(decimal//100))
                                onWait = 1
                            elif onWait == 1:
                                textR2.renderText(str(decimal//100)+' '+str((decimal%100)//10))
                                onWait = 2
                            else:
                                textR2.renderText('')
                                onWait = 0
                                b1.changeBubble(0)
                                binary = generateBinaryNumber(minBinary, maxBinary, successes, numberSequence, level)
                                strBinary = ''.join([str(binary[i]) for i in range(len(binary))])
                                decimal = getDecimalAnswer(binary)
                                textQuestion.renderText(strBinary)
                        if score >= 0:
                            textScore.renderText('Score: '+str(score))

            if event.type == KEYDOWN:
                if event.unicode == '+' and generalSpeed < 5:
                    for i in range(PLANETS):
                        planet[i].speedX += 1
                    generalSpeed += 1
                    textSpeed.renderText('Speed: x '+str(generalSpeed))
                if event.unicode == '-' and generalSpeed > 1:
                    for i in range(PLANETS):
                        planet[i].speedX -= 1
                    generalSpeed -= 1
                    textSpeed.renderText('Speed: x '+str(generalSpeed))
                if event.key == K_ESCAPE:
                    stage = 0
                    newStage = 1
                    level = 1
                    score = 0
                    generalSpeed = 1
                    successes = 0
                    textSpeed.renderText('Speed: x 1')
                    textScore.renderText('Score: 0')

        wSurface.blit(transImage, (0,0))
        textScore.drawIt(wSurface, 0)
        textSpeed.drawIt(wSurface, 0)

        d1.drawIt(wSurface)
        b1.drawIt(wSurface)
        if decimal > 9:
            b2.drawIt(wSurface)
            textR2.drawIt(wSurface, 0)
            if (decimal < 100 and onWait == 0) or (decimal > 99 and onWait < 2):
                buttonHelp.drawIt(wSurface)

        (mouseX, mouseY) = pygame.mouse.get_pos()

        if (decimal > 9 and decimal < 100 and onWait == 0) or (decimal > 99 and onWait < 2):
            if checkArea(buttonHelp, mouseX, mouseY):
                if buttonHelp.litUp == 0:
                    buttonHelp.lightUp(wSurface, 1, 'images/buttons/help')
            else:
                if buttonHelp.litUp == 1:
                    buttonHelp.lightUp(wSurface, 0, 'images/buttons/help')

        for i in range(PLANETS):
            if checkArea(planet[i], mouseX, mouseY):
                if planet[i].litUp == 0:
                    planet[i].lightUp(wSurface, 1, planet[i].number)
            else:
                if planet[i].litUp == 1:
                    planet[i].lightUp(wSurface, 0, planet[i].number)
                    
            if (planet[i].rect.right<0 and planet[i].dirX==-1) or (planet[i].rect.left>WIDTH and planet[i].dirX==1):
                sumPlanets[planet[i].number] -= 1
                x = checkTooMany(sumPlanets)
                direction = pow(-1,random.randint(0,1))
                if direction == 1:
                    planet[i] = Planet(-50, random.randint(60, HEIGHT-310), direction, wSurface, x, generalSpeed)
                elif direction == -1:
                    planet[i] = Planet(WIDTH, random.randint(60, HEIGHT-310), direction, wSurface, x, generalSpeed)
                sumPlanets[x] += 1
            
            planet[i].move(wSurface)

        if pygame.time.get_ticks() >= (sec*1000)+startTime:
            sec += 1

        textQuestion.drawIt(wSurface, BINARY_Q_POS[len(strBinary)-1])
        
        if sec > maxTime or score < 0:
            stage = 2
            newStage = 1
            level = FINAL_LEVEL+1
            
            if score < 0:
                score = 0
        else:
            bar.drawIt(wSurface, sec)

    elif stage == 2:
        if newStage == 1:
            t = pygame.time.get_ticks()
            k = ''
            if level == FINAL_LEVEL+2 or level == FINAL_LEVEL+1:
                finalScoreText.renderText(str(score))
                finalScoreText.rect.top = TEXT_FINAL_POS[level-FINAL_LEVEL]
                if score > highScore:
                    k = 'b'
                else:
                    k = 'a'
                highScore = updateScores(score)
            image = pygame.image.load('images/bg/level'+str(level)+k+'.jpg').convert_alpha()
            transImage = pygame.transform.scale(image, (WIDTH, HEIGHT))
            newStage = 0
            
        wSurface.blit(transImage, (0,0))
        if level == FINAL_LEVEL+2 or level == FINAL_LEVEL+1:
            finalScoreText.drawIt(wSurface, 0)
        if level != FINAL_LEVEL+1 and level != FINAL_LEVEL+2 and pygame.time.get_ticks() - t > 1500:
            stage = 1
            newStage = 1
        if (level == FINAL_LEVEL+1 or level == FINAL_LEVEL+2) and pygame.time.get_ticks() - t > 4000:
            stage = 0
            score = 0
            newStage = 1
            level = 1
            generalSpeed = 1
            successes = 0
            textSpeed.renderText('Speed: x 1')
            textScore.renderText('Score: 0')

    elif stage == 3:
        if newStage == 1:
            image = pygame.image.load('images/bg/bef'+str(level-1)+'.jpg').convert_alpha()
            transImage = pygame.transform.scale(image, (WIDTH, HEIGHT))
            newStage = 0
            if level == 1:
                highScoreText.renderText(str(highScore))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                stage = 2
                newStage = 1

        wSurface.blit(transImage, (0,0))
        if level == 1:
            highScoreText.drawIt(wSurface, 0)

    elif stage == 4: #options
        if newStage == 1:
            image = pygame.image.load('images/bg/xX2GRj6.png').convert_alpha()
            transImage = pygame.transform.scale(image, (WIDTH, HEIGHT))
            newStage = 0

        (mouseX, mouseY) = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                for i in range(3):
                    if checkArea(buttonsOpt[i], mouseX, mouseY):
                        stage = 0
                        maxTime = OPTIONS[i]
                        newStage = 1

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:            
                    stage = 0
                    newStage = 1

        for i in range(3):
            if checkArea(buttonsOpt[i], mouseX, mouseY):
                if buttonsOpt[i].litUp == 0:
                    buttonsOpt[i].lightUp(wSurface, 1, 'images/buttons/options'+str(i+1))
            else:
                if buttonsOpt[i].litUp == 1:
                    buttonsOpt[i].lightUp(wSurface, 0, 'images/buttons/options'+str(i+1))

        wSurface.blit(transImage, (0,0))

        for i in range(3):
            buttonsOpt[i].drawIt(wSurface)

    elif stage == 5: #scores
        if newStage == 1:
            image = pygame.image.load('images/bg/xX2GRj6.png').convert_alpha()
            transImage = pygame.transform.scale(image, (WIDTH, HEIGHT))
            newStage = 0
            scoreList = viewScores()
            for i in range(1,6):
                scoreBoard[i].renderText(str(i)+'. '+scoreList[5-i])
                    
        (mouseX, mouseY) = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:            
                    stage = 0
                    newStage = 1

            if event.type == MOUSEBUTTONDOWN:
                if checkArea(buttonsArr[2], mouseX, mouseY):
                    stage = 0
                    newStage = 1

        if checkArea(buttonsArr[2], mouseX, mouseY):
            if buttonsArr[2].litUp == 0:
                buttonsArr[2].lightUp(wSurface, 1, 'images/buttons/next0')
        else:
            if buttonsArr[2].litUp == 1:
                buttonsArr[2].lightUp(wSurface, 0, 'images/buttons/next0')
        
        wSurface.blit(transImage, (0,0))
        for i in range(6):
            scoreBoard[i].drawIt(wSurface, 0)
        buttonsArr[2].drawIt(wSurface)

    elif stage == 6: #help
        if newStage == 1:
            image = pygame.image.load('images/bg/help'+str(page)+'.jpg').convert_alpha()
            transImage = pygame.transform.scale(image, (WIDTH, HEIGHT))
            newStage = 0

        (mouseX, mouseY) = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:            
                    stage = 0
                    newStage = 1
                
            if event.type == MOUSEBUTTONDOWN:
                if page == 1:
                    if checkArea(buttonsArr[0], mouseX, mouseY):
                        stage = 0
                        newStage = 1
                    if checkArea(buttonsArr[1], mouseX, mouseY):
                        page = 2
                        newStage = 1
                elif page < TOTAL_HELP_PAGES:
                    if checkArea(buttonsArr[1], mouseX, mouseY):
                        page += 1
                        newStage = 1
                    if checkArea(buttonsArr[0], mouseX, mouseY):
                        page -= 1
                        newStage = 1
                else:
                    if checkArea(buttonsArr[0], mouseX, mouseY):
                        page = TOTAL_HELP_PAGES - 1
                        newStage = 1

        for i in range(2):
            if checkArea(buttonsArr[i], mouseX, mouseY):
                if buttonsArr[i].litUp == 0:
                    buttonsArr[i].lightUp(wSurface, 1, 'images/buttons/next'+str(i))
            else:
                if buttonsArr[i].litUp == 1:
                    buttonsArr[i].lightUp(wSurface, 0, 'images/buttons/next'+str(i))
        
        wSurface.blit(transImage, (0,0))
        if page == 1:
            buttonsArr[0].drawIt(wSurface)
            buttonsArr[1].drawIt(wSurface)
        elif page == TOTAL_HELP_PAGES:
            buttonsArr[0].drawIt(wSurface)
        else:
            buttonsArr[0].drawIt(wSurface)
            buttonsArr[1].drawIt(wSurface)

    elif stage == 7:
        pygame.quit()
        sys.exit()
         
    pygame.display.update()
    mainClock.tick(100)
