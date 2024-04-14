import pygame

class Obstacles:
    def __init__(self, x1, y1, width, height, type):
        self.x1 = x1
        self.y1 = y1
        self.width = width
        self.height = height
        self.type = type

    def draw(self, win):
        if self.type == 1:
            pygame.draw.rect(win, (96, 96, 96), (self.x1, self.y1, self.width, self.height))
            for i in range(8):
                if i%2 == 0:
                    pygame.draw.rect(win, (255, 255, 255), (self.x1, self.y1+i*10, self.width, 10))
        elif self.type == 2:
            pygame.draw.rect(win, (255, 255, 255), (self.x1, self.y1, self.width, self.height))
            for i in range(4):
                pygame.draw.line(win, (0, 0, 0), (self.x1, self.y1+i*self.height//3), (self.x1+self.width, self.y1+i*self.height//3))
            pygame.draw.circle(win, (204, 0, 0), (self.x1+self.width//2, self.y1+5), 4)
            pygame.draw.circle(win, (0, 0, 0), (self.x1+self.width//2, self.y1+15), 4)
            pygame.draw.circle(win, (0, 0, 0), (self.x1+self.width//2, self.y1+25), 4)
        
def getObstacles():
    obstacles = []

    obstacle1 = Obstacles(382, 495, 10, 30, 2)
    obstacle2 = Obstacles(540, 300, 10, 30, 2)
    obstacle3 = Obstacles(220, 14, 60, 75, 1)
    obstacle4 = Obstacles(250, 20, 20, 20, 3)

    obstacles.append(obstacle1)
    obstacles.append(obstacle2)
    obstacles.append(obstacle3)
    obstacles.append(obstacle4)

    return(obstacles)