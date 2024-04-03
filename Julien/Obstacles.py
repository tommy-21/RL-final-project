import pygame

class Obstacles:
    def __init__(self, x1, y1):
        self.x1 = x1
        self.y1 = y1

    def draw(self, win):
        pygame.draw.circle(win, (255, 255, 255), (self.x1, self.y1), 5)

def getObstacles():
    obstacles = []

    obstacle1 = Obstacles(382, 20)
    obstacle2 = Obstacles(549, 31)
    obstacle3 = Obstacles(192, 14)

    obstacles.append(obstacle1)
    obstacles.append(obstacle2)
    obstacles.append(obstacle3)

    return(obstacles)