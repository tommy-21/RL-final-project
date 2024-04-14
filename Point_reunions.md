# RL-final-project
Projet final de Reinforcement Learning

## Point des informations donnnées par le prof


### Interface utilisateur
* Attendus :
    - Une fenêtre représentant l'interface, avec un chemin (un départ et une arrivée)
    - Deux modes : Manuel et Automatique et si possible un troisième (Semi-Automatique)
* Utiliser pygame si nous n'avons jamais codé un jeu auparavant

### Algorithmes
Plusieurs cas sont à distinguer :
* Cas discret : l'espace d'état (les coordonnées x et y de la voiture) est discret ; l'algo Q-learning. 
* Cas continu : l'espace d'état est continu ; l'algo : Q-Learning adapté ou QNN

### Données d'entrainement
A simuler selon le cas (discret ou continu) et nos variables 

## Point de la rencontre du jeudi 14/03/2024
Nous avons choisi de faire le cas continu pour l'instant. 
 
- ⭐ Etats $S_t$ (variables définissant l'état) 
    * position : x, y
    * vitesse : v 
    * Orientation : $\theta$ (angle par rapport à une référence)
    * Obstacles : pas encore concrètement définis

- 🦾 Actions $A_t$ (vu comme les actions possibles à l'utilisateur)
    * Accélérer ⏫
    * Ralentir 🔼
    * Reculer ⏬
    * Tourner à gauche ⬅️
    * Tourner à droite ➡️

- 🌟 Nouvel état $S_{t+1}$ : Le nouvel état sera calculé par une fonction g à partir de l'état actuel et de l'action effectuée telle que : $$S_{t+1} = g(S_t, A_t)$$
  
- 💰 Récompenses
    * Sort de la route : -(??)
    * Cogne obstacle : -(??)
    * Atteint l'arrivée : +(??)
    * Respecte pas le code de la route : -(??)

- ❓ Problématiques ouvertes
    * Compréhension de l'adaptation de l'algo Q-Learning et l'implémentation des réseaux de neurones QNN
    * Comment va se faire la simulation des données ?
    * Définition de la fonction $g$
    * Prise en main de pygame
    * Formalisation des obstables (variable d'état)
    * Semi-discret ou continu ? la question reste ouverte (surtout en ce qui concerne le temps aussi) 
    * Vitesse maximale indépassable ou pénalisante ?
