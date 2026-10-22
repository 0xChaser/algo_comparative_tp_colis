# Rendu Projet Algo Comparative - Florian ISAK

Gestion de colis et préparation du chargement d'un camion.
Pour ce TP, j’ai utilisé Python car je suis plus à l’aise avec ce langage qu’avec le C.
Python 3.10+ suffit, sans bibliothèque externe.

## Lancer le programme

```bash
cd src
python3 main.py
```

Le menu permet d'ajouter, rechercher et trier les colis, puis de préparer un camion.
Il propose aussi des statistiques, la génération de colis et l'import CSV.

## Mesurer les performances

```bash
python3 benchmark.py
```

Les mesures portent sur le tri et le chargement, avec 100, 1 000, 10 000 et 100 000 colis.

Les poids sont des entiers en kg. Les priorités vont de 1 à 5 (5 = urgente).
Le bonus de priorité est réglable ; 0 permet de maximiser uniquement la valeur.

Les choix et les résultats sont présentés dans `rapport.pdf`.