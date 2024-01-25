import pygame
import ast
import json
from Network import Network

# Pygame variables
pygame.init()
screenSize = {"WIDTH": pygame.display.Info().current_w, "HEIGHT": pygame.display.Info().current_h}
screen = pygame.display.set_mode((1920,1080))#((screenSize["WIDTH"], screenSize["HEIGHT"]))
clock = pygame.time.Clock()
running = True
FPS_LIMIT = 60
icon = pygame.image.load("woman.png").convert()
pygame.display.set_caption("My first game")
pygame.display.set_icon(icon)
    
# Global variables
projectiles1 = []
projectiles2 = []
resizedIcon = pygame.transform.scale(icon, (screen.get_width(), screen.get_height()))
backgroundColor = "black"

# Networking
clientNumber = 0

class Player():
    def __init__(self, x, y, screen, rotation, color):
        self.x = x
        self.y = y
        self.playerSize = 64
        self.playerHeight = self.playerSize
        self.playerWidth = self.playerSize
        self.speed = 7.5
        self.playerImage = pygame.image.load("space-ship.png").convert()
        self.resizedPlayer = pygame.transform.scale(self.playerImage, (self.playerSize, self.playerSize)).convert()
        self.border = {"LEFT": 0 + self.playerSize, "RIGHT": screen.get_width() - self.playerSize*2, "TOP": 0 + self.playerSize, "BOTTOM": screen.get_height() - self.playerSize}
        self.playerHP = 1
        self.maxProjectiles = 1
        self.projectileRadius = self.playerSize/15
        self.projectileSpeed = self.speed * 6
        self.projectileColor = "blue"
        self.IsAlive = True
        self.projectiles = []
        self.rotation = rotation
        self.color = color
        
    def draw(self, screen):
        screen.blit(pygame.transform.rotate(self.resizedPlayer, self.rotation), (self.x - self.playerSize, self.y - self.playerSize/2))
        pygame.draw.circle(screen, self.color, (self.x - self.playerWidth/2, self.y), 5.0)
        
    def controls(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            
        if self.IsAlive:
            if keys[pygame.K_UP]:
                if self.y <= self.border["TOP"]:
                    return
                self.y -= self.speed
            if keys[pygame.K_DOWN]:
                if self.y >= self.border["BOTTOM"]:
                    return
                self.y += self.speed
            if keys[pygame.K_SPACE]:
                if {"X":int(self.x), "Y":int(self.y)} in self.projectiles:
                    return
                else:
                    if len(self.projectiles) < self.maxProjectiles:
                        self.projectiles.append({"X":int(self.x), "Y":int(self.y)})
                    else:
                        return    
                    
            self.update()
            
    def update(self):
        self.y = self.y
        self.x = self.x
        
def decodePosition(data:str) -> dict:#read
    result = ast.literal_eval(data)
    print(f"{result}\n{type(result)}")
    return result

def encodePosition(data:dict) -> str:#make
    return json.dumps(data)

def updateWindow(screen, player1, player2):
    screen.fill(backgroundColor)
    
    player1.draw(screen)
    player2.draw(screen)
    
    pygame.display.update()
    
def gameLoop(running):
    n = Network()
    startPosition = decodePosition(n.getPosition())
    player1 = Player(x=startPosition["X"], y=startPosition["Y"], screen=screen, rotation=-90, color="green")
    player2 = Player(x=startPosition["X"], y=startPosition["Y"], screen=screen, rotation=90, color="red")
    
    while running:
        clock.tick(FPS_LIMIT)
        
        player2Position = decodePosition(n.send(encodePosition({"X": player1.x, "Y": player1.y})))
        if player2Position is not None:
            player2.x = player2Position.get("X", player2.x)
            player2.y = player2Position.get("Y", player2.y)
            print(f"Received player2 position: {player2Position}")
        else:
            print("Received None for player2 position")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        
        player1.controls()
        updateWindow(screen, player1, player2)
        
gameLoop(running)