
import numpy as np
import matplotlib.pyplot as plt
def fonction_g(choix_angle,v):
    if v==0:
        print("ici")
        x=0
        y=0
    else: 
        if choix_angle==1:
            x=1
            y=0
        if choix_angle==2:
            x=-1
            y=0
        if choix_angle==3:
            x=0
            y=1
        if choix_angle==4:
            x=0
            y=-1
    return([x,y])

