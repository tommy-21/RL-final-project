import pygame
import math
from Walls import Wall
from Walls import getWalls
from Goals import Goal
from Goals import getGoals
from pygame.locals import *
from Car import *
from utils import *




GOALREWARD = 1
LIFE_REWARD = 0
PENALTY = -1
  

class RacingEnv:

    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 36)

        self.fps = 60
        self.width = 1000
        self.height = 600
        self.history = []

        # All the screen
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
                    done = True  # Fin du jeu lorsqu'on cogne le mur

        new_state = self.car.cast(self.walls)
        #normalize states
        if done:
            new_state = None

        return new_state, reward, done

    def render(self, action):

        DRAW_WALLS = False
        DRAW_GOALS = False
        DRAW_RAYS = True

        pygame.time.delay(60)

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
        pygame.draw.rect(self.screen,(255,255,255),(800, 75, 40, 40),2)
        pygame.draw.rect(self.screen,(255,255,255),(850, 100, 40, 40),2)
        pygame.draw.rect(self.screen,(255,255,255),(900, 75, 40, 40),2)
        pygame.draw.rect(self.screen,(255,255,255),(850, 50, 40, 40),2)

        if action == 4:
            pygame.draw.rect(self.screen,(0,255,0),(850, 50, 40, 40)) 
        elif action == 6:
            pygame.draw.rect(self.screen,(0,255,0),(850, 50, 40, 40))
            pygame.draw.rect(self.screen,(0,255,0),(800, 75, 40, 40))
        elif action == 5:
            pygame.draw.rect(self.screen,(0,255,0),(850, 50, 40, 40))
            pygame.draw.rect(self.screen,(0,255,0),(900, 75, 40, 40))
        elif action == 1:
            pygame.draw.rect(self.screen,(255, 0, 0),(850, 100, 40, 40)) 
        elif action == 8:
            pygame.draw.rect(self.screen,(0,255,0),(850, 100, 40, 40))
            pygame.draw.rect(self.screen,(0,255,0),(800, 75, 40, 40))
        elif action == 7:
            pygame.draw.rect(self.screen,(0,255,0),(850, 100, 40, 40))
            pygame.draw.rect(self.screen,(0,255,0),(900, 75, 40, 40))
        elif action == 2:
            pygame.draw.rect(self.screen,(0,255,0),(800, 75, 40, 40))
        elif action == 3:
            pygame.draw.rect(self.screen,(0,255,0),(900, 75, 40, 40))

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


