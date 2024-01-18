import pygame

class Game():
    
    def __init__(self):

        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        self.clock = pygame.time.Clock()
        self.running = True
        self.FPS_LIMIT = 60
    

        self.speed = 5
        self.playerPosition = pygame.Vector2(self.screen.get_width()/2, self.screen.get_height()/2)
        self.border = {"LEFT": 0, "RIGHT": self.screen.get_width(), "TOP": 0, "BOTTOM": self.screen.get_height()}
        
    def gameLoop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill("black")

            pygame.draw.circle(surface=self.screen, color="white", center=(self.playerPosition), radius=1.0)
            
                
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                if self.playerPosition.y == self.border["TOP"]:
                    continue
                self.playerPosition.y -= self.speed
            if keys[pygame.K_DOWN]:
                if self.playerPosition.y == self.border["BOTTOM"]:
                    continue
                self.playerPosition.y += self.speed
            if keys[pygame.K_LEFT]:
                if self.playerPosition.x == self.border["LEFT"]:
                    continue
                self.playerPosition.x -= self.speed
            if keys[pygame.K_RIGHT]:
                if self.playerPosition.x == self.border["RIGHT"]:
                    continue
                self.playerPosition.x += self.speed




            pygame.display.update()
            
            self.clock.tick(self.FPS_LIMIT)  # limits FPS
        pygame.quit()
        exit()