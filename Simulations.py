from fonction_g_discrete import fonction_g_discrete
import random
import numpy as np
import pandas as pd

def overall():
    xcible=5
    ycible=5
    lim_x=[0,20]
    lim_y=[0,20]
    destination=[xcible,ycible]
    Liste_realisations=[]
    table_cout=np.random.multivariate_normal(size=20,mean=[-5]*20,cov=np.eye(20))
    goal_x=5
    goal_y=5
    for J in range(30):
        T=np.random.choice([20,50,100])
        Table_nom=[J]*T
        Recompenses=[]
        Actions=[]
        Nouvel_etat=[]
        Positions_t=[]
        x_si=np.random.choice(range(20))
        y_si=np.random.choice(range(20))
        situation_initiale=np.array([x_si,y_si])
        for j in range(T):
            vitesse=np.random.choice([0,1,2,3])
            if situation_initiale[0]==goal_x and situation_initiale[1]==goal_y:
                recompense=1
            else:
                recompense=-1
            if vitesse!=0:

                choix_angle=random.choice([1,2,3,4])
                changement_pos=fonction_g_discrete(choix_angle=choix_angle,v=vitesse)
                situation_nouvelle=np.add(changement_pos,situation_initiale)
                if situation_nouvelle[0]>lim_x[0] or situation_nouvelle[0]>lim_x[1]:
                    recompense=+-20*vitesse
                    situation_nouvelle=situation_initiale
                elif situation_nouvelle[1]>lim_y[0] or situation_nouvelle[1]>lim_y[1]:
                    recompense=+-20*vitesse
                    situation_nouvelle=situation_initiale
                elif situation_nouvelle[0]==goal_x and situation_nouvelle[1]==goal_y:
                    recompense=1
                else:
                    recompense=+table_cout[situation_nouvelle[0],situation_nouvelle[1]]/vitesse
            else:
                situation_nouvelle=situation_initiale
                choix_angle=random.choice([0,1,2,3,4])
            Recompenses.append(recompense)
            Actions.append((vitesse,choix_angle))
            Positions_t.append(situation_initiale)
            Nouvel_etat.append(situation_nouvelle)
            situation_initiale=situation_nouvelle
        dico=pd.DataFrame({"recompense":Recompenses,"actions":Actions,"etat_t":Positions_t,"etat_suivant":Nouvel_etat,"Indice_simul":Table_nom})
        Liste_realisations.append(dico)
    return(Liste_realisations)