from fonction_g import fonction_g
import pandas as pd
import numpy as np

def simulation(t, prop, v, avance=1):
    
    data = []
    
    # si la voiture effectue une marche en avant
    if avance:
        for time in t:
            for angle in prop:
                for vitesse in v:
                    result = fonction_g(time, angle, vitesse, avance)
                    data.append({'Time': time, 'Angle': angle, 'Vitesse': vitesse, 'X': result[0], 'Y': result[1]})

    else:
        for time in t:
            for angle in prop:
                for vitesse in v:
                    result = fonction_g(time, angle, vitesse, avance)
                    data.append({'Time': time, 'Angle': angle, 'Vitesse': vitesse, 'X': result[0], 'Y': result[1]})
    
    df = pd.DataFrame(data)
    return df



t = [0,1]
prop = [0, 1/8]
v = [1, 2]

df = simulation(t, prop, v)
print(df)
