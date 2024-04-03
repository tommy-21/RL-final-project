import GameEnv
import pygame
import numpy as np
from ddqn_keras import DDQNAgent
from collections import deque
import random, math
from pygame.locals import *
from ai import Dqn

TOTAL_GAMETIME = 1000 # Max game time for one episode
N_EPISODES = 100
REPLACE_TARGET = 50

interface = GameEnv.Interface()
game_choice = interface.run()

game = GameEnv.RacingEnv()
game.fps = 60

GameTime = 0 
GameHistory = []
renderFlag = False

dqn_agent = Dqn(input_size=19, nb_action=8, gamma=0.9)

# if you want to load the existing model uncomment this line.
# careful an existing model might be overwritten
#ddqn_agent.load_model()

dqn_scores = []
eps_history = []

def run():

    for e in range(N_EPISODES):
        
        game.reset()  # reset env

        done = False
        score = 0
        counter = 0
        
        observation_, reward, done = game.step(0, game_choice)  # Un mouvement de la voiture avec l'action 0
        observation = np.array(observation_)
        print(observation)

        gtime = 0  # set game time back to 0
        
        renderFlag = False  # if you want to render every episode set to true

        if e % 5 == 0 and e > 0:  # render every 5 episodes
            renderFlag = True
        
        while not done:
            # for event in pygame.event.get():
            #     if event.type == QUIT:
            #         return True
            #     elif event.type == KEYDOWN:
            #         if event.key == K_ESCAPE:
            #             return True
            
            action = dqn_agent.update(new_signal=observation, reward=reward)
            observation_, reward, done = game.step(action, game_choice)
            observation_ = np.array(observation_)

            # This is a countdown if no reward is collected the car will be done within 100 ticks
            if reward == 0:
                counter += 1
                if counter > 100:
                    done = True
            else:
                counter = 0

            score += reward

            # ddqn_agent.remember(observation, action, reward, observation_, int(done))
            # observation = observation_
            # ddqn_agent.learn()
            
            gtime += 1

            if gtime >= TOTAL_GAMETIME:
                done = True

            if renderFlag:
                game.render(action)

        # eps_history.append(ddqn_agent.epsilon)
        dqn_scores.append(score)
        avg_score = np.mean(dqn_scores[max(0, e-100):(e+1)])

        if e % REPLACE_TARGET == 0 and e > REPLACE_TARGET:
            dqn_agent.update_network_parameters()

        if e % 10 == 0 and e > 10:
            dqn_agent.save()
            print("save model")
            
        print('episode: ', e,'score: %.2f' % score,
              ' average score %.2f' % avg_score,)
            #   ' epsolon: ', ddqn_agent.epsilon,
            #   ' memory size', ddqn_agent.memory.mem_cntr % ddqn_agent.memory.mem_size)   

run()        
