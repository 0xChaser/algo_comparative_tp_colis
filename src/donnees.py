import csv
import random
from colis import Colis
from collection import CollectionColis

DESTINATIONS = ["Paris", "Lille", "Lyon", "Marseille", "Bordeaux", "Nantes", "Toulouse", "Nice"]


def generer(n: int, graine: int = 42, poids_max: int = 30, valeur_max: int = 100,
            collection: CollectionColis | None = None, debut_id: int = 1) -> CollectionColis:
    rnd = random.Random(graine)
    col = collection if collection is not None else CollectionColis()
    for i in range(debut_id, debut_id + n):
        col.ajouter(Colis(i, rnd.randint(1, poids_max), rnd.randint(1, valeur_max),
                          rnd.randint(1, 5), rnd.choice(DESTINATIONS)))
    return col


def exemple_sujet() -> CollectionColis:
    col = CollectionColis()
    for t in [(101, 8, 20, 2, "Paris"), (102, 3, 10, 5, "Lille"), (103, 12, 40, 1, "Lyon"),
              (104, 5, 25, 4, "Paris"), (105, 2, 15, 3, "Lille")]:
        col.ajouter(Colis(*t))
    return col


def importer_csv(chemin: str, col: CollectionColis) -> tuple[int, int]:
    """Lit id, poids, valeur, priorité, destination. Renvoie les nombres acceptés et rejetés."""
    ok = ko = 0
    with open(chemin, newline="", encoding="utf-8") as f:
        echantillon = f.read(2048); f.seek(0)
        delim = max([",", ";", "\t"], key=echantillon.count)
        for ligne in csv.reader(f, delimiter=delim):
            try:
                col.ajouter(Colis(int(ligne[0]), int(ligne[1]), int(ligne[2]), int(ligne[3]), ligne[4].strip()))
                ok += 1
            except (ValueError, IndexError):
                ko += 1  # en-tête, ligne invalide ou doublon
    return ok, ko


def exporter_csv(chemin: str, colis) -> None:
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "poids", "valeur", "priorite", "destination"])
        for c in colis:
            w.writerow([c.id, c.poids, c.valeur, c.priorite, c.destination])
