import pygame, math
from Ray import Ray
from utils import *

GOALREWARD = 1

class Car:
    def __init__(self, x, y):
        self.pt = myPoint(x, y)
        self.x = x
        self.y = y
        self.width = 14
        self.height = 30

        self.points = 0

        self.original_image = pygame.image.load("car.png").convert()
        self.image = self.original_image  # This will reference the rotated image.
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect().move(self.x, self.y)

        self.angle = math.radians(180)
        self.soll_angle = self.angle

        self.dvel = 1  # Vitesse de la voiture
        self.vel = 0
        self.velX = 0
        self.velY = 0
        self.maxvel = 20 # Vitesse max

        self.angle = math.radians(180)
        self.soll_angle = self.angle

        # Coin supérieur gauche du rectangle
        self.pt1 = myPoint(self.pt.x - self.width / 2, self.pt.y - self.height / 2)
        # Coin supérieur droit du rectangle
        self.pt2 = myPoint(self.pt.x + self.width / 2, self.pt.y - self.height / 2)
        # Coin inférieur droit du rectangle
        self.pt3 = myPoint(self.pt.x + self.width / 2, self.pt.y + self.height / 2)
        # Coin inférieur gauche du rectangle
        self.pt4 = myPoint(self.pt.x - self.width / 2, self.pt.y + self.height / 2)

        self.p1 = self.pt1
        self.p2 = self.pt2
        self.p3 = self.pt3
        self.p4 = self.pt4

        self.distances = []
    

    def action(self, choice):
        if choice == 0:  # Ne rien faire
            pass
        elif choice == 1:  # Accélérer
            self.accelerate(self.dvel)
        elif choice == 8:  # Accélérer puis tourner à gauche
            self.accelerate(self.dvel)
            self.turn(1)
        elif choice == 7:  # Accélérer puis tourner à droite
            self.accelerate(self.dvel)
            self.turn(-1)
        elif choice == 4:  # Reculer
            self.accelerate(-self.dvel)
        elif choice == 5:  # Reculer puis tourner à gauche
            self.accelerate(-self.dvel)
            self.turn(1)
        elif choice == 6:  # Reculer puis tourner à droite
            self.accelerate(-self.dvel)
            self.turn(-1)
        elif choice == 3:  # Tourner à gauche
            self.turn(1)
        elif choice == 2:  # Tourner à droite
            self.turn(-1)
    
    def accelerate(self, dvel):
        dvel = dvel * 2

        self.vel = self.vel + dvel

        # On ne peut pas dépasser la vitesse maximale
        if self.vel > self.maxvel:
            self.vel = self.maxvel
        
        if self.vel < -self.maxvel:
            self.vel = -self.maxvel
        
        
    def turn(self, dir):
        self.soll_angle = self.soll_angle + dir * math.radians(15)
    
    # Mettre à jour la position de l'image de la voiture
    def update(self):

        #drifting code 

        # if(self.soll_angle > self.angle):
        #     if(self.soll_angle > self.angle + math.radians(10) * self.maxvel / ((self.velX**2 + self.velY**2)**0.5 + 1)):
        #         self.angle = self.angle + math.radians(10) * self.maxvel / ((self.velX**2 + self.velY**2)**0.5 + 1)
        #     else:
        #         self.angle = self.soll_angle
        
        # if(self.soll_angle < self.angle):
        #     if(self.soll_angle < self.angle - math.radians(10) * self.maxvel / ((self.velX**2 + self.velY**2)**0.5 + 1)):
        #         self.angle = self.angle - math.radians(10) * self.maxvel / ((self.velX**2 + self.velY**2)**0.5 + 1)
        #     else:
        #         self.angle = self.soll_angle
        
        self.angle = self.soll_angle

        vec_temp = rotate(myPoint(0,0), myPoint(0,self.vel), self.angle)
        self.velX, self.velY = vec_temp.x, vec_temp.y

        self.x = self.x + self.velX
        self.y = self.y + self.velY

        self.rect.center = self.x, self.y

        self.pt1 = myPoint(self.pt1.x + self.velX, self.pt1.y + self.velY)
        self.pt2 = myPoint(self.pt2.x + self.velX, self.pt2.y + self.velY)
        self.pt3 = myPoint(self.pt3.x + self.velX, self.pt3.y + self.velY)
        self.pt4 = myPoint(self.pt4.x + self.velX, self.pt4.y + self.velY)

        self.p1 ,self.p2 ,self.p3 ,self.p4  = rotateRect(self.pt1, self.pt2, self.pt3, self.pt4, self.soll_angle)

        self.image = pygame.transform.rotate(self.original_image, 90 - self.soll_angle * 180 / math.pi)
        x, y = self.rect.center  # Save its current center.
        self.rect = self.image.get_rect()  # Replace old rect with new rect.
        self.rect.center = (x, y)

    def cast(self, walls):

        """
            Fonction qui permet de lancer des rayons depuis la voiture dans différentes
            directions pour détecter les murs et collecter des informations sur l'environnement.
        """

        ray1 = Ray(self.x, self.y, self.soll_angle)
        ray2 = Ray(self.x, self.y, self.soll_angle - math.radians(30))
        ray3 = Ray(self.x, self.y, self.soll_angle + math.radians(30))
        ray4 = Ray(self.x, self.y, self.soll_angle + math.radians(45))
        ray5 = Ray(self.x, self.y, self.soll_angle - math.radians(45))
        ray6 = Ray(self.x, self.y, self.soll_angle + math.radians(90))
        ray7 = Ray(self.x, self.y, self.soll_angle - math.radians(90))
        ray8 = Ray(self.x, self.y, self.soll_angle + math.radians(180))

        ray9 = Ray(self.x, self.y, self.soll_angle + math.radians(10))
        ray10 = Ray(self.x, self.y, self.soll_angle - math.radians(10))
        ray11 = Ray(self.x, self.y, self.soll_angle + math.radians(135))
        ray12 = Ray(self.x, self.y, self.soll_angle - math.radians(135))
        ray13 = Ray(self.x, self.y, self.soll_angle + math.radians(20))
        ray14 = Ray(self.x, self.y, self.soll_angle - math.radians(20))

        ray15 = Ray(self.p1.x,self.p1.y, self.soll_angle + math.radians(90))
        ray16 = Ray(self.p2.x,self.p2.y, self.soll_angle - math.radians(90))

        ray17 = Ray(self.p1.x,self.p1.y, self.soll_angle + math.radians(0))
        ray18 = Ray(self.p2.x,self.p2.y, self.soll_angle - math.radians(0))

        self.rays = []
        self.rays.append(ray1)
        self.rays.append(ray2)
        self.rays.append(ray3)
        self.rays.append(ray4)
        self.rays.append(ray5)
        self.rays.append(ray6)
        self.rays.append(ray7)
        self.rays.append(ray8)

        self.rays.append(ray9)
        self.rays.append(ray10)
        self.rays.append(ray11)
        self.rays.append(ray12)
        self.rays.append(ray13)
        self.rays.append(ray14)

        self.rays.append(ray15)
        self.rays.append(ray16)

        self.rays.append(ray17)
        self.rays.append(ray18)


        observations = []
        self.closestRays = []

        # Calcul pour chaque rayon, le mur le plus proche et la distance correspondante
        for ray in self.rays:
            closest = None # myPoint(0,0)
            record = math.inf
            for wall in walls:
                pt = ray.cast(wall)
                if pt:
                    dist = distance(myPoint(self.x, self.y), pt)
                    if dist < record:
                        record = dist
                        closest = pt

            if closest: 
                #append distance for current ray 
                self.closestRays.append(closest)
                observations.append(record)
            else:
                observations.append(1000)

        for i in range(len(observations)):
            #invert observation values 0 is far away 1 is close
            observations[i] = ((1000 - observations[i]) / 1000)

        observations.append(self.vel / self.maxvel)
        return observations

    def collision(self, wall):

        line1 = myLine(self.p1, self.p2)
        line2 = myLine(self.p2, self.p3)
        line3 = myLine(self.p3, self.p4)
        line4 = myLine(self.p4, self.p1)

        x1 = wall.x1 
        y1 = wall.y1
        x2 = wall.x2
        y2 = wall.y2

        lines = []
        lines.append(line1)
        lines.append(line2)
        lines.append(line3)
        lines.append(line4)

        for li in lines:
            
            x3 = li.pt1.x
            y3 = li.pt1.y
            x4 = li.pt2.x
            y4 = li.pt2.y

            den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            
            if(den == 0):
                den = 0
            else:
                t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
                u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

                if t > 0 and t < 1 and u < 1 and u > 0:
                    return(True)
        
        return(False)
    
    def score(self, goal):
        
        line1 = myLine(self.p1, self.p3)

        # Le point (0, -50) a été pivoté de self.angle autour de (0, 0)
        vec = rotate(myPoint(0, 0), myPoint(0, -50), self.angle)
        # Droite reliant l'ancien centre de la voiture et le nouveau centre de la voiture
        line1 = myLine(myPoint(self.x, self.y), myPoint(self.x + vec.x, self.y + vec.y))

        # Coordonnées du goal
        x1 = goal.x1 
        y1 = goal.y1
        x2 = goal.x2
        y2 = goal.y2
        
        # Coordonnées 
        x3 = line1.pt1.x
        y3 = line1.pt1.y
        x4 = line1.pt2.x
        y4 = line1.pt2.y

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        
        if(den == 0):
            den = 0
        else:
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

            if t > 0 and t < 1 and u < 1 and u > 0:
                pt = math.floor(x1 + t * (x2 - x1)), math.floor(y1 + t * (y2 - y1))

                d = distance(myPoint(self.x, self.y), myPoint(pt[0], pt[1]))
                if d < 20:
                    #pygame.draw.circle(win, (0,255,0), pt, 5)
                    self.points += GOALREWARD
                    return(True)

        return(False)

    def reset(self):

        self.x = 50
        self.y = 300
        self.velX = 0
        self.velY = 0
        self.vel = 0
        self.angle = math.radians(180)
        self.soll_angle = self.angle
        self.points = 0

        self.pt1 = myPoint(self.pt.x - self.width / 2, self.pt.y - self.height / 2)
        self.pt2 = myPoint(self.pt.x + self.width / 2, self.pt.y - self.height / 2)
        self.pt3 = myPoint(self.pt.x + self.width / 2, self.pt.y + self.height / 2)
        self.pt4 = myPoint(self.pt.x - self.width / 2, self.pt.y + self.height / 2)

        self.p1 = self.pt1
        self.p2 = self.pt2
        self.p3 = self.pt3
        self.p4 = self.pt4

    def compute_distances(self, goal):
        if goal.isactiv:
            num = abs((goal.x2 - goal.x1)*(goal.y1-self.y)-(goal.x1-self.x)*(goal.y2-goal.y1))
            den = math.sqrt((goal.x2 - goal.x1)**2 + (goal.y2 - goal.y1)**2)
            self.distances.append(num/den)

    def draw(self, win):
        win.blit(self.image, self.rect)

    def outside(self, wall):

        line1 = myLine(self.p1, self.p2)
        line2 = myLine(self.p2, self.p3)
        line3 = myLine(self.p3, self.p4)
        line4 = myLine(self.p4, self.p1)

        x1 = wall.pt1.x
        y1 = wall.pt1.y
        x2 = wall.pt2.x
        y2 = wall.pt2.y

        lines = []
        lines.append(line1)
        lines.append(line2)
        lines.append(line3)
        lines.append(line4)

        for li in lines:
            
            x3 = li.pt1.x
            y3 = li.pt1.y
            x4 = li.pt2.x
            y4 = li.pt2.y

            den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            
            if(den == 0):
                den = 0
            else:
                t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
                u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

                if t > 0 and t < 1 and u < 1 and u > 0:
                    return True
        
        return False