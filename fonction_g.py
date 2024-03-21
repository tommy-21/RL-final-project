
import numpy as np
import matplotlib.pyplot as plt
def fonction_g(t,prop,v,avance):
    if avance==1:
        angle=np.pi * prop
        x=v*t*np.cos((np.pi/2)-angle*t)
        y=v*t*np.sin((np.pi/2)-angle*t)
    else:
        angle=np.pi*prop
        x=v*t*np.cos((-np.pi/2)-angle*t)
        y=v*t*np.sin((-np.pi/2)-angle*t)
    return([x,y])

vecteur_temps=np.linspace(0,10,100)
resultat=np.array([fonction_g(elt,prop=1/2,v=1,avance=1) for elt in vecteur_temps])
M=resultat.shape[0]
resultat=resultat.reshape((int(M),2))
plt.plot(resultat[:,0],resultat[:,1])
# 
resultat2=np.array([fonction_g(elt,prop=-1/2,v=1,avance=1) for elt in vecteur_temps])
M=resultat.shape[0]
resultat=resultat.reshape((int(M),2))
plt.plot(resultat2[:,0],resultat2[:,1],color="r")
plt.title("Test avec Angle de 90°")
plt.show()

# do back. 
resultat_back1=np.array([fonction_g(elt,prop=1/2,v=1,avance=2) for elt in vecteur_temps])
M=resultat_back1.shape[0]
resultat_back=resultat_back1.reshape((int(M),2))
plt.plot(resultat_back1[:,0],resultat_back1[:,1])
resultat_back2=np.array([fonction_g(elt,prop=-1/2,v=1,avance=2) for elt in vecteur_temps])
M=resultat_back2.shape[0]
resultat_back=resultat_back2.reshape((int(M),2))
plt.plot(resultat_back2[:,0],resultat_back2[:,1],color="r")
plt.title("Test avec Angle de -90°")
plt.show()