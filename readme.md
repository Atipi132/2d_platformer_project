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
-   [Ylian](https://github.com/TDEVYS) a complètement réécrit le moteur graphique afin de pouvoir suivre le joueur avec une caméra. Cela a été fait grâce à [ce tutoriel](https://www.youtube.com/watch?v=WViyCAa6yLI), expliquant notamment comment utiliser [Tiled](https://www.mapeditor.org/).

-   [Hugo](https://github.com/Atipi132) a travaillé sur l'ennemi afin de le faire fonctionner dans ce nouveau moteur graphique.

### 5. Nouveau niveau, nouvel ennemi et un menu
-   [Hugo](https://github.com/Atipi132) a travaillé sur un menu permettant de choisir la taille de la fenêtre souhaitée pour le jeu. Il a aussi créé un moyen de transitionner entre plusieurs niveau lorsque le joueur arrive à la fin d'un niveau.

-   [Ylian](https://github.com/TDEVYS) a ajouté un nouvel ennemi ([la sorcière](https://9e0.itch.io/witches-pack)) et a créé un nouveau niveau où cet ennemi est présent.

## Ressources

Nous nous sommes aidé de tutoriels tels que [celui-ci](https://docs.replit.com/tutorials/python/2d-platform-game) et utilisé des ressources libres de droit pour les pour les graphismes :
- [personnage principal](https://legnops.itch.io/red-hood-character)
- [ennemi squelette](https://jesse-m.itch.io/skeleton-pack)
- [ennemi sorcière](https://9e0.itch.io/witches-pack)
- [tuiles des niveaux](https://ninjikin.itch.io/starter-tiles?download)

## Utilisation du jeu

Pour lancer le jeu, il suffit d'utiliser la commande
```script
python main.py
```
dans le dossier contenant le jeu.

- ### Commandes du jeu
    Il suffit d'utiliser les flèches de votre clavier pour vous déplacer. La touche `A` permet d'attaquer et la touche `espace` permet de sauter.

    Pour mettre le jeu en pause, il suffit d'appuyer sur la toucher `Echap`.