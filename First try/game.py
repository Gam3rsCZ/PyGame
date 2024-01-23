import pygame

class Game():
    
    def __init__(self):

        # pygame setup
        pygame.init()
        self.screenSize = {"WIDTH": pygame.display.Info().current_w, "HEIGHT": pygame.display.Info().current_h}
        self.screen = pygame.display.set_mode((800,600))#((self.screenSize["WIDTH"], self.screenSize["HEIGHT"]))
        #pygame.display.toggle_fullscreen()
        self.clock = pygame.time.Clock()
        self.running = True
        self.FPS_LIMIT = 60
        self.icon = pygame.image.load("woman.png").convert()
        pygame.display.set_caption("My first game")
        pygame.display.set_icon(self.icon)
    
        # declaring variables
        self.radius = 7.5
        self.speed = 7.5
        self.projectiles = []
        self.maxProjectiles = 5
        self.projectileSpeed = (self.speed/3)*2
        self.playerPosition = pygame.Vector2(self.screen.get_width()/2, self.screen.get_height()/2)
        self.border = {"LEFT": 0 + self.radius, "RIGHT": self.screen.get_width() - self.radius, "TOP": 0 + self.radius, "BOTTOM": self.screen.get_height() - self.radius}
        self.resizedIcon = pygame.transform.scale(self.icon, (self.screen.get_width(), self.screen.get_height()))
        
    def gameLoop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.blit(self.resizedIcon, (0,0),)

            for projectile in self.projectiles:
                if (projectile["X"] > self.screen.get_width()) or (projectile["Y"] > self.screen.get_height()) or (projectile["X"] < 0) or (projectile["Y"] < 0):
                    self.projectiles.remove({"X": projectile["X"],"Y": projectile["Y"]})
                else:
                    projectile["X"] += 5
                    pygame.draw.circle(surface=self.screen, color="red", center=(projectile["X"], projectile["Y"]), radius=self.radius/2)
                
            pygame.draw.circle(surface=self.screen, color="white", center=(self.playerPosition), radius=self.radius)
            
            self.controls()
            



            pygame.display.update()
            
            self.clock.tick(self.FPS_LIMIT)  # limits FPS
        pygame.quit()
        exit()
        
    def controls(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if self.playerPosition.y <= self.border["TOP"]:
                return
            self.playerPosition.y -= self.speed
        if keys[pygame.K_DOWN]:
            if self.playerPosition.y >= self.border["BOTTOM"]:
                return
            self.playerPosition.y += self.speed
        if keys[pygame.K_LEFT]:
            if self.playerPosition.x <= self.border["LEFT"]:
                return
            self.playerPosition.x -= self.speed
        if keys[pygame.K_RIGHT]:
            if self.playerPosition.x >= self.border["RIGHT"]:
                return
            self.playerPosition.x += self.speed
        if keys[pygame.K_ESCAPE]:
            self.running = False
        if keys[pygame.K_SPACE]:
            if {"X":self.playerPosition.x, "Y":self.playerPosition.y} in self.projectiles:
                return
            else:
                if len(self.projectiles) < self.maxProjectiles:
                    self.projectiles.append({"X":self.playerPosition.x, "Y":self.playerPosition.y})
                else:
                    return    
        if keys[pygame.K_s]:
            self.projectiles.clear()