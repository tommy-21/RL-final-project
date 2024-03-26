
import numpy as np
import matplotlib.pyplot as plt
def fonction_g(t,prop,v,avance):
    angle=(np.pi) * prop
    if avance==1:
        if angle!=0: 
            if abs(angle)<abs((np.pi/4)):
                elt=abs((np.pi/4)-abs(angle))/2
            elif abs(angle)<abs((np.pi/2)):
                elt=abs((np.pi/2)-abs(angle))/2
            elif abs(angle)<abs((np.pi/8)):
                elt=abs((np.pi/8)-abs(angle))/2  
            else:
                elt=abs((3*np.pi/4)-abs(angle))/2  
            t_post=abs(elt/angle)
            x_etoile=v*t_post*np.cos((np.pi/2)-angle*t_post)
            y_etoile=v*t_post*np.sin((np.pi/2)-angle*t_post)
            if t<=t_post:
                x=v*t*np.cos((np.pi/2)-angle*t)
                y=v*t*np.sin((np.pi/2)-angle*t)
            if t>t_post:
                angle_postmouv=((np.pi)/2)-angle
                x=x_etoile+v*(t-t_post)*np.cos(angle_postmouv)
                y=y_etoile+v*(t-t_post)*np.sin(angle_postmouv)
        else:
            x=v*t*np.cos(((np.pi)/2)-angle)
            y=v*t*np.sin(((np.pi)/2)-angle)
    else:
        if angle!=0:
            angle=np.pi*prop
            if abs(angle) <abs((np.pi/4)):
                elt=abs((np.pi/4)-abs(angle))/2
            elif abs(angle)<abs((np.pi/2)):
                elt=abs((np.pi/2)-abs(angle))/2
            elif abs(angle)<abs((np.pi/8)):
                elt=abs((np.pi/8)-abs(angle))/2   
            else:
                elt=abs((3*np.pi/4)-abs(angle))/2  
            t_post=abs(elt/angle)
            x_etoile=v*t_post*np.cos((np.pi/2)+angle*t_post)
            y_etoile=-v*t_post*np.sin((np.pi/2)+angle*t_post)
            if t<=t_post:
                x=v*t*np.cos(-(np.pi/2)-angle*t)
                y=v*t*np.sin(-(np.pi/2)-angle*t)
            if t>t_post:
                angle_postmouv=-((np.pi)/2)-angle
                x=x_etoile+v*(t-t_post)*np.cos(angle_postmouv)
                y=y_etoile+v*(t-t_post)*np.sin(angle_postmouv)
        else:
            x=v*t*np.cos(((np.pi)/2)-angle)
            y=-v*t*np.sin(((np.pi)/2)-angle)
    return([x,y])

vecteur_temps=np.linspace(0,10,100)
angle=np.pi/4

resultat=np.array([fonction_g(elt,prop=1/8,v=1,avance=1) for elt in vecteur_temps])
M=resultat.shape[0]
resultat=resultat.reshape((int(M),2))
plt.plot(resultat[:,0],resultat[:,1])
# 
resultat2=np.array([fonction_g(elt,prop=-1/8,v=1,avance=2) for elt in vecteur_temps])
M=resultat.shape[0]
resultat=resultat.reshape((int(M),2))
plt.plot(resultat2[:,0],resultat2[:,1],color="r")
plt.title("Test avec Angle de 90°")
plt.show()
