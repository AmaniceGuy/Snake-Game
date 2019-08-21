import pygame
import random
pygame.init()

class Segment(pygame.sprite.Sprite):
    def __init__(self,x,y):
        self.image = pygame.Surface((20,20))
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def draw(self,surface):
        surface.blit(self.image,self.rect.topleft)

class Fruit(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.Surface((20,20))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.topleft = random.randrange(14,585,23),random.randrange(14,585,23)

    def move(self):
        self.rect.topleft = random.randrange(14,585,23),random.randrange(14,585,23)

    def draw(self,surface):
        surface.blit(self.image,self.rect.topleft)
        
class Edge(pygame.sprite.Sprite):
    def __init__(self,size,x,y):
        self.image = pygame.Surface(size)
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        
    def draw(self,surface):
        surface.blit(self.image,self.rect.topleft)

class ScoreKeeper(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.Surface((600,50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,600)
        self.score = 0
        self.font = pygame.font.Font("moonhouse.ttf",30)

    def playerScore(self):
        self.score += 1

    def draw(self,surface):
        self.message = self.font.render("SCORE: " + str(self.score),True,(0,0,0))
        self.image.fill((255,255,255))
        self.image.blit(self.message,(600 - self.message.get_width() - 10,10))
        surface.blit(self.image,self.rect.topleft)

screen = pygame.display.set_mode((600,650))
pygame.display.set_caption("Snake")

background = pygame.Surface(screen.get_size())
background.fill((0,0,0))

segments = [Segment(300,300)]
walls = [Edge((10,600),0,0),Edge((600,10),0,0),\
            Edge((10,600),590,0),Edge((600,10),0,590)]

fruit = Fruit()

scoreKeeper = ScoreKeeper()

direction = 2
gameTick = 0
clock = pygame.time.Clock()
run = True
fps = 10

while run:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 3:
                direction = 1
            elif event.key == pygame.K_DOWN and direction != 1:
                direction = 3
            elif event.key == pygame.K_LEFT and direction != 0:
                direction = 2
            elif event.key == pygame.K_RIGHT and direction != 2:
                direction = 0

    if pygame.sprite.spritecollide(segments[0],walls,False):
        run = False
    elif pygame.sprite.spritecollide(segments[0],segments[1:],False):
        run = False

    headx,heady = segments[0].rect.center
    if pygame.sprite.spritecollide(fruit,segments,False):
        fruit.move()
        scoreKeeper.playerScore()
        if scoreKeeper.score in [15,25,35]:
            fps += 1
    else:
        segments.pop()

    if direction == 0:
        newSegment = Segment(headx + 23 ,heady)
    elif direction == 1:
        newSegment = Segment(headx ,heady - 23)
    elif direction == 2:
        newSegment = Segment(headx - 23, heady)
    elif direction == 3:
        newSegment = Segment(headx, heady + 23)
    segments.insert(0,newSegment)
    
    background.fill((0,0,0))
    for wall in walls:
        wall.draw(background)
    fruit.draw(background)
    for section in segments:
        section.draw(background)
    scoreKeeper.draw(background)
        
    screen.blit(background,(0,0))
    pygame.display.flip()
    
pygame.quit()
