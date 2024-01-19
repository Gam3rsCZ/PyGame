import pygame

class Game():
    
    def __init__(self):

        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        self.clock = pygame.time.Clock()
        self.running = True
        self.FPS_LIMIT = 60
    
        # declaring variables
        self.radius = 7.5
        self.speed = 7.5
        self.dots = []
        self.oldest = 0
        self.maxDots = 5
        self.playerPosition = pygame.Vector2(self.screen.get_width()/2, self.screen.get_height()/2)
        self.border = {"LEFT": 0 + self.radius, "RIGHT": self.screen.get_width() - self.radius, "TOP": 0 + self.radius, "BOTTOM": self.screen.get_height() - self.radius}
        
    def gameLoop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill("black")

            for dot in self.dots:
                pygame.draw.circle(surface=self.screen, color="red", center=(dot["X"], dot["Y"]), radius=self.radius/2)
            
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
        if keys[pygame.K_w]:
            if {"X": self.playerPosition.x, "Y": self.playerPosition.y} in self.dots:
                return
            elif len(self.dots) < self.maxDots:
                self.dots.append({"X": self.playerPosition.x, "Y": self.playerPosition.y})
            else:
                if self.oldest < self.maxDots:
                    self.dots.pop(self.oldest)
                    self.dots.insert(self.oldest, {"X": self.playerPosition.x, "Y": self.playerPosition.y})
                    self.oldest +=1
                else:
                    self.oldest = 0
        if keys[pygame.K_s]:
            self.dots.clear()