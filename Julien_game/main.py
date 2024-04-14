import GameEnv
import pygame
import os
import sys
import time
import numpy as np
from ddqn_keras import DDQNAgent
from DDQN_v2 import DDQNAgent_V2
from collections import deque
import random, math
from pygame.locals import *

TOTAL_GAMETIME = 1000 # Max game time for one episode
N_EPISODES = 20
REPLACE_TARGET = 5

interface = GameEnv.Interface()
game_choice = interface.run()

game = GameEnv.RacingEnv()
game.fps = 60

GameTime = 0 
GameHistory = []
renderFlag = False

#ddqn_agent = DDQNAgent(alpha=0.0005, gamma=0.99, n_actions=5, epsilon=0.5, epsilon_end=0.02, epsilon_dec=0.95, replace_target= REPLACE_TARGET, batch_size=256, input_dims=24)
ddqn_agent = DDQNAgent_V2(alpha=0.0005, gamma=0.99, n_actions=5, epsilon=0.5, epsilon_end=0.02, epsilon_dec=0.95, replace_target= REPLACE_TARGET, batch_size=256, input_dims=24)

# if you want to load the existing model uncomment this line.
# careful an existing model might be overwritten
#ddqn_agent.load_model()

ddqn_scores = []
eps_history = []

def run():

    for e in range(N_EPISODES):
        
        game.reset()  # reset env

        i = 0
        j = 0
        temps_init = time.time()
        temps_init_2 = time.time()

        done = False
        score = 0
        counter = 0
        
        states_, reward, done, _ = game.step(0, game_choice)  # Un mouvement de la voiture avec l'action 0
        states = np.array(states_)

        gtime = 0  # set game time back to 0
        
        renderFlag = True  # if you want to render every episode set to true

        # if e % 2 == 0 and e > 0:  # render every 5 episodes
        #     renderFlag = True
        
        while not done:
            sys.stdout = open(os.devnull, 'w')
            action = ddqn_agent.choose_action(states)
            sys.stdout = sys.__stdout__
            states_, reward, done, action = game.step(action, game_choice)
            states_ = np.array(states_)

            # This is a countdown if no reward is collected the car will be done within 100 ticks
            if reward == 0:
                counter += 1
                if counter > 100:
                    done = True
                    game.reset()
            else:
                counter = 0

            score += reward

            ddqn_agent.remember(states, action, reward, states_, int(done))
            states = states_
            sys.stdout = open(os.devnull, 'w')
            ddqn_agent.learn()
            sys.stdout = sys.__stdout__
            # print(ddqn_agent.epsilon)
            
            gtime += 1

            if gtime >= TOTAL_GAMETIME:
                done = True
                game.reset()

            if renderFlag:
                temps_fin = time.time()
                if (i == 2) & ((temps_fin-temps_init) > 1):
                    i = 0
                    temps_init = temps_fin
                else:
                    if (temps_fin - temps_init) > 5:
                        temps_init = temps_fin
                        i += 1
                temps_fin_2 = time.time()
                if (temps_fin_2 - temps_init_2) > 2:
                    temps_init_2 = temps_fin_2
                    j += 1
                    if j == 6:
                        j = 0
                game.render(action, i, j)

        eps_history.append(ddqn_agent.epsilon)
        ddqn_scores.append(score)
        avg_score = np.mean(ddqn_scores[max(0, e-100):(e+1)])

        if e % REPLACE_TARGET == 0 and e > REPLACE_TARGET:
            ddqn_agent.update_network_parameters()

        if e % 10 == 0 and e >= 10:
            ddqn_agent.save_model()
            print("save model")
            
        print('episode: ', e+1,'score: %.2f' % score,
              ' average score %.2f' % avg_score,
              ' epsilon: ', ddqn_agent.epsilon,
              ' memory size', ddqn_agent.memory.mem_cntr % ddqn_agent.memory.mem_size)   

run()        
