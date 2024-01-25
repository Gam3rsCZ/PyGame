import pygame
import threading

class Game():
    
    def __init__(self):

        #Pygame variables
        pygame.init()
        self.screenSize = {"WIDTH": pygame.display.Info().current_w, "HEIGHT": pygame.display.Info().current_h}
        self.screen = pygame.display.set_mode((1920,1080))#((self.screenSize["WIDTH"], self.screenSize["HEIGHT"]))
        self.clock = pygame.time.Clock()
        self.running = True
        self.FPS_LIMIT = 60
        self.icon = pygame.image.load("woman.png").convert()
        self.playerImage = pygame.image.load("space-ship.png").convert()
        pygame.display.set_caption("My first game")
        pygame.display.set_icon(self.icon)
    
        #Global variables
        self.playerSize = 64
        self.playerHeight = self.playerSize
        self.playerWidth = self.playerSize
        self.speed = 7.5
        self.projectiles1 = []
        self.projectiles2 = []
        self.maxProjectiles = 1
        self.projectileRadius = self.playerSize/15
        self.projectileSpeed = self.speed * 6
        self.playerHP = 1
        self.border = {"LEFT": 0 + self.playerSize, "RIGHT": self.screen.get_width() - self.playerSize*2, "TOP": 0 + self.playerSize, "BOTTOM": self.screen.get_height() - self.playerSize}
        self.resizedIcon = pygame.transform.scale(self.icon, (self.screen.get_width(), self.screen.get_height()))
        self.resizedPlayer = pygame.transform.scale(self.playerImage, (self.playerSize, self.playerSize)).convert()
        self.projectileColor = "blue"
        self.backgroundColor = "black"
        
        #Player 1
        self.player1Position = pygame.Vector2(self.playerSize, self.screen.get_height()/2)
        self.player1HP = self.playerHP
        self.player1IsAlive = True
        self.player1_keys = set()
        
        #Player 2
        self.player2Position = pygame.Vector2((self.screen.get_width() - self.playerSize*2), self.screen.get_height()/2)
        self.player2HP = self.playerHP
        self.player2IsAlive = True
        self.player2_keys = set()
        
        
    def gameLoop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                

            #self.screen.blit(self.resizedIcon, (0,0),)
            self.screen.fill(self.backgroundColor)

            #Player 1 projectiles
            for projectile in self.projectiles1:
                #playerHitbox = pygame.Rect(self.player2Position.x, self.player2Position.y, self.playerWidth, self.playerHeight)
                playerHitbox = pygame.Rect(self.player2Position.x - self.playerWidth / 2, self.player2Position.y - self.playerHeight / 2, self.playerWidth, self.playerHeight)
                projectileHitbox = pygame.Rect(projectile["X"], projectile["Y"], self.projectileRadius, self.projectileRadius)

                #Collision with player
                if self.player2IsAlive:
                    if projectileHitbox.colliderect(playerHitbox):
                        if (self.player2HP - 1) == 0:
                            self.player2IsAlive = False
                        else:
                            self.player2HP -= 1
                        self.projectiles1.remove({"X": projectile["X"],"Y": projectile["Y"]})
                    
                #Collision with screen border
                if (projectile["X"] > self.screen.get_width()) or (projectile["Y"] > self.screen.get_height()) or (projectile["X"] < 0) or (projectile["Y"] < 0):
                    self.projectiles1.remove({"X": projectile["X"],"Y": projectile["Y"]})
                    
                #Projectile movement
                else:
                    projectile["X"] += self.projectileSpeed
                    pygame.draw.circle(surface=self.screen, color=self.projectileColor, center=(projectile["X"], projectile["Y"]), radius=self.projectileRadius)
                    
            #Player 2 projectiles
            for projectile in self.projectiles2:
                #playerHitbox = pygame.Rect(self.player1Position.x, self.player1Position.y, self.playerWidth, self.playerHeight)
                playerHitbox = pygame.Rect(self.player1Position.x - self.playerWidth / 2, self.player1Position.y - self.playerHeight / 2, self.playerWidth, self.playerHeight)
                projectileHitbox = pygame.Rect(projectile["X"], projectile["Y"], self.projectileRadius, self.projectileRadius)
                
                #Collision with player
                if self.player1IsAlive:
                    if projectileHitbox.colliderect(playerHitbox):
                        if (self.player1HP - 1) == 0:
                            self.player1IsAlive = False
                        else:
                            self.player1HP -= 1
                        self.projectiles2.remove({"X": projectile["X"],"Y": projectile["Y"]})
                    
                #Collision with screen border
                if (projectile["X"] > self.screen.get_width()) or (projectile["Y"] > self.screen.get_height()) or (projectile["X"] < (self.projectileRadius + self.projectileSpeed)) or (projectile["Y"] < 0):
                    self.projectiles2.remove({"X": projectile["X"],"Y": projectile["Y"]})
                    
                #Projectile movement
                else:
                    projectile["X"] -= self.projectileSpeed
                    pygame.draw.circle(surface=self.screen, color=self.projectileColor, center=(projectile["X"], projectile["Y"]), radius=self.projectileRadius)
                
            #player1
            if self.player1IsAlive:
                self.screen.blit(pygame.transform.rotate(self.resizedPlayer, -90.0), (self.player1Position.x - self.playerSize, self.player1Position.y - self.playerSize/2))
            else:
                pass
                
            
            #player2
            if self.player2IsAlive:
                self.screen.blit(pygame.transform.rotate(self.resizedPlayer, 90.0), (self.player2Position.x + self.playerSize, self.player2Position.y - self.playerSize/2))
            else:
                pass
                

            #Controls
            self.controls_Y()


            pygame.display.update()
            
            self.clock.tick(self.FPS_LIMIT)  # limits FPS
        pygame.quit()
        exit()

    def controls_FULL(self):
        keys = pygame.key.get_pressed()
        
        #game
        if keys[pygame.K_ESCAPE]:
            self.running = False
            
            
        #player 1 movement
        if self.player1IsAlive:
            if keys[pygame.K_w]:
                if self.player1Position.y <= self.border["TOP"]:
                    return
                self.player1Position.y -= self.speed
            if keys[pygame.K_s]:
                if self.player1Position.y >= self.border["BOTTOM"]:
                    return
                self.player1Position.y += self.speed
            if keys[pygame.K_SPACE]:
                if {"X":int(self.player1Position.x), "Y":int(self.player1Position.y)} in self.projectiles1:
                    return
                else:
                    if len(self.projectiles1) < self.maxProjectiles:
                        self.projectiles1.append({"X":int(self.player1Position.x), "Y":int(self.player1Position.y)})
                    else:
                        return
            if keys[pygame.K_a]:
                if self.player1Position.x <= self.border["LEFT"]:
                    return
                self.player1Position.x -= self.speed
            if keys[pygame.K_d]:
                if self.player1Position.x >= self.border["RIGHT"]:
                    return
                elif self.player1Position.x >= ((self.screen.get_width()/4) - self.playerSize/2):
                    return
                self.player1Position.x += self.speed

        #player 2 movement 
        if self.player2IsAlive:
            if keys[pygame.K_UP]:
                if self.player2Position.y <= self.border["TOP"]:
                    return
                self.player2Position.y -= self.speed
            if keys[pygame.K_DOWN]:
                if self.player2Position.y >= self.border["BOTTOM"]:
                    return
                self.player2Position.y += self.speed
            if keys[pygame.K_LEFT]:
                if self.player2Position.x <= self.border["LEFT"]:
                    return
                elif self.player2Position.x <= ((self.screen.get_width()/4 * 3) - self.playerSize/2):
                    return
                self.player2Position.x -= self.speed
            if keys[pygame.K_RIGHT]:
                if self.player2Position.x >= self.border["RIGHT"]:
                    return
                self.player2Position.x += self.speed
            if keys[pygame.K_RSHIFT]:
                if {"X":int(self.player2Position.x), "Y":int(self.player2Position.y)} in self.projectiles2:
                    return
                else:
                    if len(self.projectiles2) < self.maxProjectiles:
                        self.projectiles2.append({"X":int(self.player2Position.x), "Y":int(self.player2Position.y)})
                    else:
                        return    
                    
    def controls_Y(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.running = False
            
        #player 1 movement
        if self.player1IsAlive:
            if keys[pygame.K_w]:
                if self.player1Position.y <= self.border["TOP"]:
                    return
                self.player1Position.y -= self.speed
            if keys[pygame.K_s]:
                if self.player1Position.y >= self.border["BOTTOM"]:
                    return
                self.player1Position.y += self.speed
            if keys[pygame.K_SPACE]:
                if {"X":int(self.player1Position.x), "Y":int(self.player1Position.y)} in self.projectiles1:
                    return
                else:
                    if len(self.projectiles1) < self.maxProjectiles:
                        self.projectiles1.append({"X":int(self.player1Position.x), "Y":int(self.player1Position.y)})
                    else:
                        return

        #player 2 movement 
        if self.player2IsAlive:
            if keys[pygame.K_UP]:
                if self.player2Position.y <= self.border["TOP"]:
                    return
                self.player2Position.y -= self.speed
            if keys[pygame.K_DOWN]:
                if self.player2Position.y >= self.border["BOTTOM"]:
                    return
                self.player2Position.y += self.speed
            if keys[pygame.K_RSHIFT]:
                if {"X":int(self.player2Position.x), "Y":int(self.player2Position.y)} in self.projectiles2:
                    return
                else:
                    if len(self.projectiles2) < self.maxProjectiles:
                        self.projectiles2.append({"X":int(self.player2Position.x), "Y":int(self.player2Position.y)})
                    else:
                        return    