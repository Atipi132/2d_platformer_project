# Projet de platformeur 2D en python
Nous tenterons dans ce projet de créer quelques niveaux d'un platformeur 2D, inspiré de Donkey Kong. 
Il faudra donc implémenter :
- Un personnage pouvant bouger et effectuer des actions suivant les touches appuyées par l'utilisateur
- De la physique pour implémenter un saut, une vitesse ainsi qu'une chute
- Des arrières plans pour rendre le jeu plus vivants
- Des ennemies pouvant infliger des dégats au joueur

## Membres de l'équipe
- [Ylian Sidre](https://github.com/TDEVYS)
- [Hugo Pothieux](https://github.com/Atipi132)

## Répartition des tâches

### 1. Physique et animations (Mardi 02/04/2024)
-   [Hugo](https://github.com/Atipi132) s'occupera de faire fonctionner un sytème de physique (Réalisé pendant la séance du Mardi 02/04/2024)
-   [Ylian](https://github.com/TDEVYS) s'occupera des animations (Réalisé pendant la séance du Mardi 02/04/2024)

### 2. Attaques et ennemis (Jeudi 04/04/2024)
-   [Ylian](https://github.com/TDEVYS) a ajouté des animations et créé un prototype d'attaque pour le joueur.
-   [Hugo](https://github.com/Atipi132) a créé une nouvelle classe pour les Non-playable characters, plus particulièrement les ennemis.

### 3. Attaques fonctionnelles, nouvelles animations (Jeudi 11/04/2024)
-   [Hugo](https://github.com/Atipi132) a modifié la fonction d'attaque du joueur pour qu'elle fonctionne et qu'elle tue les ennemis qu'elle touche. Un cooldown a aussi été ajouté pour éviter de garder l'attaque toujours activée.
-   [Ylian](https://github.com/TDEVYS) a récupéré et découpé de nouveaux sprites pour le joueur à partir de [ce pack](https://legnops.itch.io/red-hood-character).

### 4. Nouvelle version : réécriture complète du moteur physique et de l'ennemi (Du Jeudi 11/04/2024 au Vendredi 17/05/2024)
-   [Ylian](https://github.com/TDEVYS) a complètement réécri le moteur graphique afin de pouvoir suivre le joueur avec une caméra. Cela a été fait grâce à [ce tutoriel](https://www.youtube.com/watch?v=WViyCAa6yLI), expliquant notamment comment utiliser [Tiled](https://www.mapeditor.org/).

-   [Hugo](https://github.com/Atipi132) a travaillé sur l'ennemi afin de le faire fonctionner dans ce nouveau moteur graphique.


## Ressources

Nous nous sommes aidé de tutoriels tels que [celui-ci](https://docs.replit.com/tutorials/python/2d-platform-game) et utilisé des [ressources libres de droit pour les pour les graphismes](https://jesse-m.itch.io/jungle-pack).




