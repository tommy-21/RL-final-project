import pygame
import math
from Walls import Wall
from Walls import getWalls
from Goals import Goal
from Goals import getGoals
from pygame.locals import *



GOALREWARD = 1
LIFE_REWARD = 0
PENALTY = -1


def distance(pt1, pt2):
    return(((pt1.x - pt2.x)**2 + (pt1.y - pt2.y)**2)**0.5)

def rotate(origin,point,angle):
    qx = origin.x + math.cos(angle) * (point.x - origin.x) - math.sin(angle) * (point.y - origin.y)
    qy = origin.y + math.sin(angle) * (point.x - origin.x) + math.cos(angle) * (point.y - origin.y)
    q = myPoint(qx, qy)
    return q

def rotateRect(pt1, pt2, pt3, pt4, angle):

    pt_center = myPoint((pt1.x + pt3.x)/2, (pt1.y + pt3.y)/2)

    pt1 = rotate(pt_center,pt1,angle)
    pt2 = rotate(pt_center,pt2,angle)
    pt3 = rotate(pt_center,pt3,angle)
    pt4 = rotate(pt_center,pt4,angle)

    return pt1, pt2, pt3, pt4

class myPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class myLine:
    def __init__(self, pt1, pt2):
        self.pt1 = myPoint(pt1.x, pt1.y)
        self.pt2 = myPoint(pt2.x, pt2.y)

class Ray:
    def __init__(self,x,y,angle):
        self.x = x
        self.y = y
        self.angle = angle

    def cast(self, wall):
        x1 = wall.x1 
        y1 = wall.y1
        x2 = wall.x2
        y2 = wall.y2

        vec = rotate(myPoint(0,0), myPoint(0,-1000), self.angle)
        
        x3 = self.x
        y3 = self.y
        x4 = self.x + vec.x
        y4 = self.y + vec.y

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            
        if(den == 0):
            den = 0
        else:
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

            if t > 0 and t < 1 and u < 1 and u > 0:
                pt = myPoint(math.floor(x1 + t * (x2 - x1)), math.floor(y1 + t * (y2 - y1)))
                return(pt)

 

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

        self.pt1 = myPoint(self.pt.x - self.width / 2, self.pt.y - self.height / 2)
        self.pt2 = myPoint(self.pt.x + self.width / 2, self.pt.y - self.height / 2)
        self.pt3 = myPoint(self.pt.x + self.width / 2, self.pt.y + self.height / 2)
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
        pass
    
    def accelerate(self, dvel):
        dvel = dvel * 2

        self.vel = self.vel + dvel

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

        for ray in self.rays:
            closest = None #myPoint(0,0)
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

        vec = rotate(myPoint(0,0), myPoint(0,-50), self.angle)
        line1 = myLine(myPoint(self.x,self.y),myPoint(self.x + vec.x, self.y + vec.y))

        x1 = goal.x1 
        y1 = goal.y1
        x2 = goal.x2
        y2 = goal.y2
            
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

    def draw(self, win):
        win.blit(self.image, self.rect)
  

class RacingEnv:

    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 36)

        self.fps = 60
        self.width = 1000
        self.height = 600
        self.history = []

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("RACING DQN")
        self.screen.fill((0,0,0))
        self.back_image = pygame.image.load("track.png").convert()
        self.back_rect = self.back_image.get_rect().move(0, 0)
        
        image = pygame.image.load("red.png").convert()
        self.red_lights = pygame.transform.scale(image, (image.get_width() * 0.02, image.get_height() * 0.02))
        self.red_lights_rect = self.red_lights.get_rect().move(382, 20)

        image = pygame.image.load("green.png").convert()
        self.green_lights = pygame.transform.scale(image, (image.get_width() * 0.1, image.get_height() * 0.1))
        self.green_lights_rect = self.green_lights.get_rect().move(549, 31)

        image = pygame.image.load("pieton.png").convert()
        self.pedestrian = pygame.transform.scale(image, (image.get_width() * 0.3, image.get_height() * 0.3))
        self.pedestrian_rect = self.pedestrian.get_rect().move(192, 14)
        
        image = pygame.image.load("goals.png").convert()
        self.goals_im = pygame.transform.scale(image, (image.get_width() * 0.05, image.get_height() * 0.05))
        self.goals_im_rect = self.goals_im.get_rect().move(600, 150)

        self.clock = pygame.time.Clock()
        self.action_space = None
        self.observation_space = None
        self.game_reward = 0
        self.score = 0

        # method call
        self.reset()


    def reset(self):
        self.screen.fill((0, 0, 0))

        self.car = Car(50, 300)
        self.walls = getWalls()
        self.goals = getGoals()
        self.game_reward = 0

    def step(self, action, mode):

        if mode == "manuel":
            done = self.handle_events(action)
        else:# mode == "automatique":
            done = False
            self.car.action(action)
            self.car.update()
        #self.car.action(action)
        # self.car.update()
        reward = LIFE_REWARD

        # Check if car passes Goal and scores
        index = 1
        for goal in self.goals:
            
            if index > len(self.goals):
                index = 1
            if goal.isactiv:
                if self.car.score(goal):
                    goal.isactiv = False
                    self.goals[index-2].isactiv = True
                    reward += GOALREWARD

            index = index + 1

        #check if car crashed in the wall
        for wall in self.walls:
            if self.car.collision(wall):
                reward += PENALTY
                if mode == "automatique":
                    done = True
                # done = True  # Fin du jeu lorsqu'on cogne le mur

        new_state = self.car.cast(self.walls)
        #normalize states
        if done:
            new_state = None

        return new_state, reward, done

    def render(self, action):

        DRAW_WALLS = False
        DRAW_GOALS = False
        DRAW_RAYS = False

        pygame.time.delay(10)

        self.clock = pygame.time.Clock()
        self.screen.fill((0, 0, 0))

        self.screen.blit(self.back_image, self.back_rect)
        self.screen.blit(self.red_lights, self.red_lights_rect)
        self.screen.blit(self.green_lights, self.green_lights_rect)
        self.screen.blit(self.pedestrian, self.pedestrian_rect)
        #self.screen.blit(self.goals_im, self.goals_im_rect)

        if DRAW_WALLS:
            for wall in self.walls:
                wall.draw(self.screen)
        
        if DRAW_GOALS:
            for goal in self.goals:
                goal.draw(self.screen)
                if goal.isactiv:
                    goal.draw(self.screen)
        
        self.car.draw(self.screen)

        if DRAW_RAYS:
            i = 0
            for pt in self.car.closestRays:
                pygame.draw.circle(self.screen, (0,0,255), (pt.x, pt.y), 5)
                i += 1
                if i < 15:
                    pygame.draw.line(self.screen, (255,255,255), (self.car.x, self.car.y), (pt.x, pt.y), 1)
                elif i >=15 and i < 17:
                    pygame.draw.line(self.screen, (255,255,255), ((self.car.p1.x + self.car.p2.x)/2, (self.car.p1.y + self.car.p2.y)/2), (pt.x, pt.y), 1)
                elif i == 17:
                    pygame.draw.line(self.screen, (255,255,255), (self.car.p1.x , self.car.p1.y ), (pt.x, pt.y), 1)
                else:
                    pygame.draw.line(self.screen, (255,255,255), (self.car.p2.x, self.car.p2.y), (pt.x, pt.y), 1)

        #render controll
        pygame.draw.rect(self.screen,(255,255,255),(800, 100, 40, 40),2)
        pygame.draw.rect(self.screen,(255,255,255),(850, 100, 40, 40),2)
        pygame.draw.rect(self.screen,(255,255,255),(900, 100, 40, 40),2)
        pygame.draw.rect(self.screen,(255,255,255),(850, 50, 40, 40),2)

        if action == 4:
            pygame.draw.rect(self.screen,(0,255,0),(850, 50, 40, 40)) 
        elif action == 6:
            pygame.draw.rect(self.screen,(0,255,0),(850, 50, 40, 40))
            pygame.draw.rect(self.screen,(0,255,0),(800, 100, 40, 40))
        elif action == 5:
            pygame.draw.rect(self.screen,(0,255,0),(850, 50, 40, 40))
            pygame.draw.rect(self.screen,(0,255,0),(900, 100, 40, 40))
        elif action == 1:
            pygame.draw.rect(self.screen,(255, 0, 0),(850, 100, 40, 40)) 
        elif action == 8:
            pygame.draw.rect(self.screen,(0,255,0),(850, 100, 40, 40))
            pygame.draw.rect(self.screen,(0,255,0),(800, 100, 40, 40))
        elif action == 7:
            pygame.draw.rect(self.screen,(0,255,0),(850, 100, 40, 40))
            pygame.draw.rect(self.screen,(0,255,0),(900, 100, 40, 40))
        elif action == 2:
            pygame.draw.rect(self.screen,(0,255,0),(800, 100, 40, 40))
        elif action == 3:
            pygame.draw.rect(self.screen,(0,255,0),(900, 100, 40, 40))

        # score
        text_surface = self.font.render(f'Points {self.car.points}', True, pygame.Color('green'))
        self.screen.blit(text_surface, dest=(0, 0))
        # speed
        text_surface = self.font.render(f'Speed {self.car.vel*-1}', True, pygame.Color('green'))
        self.screen.blit(text_surface, dest=(800, 0))

        self.clock.tick(self.fps)
        pygame.display.update()

    def close(self):
        pygame.quit()

    def handle_events(self, action):
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    self.car.action(4)
                    self.car.update()
                    self.render(action)
                elif event.key == K_DOWN:
                    self.car.action(1)
                    self.car.update()
                    self.render(action)
                elif event.key == K_LEFT:
                    self.car.action(2)
                    self.car.update()
                elif event.key == K_RIGHT:
                    self.car.action(3)
                    self.car.update()
                elif event.key == K_ESCAPE:
                    return True
                return False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            self.car.action(7)
            self.car.update()
            return False
        elif keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            self.car.action(8)
            self.car.update()
            return False
        elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            self.car.action(6)
            self.car.update()
            return False
        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            self.car.action(5)
            self.car.update()
            return False

        self.car.action(0)
        self.car.update()
        return False


class Interface:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("Choix du mode")

        self.font = pygame.font.Font(None, 24)
        self.selected_mode = None
        self.background_color = (200, 200, 200)
        self.text_color = (0, 0, 0)

        # Chargement du curseur fléché
        self.cursor_hand = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)

    def draw_interface(self):
        # Dessiner l'arrière-plan
        self.screen.fill(self.background_color)

        # Dessiner les options de mode avec des bordures
        pygame.draw.rect(self.screen, self.text_color, (50, 50, 300, 30), 2)
        pygame.draw.rect(self.screen, self.text_color, (50, 100, 300, 30), 2)
        pygame.draw.rect(self.screen, self.text_color, (50, 150, 300, 30), 2)

        # Dessiner les options de mode centrées
        text_auto = self.font.render("Mode Automatique", True, self.text_color)
        text_semi_auto = self.font.render("Mode Semi-Automatique", True, self.text_color)
        text_manual = self.font.render("Mode Manuel", True, self.text_color)

        text_rect_auto = text_auto.get_rect(center=(self.screen.get_width() // 2, 65))
        text_rect_semi_auto = text_semi_auto.get_rect(center=(self.screen.get_width() // 2, 115))
        text_rect_manual = text_manual.get_rect(center=(self.screen.get_width() // 2, 165))

        self.screen.blit(text_auto, text_rect_auto)
        self.screen.blit(text_semi_auto, text_rect_semi_auto)
        self.screen.blit(text_manual, text_rect_manual)

        pygame.display.flip()

    def get_user_choice(self):
        while self.selected_mode is None:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # Enregistrer le mode sélectionné
                    if 50 <= mouse_pos[0] <= 350:
                        if 35 <= mouse_pos[1] <= 85:
                            self.selected_mode = "automatique"
                        elif 85 <= mouse_pos[1] <= 135:
                            self.selected_mode = "semi-automatique"
                        elif 135 <= mouse_pos[1] <= 185:
                            self.selected_mode = "manuel"
                elif event.type == MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    # Changer le curseur en flèche lorsqu'il survole une option
                    if 50 <= mouse_pos[0] <= 350:
                        if 35 <= mouse_pos[1] <= 85 or 85 <= mouse_pos[1] <= 135 or 135 <= mouse_pos[1] <= 185:
                            pygame.mouse.set_cursor(*self.cursor_hand)

    def run(self):
        self.draw_interface()
        self.get_user_choice()
        pygame.quit()
        return self.selected_mode


