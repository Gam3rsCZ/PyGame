import pygame

class Game():
    
    def __init__(self):

        # pygame setup
        pygame.init()
        self.screenSize = {"WIDTH": pygame.display.Info().current_w, "HEIGHT": pygame.display.Info().current_h}
        self.screen = pygame.display.set_mode((1920,1080))#((self.screenSize["WIDTH"], self.screenSize["HEIGHT"]))
        pygame.display.toggle_fullscreen()
        self.clock = pygame.time.Clock()
        self.running = True
        self.FPS_LIMIT = 60
        self.icon = pygame.image.load("woman.png").convert()
        pygame.display.set_caption("My first game")
        pygame.display.set_icon(self.icon)
    
        # declaring variables
        self.radius = 7.5
        self.speed = 7.5
        self.projectiles1 = []
        self.projectiles2 = []
        self.maxProjectiles = 1
        self.projectileSpeed = self.speed * 3
        self.player1Position = pygame.Vector2(self.screen.get_width()/20, self.screen.get_height()/2)
        self.player1HP = 1
        self.player2Position = pygame.Vector2((self.screen.get_width()/20)*19, self.screen.get_height()/2)
        self.player2HP = 1
        self.border = {"LEFT": 0 + self.radius, "RIGHT": self.screen.get_width() - self.radius, "TOP": 0 + self.radius, "BOTTOM": self.screen.get_height() - self.radius}
        self.resizedIcon = pygame.transform.scale(self.icon, (self.screen.get_width(), self.screen.get_height()))
        
    def gameLoop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            #self.screen.blit(self.resizedIcon, (0,0),)
            self.screen.fill("black")

            for projectile in self.projectiles1:
                if (projectile["X"] == int(self.player2Position.x)) and (projectile["Y"] == int(self.player2Position.y)):
                    self.player2HP -= 1
                elif (projectile["X"] > self.screen.get_width()) or (projectile["Y"] > self.screen.get_height()) or (projectile["X"] < 0) or (projectile["Y"] < 0):
                    self.projectiles1.remove({"X": projectile["X"],"Y": projectile["Y"]})
                else:
                    projectile["X"] += self.projectileSpeed
                    pygame.draw.circle(surface=self.screen, color="red", center=(projectile["X"], projectile["Y"]), radius=self.radius/2)
                    
            for projectile in self.projectiles2:
                if (projectile["X"] == int(self.player1Position.x)) and (projectile["Y"] == int(self.player1Position.y)):
                    self.player1HP -= 1
                elif (projectile["X"] > self.screen.get_width()) or (projectile["Y"] > self.screen.get_height()) or (projectile["X"] < (self.radius + self.projectileSpeed)) or (projectile["Y"] < 0):
                    self.projectiles2.remove({"X": projectile["X"],"Y": projectile["Y"]})
                else:
                    projectile["X"] -= self.projectileSpeed
                    pygame.draw.circle(surface=self.screen, color="red", center=(projectile["X"], projectile["Y"]), radius=self.radius/2)
                
            #player1
            if self.player1HP == 0:
                pass
            else:
                pygame.draw.circle(surface=self.screen, color="white", center=(self.player1Position), radius=self.radius)
                
            
            #player2
            if self.player2HP == 0:
                pass
            else:
                pygame.draw.circle(surface=self.screen, color="yellow", center=(self.player2Position), radius=self.radius)
                
            
            self.controls()
            



            pygame.display.update()
            
            self.clock.tick(self.FPS_LIMIT)  # limits FPS
        pygame.quit()
        exit()
        
    def controls(self):
        keys = pygame.key.get_pressed()
        #player 1 movement
        if keys[pygame.K_w]:
            if self.player1Position.y <= self.border["TOP"]:
                return
            self.player1Position.y -= self.speed
        if keys[pygame.K_s]:
            if self.player1Position.y >= self.border["BOTTOM"]:
                return
            self.player1Position.y += self.speed
        """
        if keys[pygame.K_a]:
            if self.player1Position.x <= self.border["LEFT"]:
                return
            self.player1Position.x -= self.speed
        if keys[pygame.K_d]:
            if self.player1Position.x >= self.border["RIGHT"]:
                return
            elif self.player1Position.x >= self.screen.get_width()/4:
                return
            self.player1Position.x += self.speed
        """
        if keys[pygame.K_SPACE]:
            if {"X":int(self.player1Position.x), "Y":int(self.player1Position.y)} in self.projectiles1:
                return
            else:
                if len(self.projectiles1) < self.maxProjectiles:
                    self.projectiles1.append({"X":int(self.player1Position.x), "Y":int(self.player1Position.y)})
                else:
                    return   
        #player 2 movement 
        if keys[pygame.K_UP]:
            if self.player2Position.y <= self.border["TOP"]:
                return
            self.player2Position.y -= self.speed
        if keys[pygame.K_DOWN]:
            if self.player2Position.y >= self.border["BOTTOM"]:
                return
            self.player2Position.y += self.speed
        """
        if keys[pygame.K_LEFT]:
            if self.player2Position.x <= self.border["LEFT"]:
                return
            elif self.player2Position.x <= (self.screen.get_width()/4 * 3):
                return
            self.player2Position.x -= self.speed
        if keys[pygame.K_RIGHT]:
            if self.player2Position.x >= self.border["RIGHT"]:
                return
            self.player2Position.x += self.speed
        """
        if keys[pygame.K_RSHIFT]:
            if {"X":int(self.player2Position.x), "Y":int(self.player2Position.y)} in self.projectiles2:
                return
            else:
                if len(self.projectiles2) < self.maxProjectiles:
                    self.projectiles2.append({"X":int(self.player2Position.x), "Y":int(self.player2Position.y)})
                else:
                    return    

        #Close game
        if keys[pygame.K_ESCAPE]:
            self.running = False