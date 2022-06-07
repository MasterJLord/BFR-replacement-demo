import pygame, sys, random
from pygame.locals import *
pygame.init()
clock=pygame.time.Clock()
screen=pygame.display.set_mode((1200,800))

#variables setup
IgnorePresses = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
FullLibrary = {
    "strike":"strike.png",
    "defend":"defend.png",
    "bonk":"bash.png",
    "heal":"BandageUp.png",
    "up":"up.png",
    "down":"down.png"
}
SongSyncing = [
    (1,100), (3, 450), (2, 800), (2, 1050), (2, 1250), (3, 1650), (3, 2000), (1, 2350), (1, 2600), (1, 2850), (3, 3200), (3, 3600), (1, 3950), (1, 4200), (1, 4450), (4, 4800), (3, 5200), (1, 5550), (1, 5800), (1, 6050), (4, 6400), (3, 6800), (1, 7150), (1, 7400), (1, 7650),
    (2, 8000), (2, 8400), (1, 8750), (1, 9000), (1, 9250), (2, 9600), (2, 10000), (3, 10350), (3, 10600), (3, 10850),
    (4, 11200),  (2, 11400),  (1, 11600),  (1, 11800),  (3, 12000),  (3, 12200),  (2, 12400),  (2, 12600),  #beats for every note was overwhelming here, just playing the cards 4 times in .4 seconds was difficult without reading them, notes could be added back in between every other one of these though
    (4, 12800), (2, 13200), (3, 13550), (3, 13800), (3, 14050), (2, 14400), (2, 14800), (3, 15150), (3, 15400), (3, 15650), (2, 16000), (2, 16400), (1, 16750), (1, 17000), (1, 17250), (2, 17600), (2, 18000), (3, 18350), (3, 18600), (3, 18850),
    (2, 19200), (2, 19450), (4, 19850), (2, 20250), (1, 20400), (1, 20550), (1, 20700), (3, 20850), (3, 21000),
    (4, 21400), (2, 21800), (1, 21950), (1, 22100), (1, 22250), (3, 22400)
    #4  2 1 1 1 3
]
#1: energy, circle, 2: draw, triangle, 3: play, square, 4: attack, vertical line
TimeElapsed = 0
Hand=[]
Discard = []
QueuedCard = 0
Energy = 3
MaxEnergy = 4
EnemyHealth = 20
MyHealth = 15
YPosition = random.randint(0, 1)
XPosition = random.randint(0, 1)
Targeted = random.randint(0, 1)
deck = ["strike", "defend", "heal", "bonk", "defend", "strike", "strike", "bonk",  "up", "down", "up", "down", "up", "down"]

#function definition
def strike():
    global Energy
    global EnemyHealth
    global QueuedCard
    global Discard
    if Energy > 0:
        Energy -= 1
        EnemyHealth -= 6
        Discard.append(QueuedCard)
        QueuedCard = 0
def defend():
    global Energy
    global MyHealth
    global QueuedCard
    global Discard
    if Energy > 0:
        Energy -= 1
        MyHealth += 5
        Discard.append(QueuedCard)
        QueuedCard = 0
def bonk():
    global Energy
    global EnemyHealth
    global QueuedCard
    global Discard
    if Energy > 1:
        Energy -= 2
        EnemyHealth -= 8
        Discard.append(QueuedCard)
        QueuedCard = 0
def heal():
    global MyHealth
    global QueuedCard
    global Discard
    MyHealth += 4
    Discard.append(QueuedCard)
    QueuedCard = 0
def up():
    global Energy
    global YPosition
    global QueuedCard
    global Discard
    if Energy > 0:
        Energy -= 1
        if YPosition != 0:
            YPosition -= 1
        Discard.append(QueuedCard)
        QueuedCard = 0
def down():
    global Energy
    global YPosition
    global QueuedCard
    global Discard
    if Energy > 0:
        Energy -= 1
        if YPosition != 1:
            YPosition += 1
        Discard.append(QueuedCard)
        QueuedCard = 0

#function assigning
FunctionNames = {
    "strike":strike,
    "defend":defend,
    "bonk":bonk,
    "heal":heal,
    "up":up,
    "down":down
}

#game setup
random.shuffle(deck)
for p in FullLibrary.keys():
    FullLibrary[p] = pygame.transform.scale(pygame.image.load(FullLibrary[p]), (135, 175)).convert()
PlayerPhoto = pygame.transform.scale(pygame.image.load("Watcher.webp"), (215, 144))
for i in range(4):
    Hand.append(deck.pop(0))

pygame.mixer.init()
pygame.mixer.music.load("mind-bloom.mp3")
pygame.mixer.music.set_volume(.35)
pygame.mixer.music.play()


while True:
    #quitting
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit() 
    

    #controls
    key=pygame.key.get_pressed()
    if key[K_1] and len(Hand) > 0:
        if not IgnorePresses[0]:
            if(QueuedCard != 0):
                Hand.insert(0, QueuedCard)
                QueuedCard = Hand.pop(1)
            else:
                QueuedCard = Hand.pop(0)
            IgnorePresses[0] = 1
    elif IgnorePresses[0]:
        IgnorePresses[0] = 0
    if key[K_2] and len(Hand) > 1:
        if not IgnorePresses[1]:
            if(QueuedCard != 0):
                Hand.insert(1, QueuedCard)
                QueuedCard = Hand.pop(2)
            else:
                QueuedCard = Hand.pop(1)
            IgnorePresses[1] = 1
    elif IgnorePresses[1]:
        IgnorePresses[1] = 0
    if key[K_3] and len(Hand) > 2:
        if not IgnorePresses[2]:
            if(QueuedCard != 0):
                Hand.insert(2, QueuedCard)
                QueuedCard = Hand.pop(3)
            else:
                QueuedCard = Hand.pop(2)
            IgnorePresses[2] = 1
    elif IgnorePresses[2]:
        IgnorePresses[2] = 0
    if key[K_4] and len(Hand) > 3:
        if not IgnorePresses[3]:
            if(QueuedCard != 0):
                Hand.insert(3, QueuedCard)
                QueuedCard = Hand.pop(4)
            else:
                QueuedCard = Hand.pop(3)
            IgnorePresses[3] = 1
    elif IgnorePresses[3]:
        IgnorePresses[3] = 0
    if key[K_5] and len(Hand) > 4:
        if not IgnorePresses[4]:
            if(QueuedCard != 0):
                Hand.insert(4, QueuedCard)
                QueuedCard = Hand.pop(5)
            else:
                QueuedCard = Hand.pop(4)
            IgnorePresses[4] = 1
    elif IgnorePresses[4]:
        IgnorePresses[4] = 0
    if key[K_6] and len(Hand) > 5:
        if not IgnorePresses[5]:
            if(QueuedCard != 0):
                Hand.insert(5, QueuedCard)
                QueuedCard = Hand.pop(6)
            else:
                QueuedCard = Hand.pop(5)
            IgnorePresses[5] = 1
    elif IgnorePresses[5]:
        IgnorePresses[5] = 0
    if key[K_7] and len(Hand) > 6:
        if not IgnorePresses[6]:
            if(QueuedCard != 0):
                Hand.insert(6, QueuedCard)
                QueuedCard = Hand.pop(7)
            else:
                QueuedCard = Hand.pop(6)
            IgnorePresses[6] = 1
    elif IgnorePresses[6]:
        IgnorePresses[6] = 0
    if key[K_8] and len(Hand) > 7:
        if not IgnorePresses[7]:
            if(QueuedCard != 0):
                Hand.insert(7, QueuedCard)
                QueuedCard = Hand.pop(8)
            else:
                QueuedCard = Hand.pop(7)
            IgnorePresses[7] = 1
    elif IgnorePresses[7]:
        IgnorePresses[7] = 0
    if key[K_9] and len(Hand) > 8:
        if not IgnorePresses[8]:
            if(QueuedCard != 0):
                Hand.insert(8, QueuedCard)
                QueuedCard = Hand.pop(9)
            else:
                QueuedCard = Hand.pop(8)
            IgnorePresses[8] = 1
    elif IgnorePresses[8]:
        IgnorePresses[8] = 0
    if key[K_0] and len(Hand) > 9:
        if not IgnorePresses[9]:
            if(QueuedCard != 0):
                Hand.insert(9, QueuedCard)
                QueuedCard = Hand.pop(10)
            else:
                QueuedCard = Hand.pop(9)
            IgnorePresses[9] = 1
    elif IgnorePresses[9]:
        IgnorePresses[9] = 0
        
    #Song rendering and beat management
    screen.fill((0, 0, 0))
    TimeElapsed += clock.get_time()
    pygame.draw.line(screen, (110, 110, 110), (82, 740), (1200, 740), 3)
    pygame.draw.circle(screen, (110, 110, 110), (82, 740), 8)
    # pygame.draw.circle(screen, (110, 110, 110), (1118, 740), 8)
    for b in SongSyncing:
        if b[0] == 1:
            pygame.draw.circle(screen, (110, 110, 110), (82+b[1]-TimeElapsed/2, 740), 20)
            if b[1]-TimeElapsed/2 < 0:
                del SongSyncing[0]
                if Energy < MaxEnergy:
                    Energy += 1
        elif b[0] == 2:
            pygame.draw.polygon(screen, (110, 110, 110), ((82+b[1]-TimeElapsed/2, 720), (62+b[1]-TimeElapsed/2, 760), (102+b[1]-TimeElapsed/2, 760)))
            if b[1]-TimeElapsed/2 < 0:
                del SongSyncing[0]
                if len(Hand) < 10:
                    if len(deck) > 0:
                        Hand.append(deck.pop(0))
                    if len(deck) == 0 and len(Discard) != 0:
                        random.shuffle(Discard)
                        deck = Discard
        elif b[0] == 3:
            pygame.draw.rect(screen, (110, 110, 110), (62+b[1]-TimeElapsed/2, 720, 40, 40))
            if b[1]-TimeElapsed/2 < 0:
                del SongSyncing[0]
                if QueuedCard != 0:
                    FunctionNames[QueuedCard]()
        elif b[0] == 4:
            pygame.draw.line(screen, (255, 110, 110), (82+b[1]-TimeElapsed/2, 710), (82+b[1]-TimeElapsed/2, 770), 6)
            if b[1]-TimeElapsed/2 < 0:
                if YPosition == Targeted and EnemyHealth > 0:   
                    MyHealth -= 6
                    if MyHealth <= 0:
                        pygame.mixer.music.stop()
                Targeted = random.randint(0, 1)
                del SongSyncing[0]
    
    #Everything else rendering
    #Hand, library, energy
    if len(deck) > 0:
        screen.blit(FullLibrary[deck[0]], (15, 500))
    if QueuedCard != 0:
        screen.blit(FullLibrary[QueuedCard], (82, 300))
    for h in range(len(Hand)):
        screen.blit(FullLibrary[Hand[h]], ((h+1)*145+45, 500))
    for e in range(Energy):
        pygame.draw.circle(screen, (240, 155, 25), (40, 460-70*e), 25)
    #Health bars
    pygame.draw.line(screen, (0, 140, 0), (230, 35), (230+10*EnemyHealth, 35), 8)
    pygame.draw.line(screen, (0, 140, 0), (230, 465), (230+10*MyHealth, 465), 8)
    if EnemyHealth > 0:
        pygame.draw.rect(screen, (90, 0, 0), (450, 100+Targeted*150, 300, 150))
    pygame.draw.rect(screen, (255, 255, 255), (450, 100, 150, 150), 3)
    pygame.draw.rect(screen, (255, 255, 255), (600, 100, 150, 150), 3)
    pygame.draw.rect(screen, (255, 255, 255), (450, 250, 150, 150), 3)
    pygame.draw.rect(screen, (255, 255, 255), (600, 250, 150, 150), 3)
    screen.blit(PlayerPhoto, (450+150*XPosition, 100+150*YPosition))
    
        


            


    clock.tick(60)
    pygame.display.update()
