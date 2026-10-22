from colis import Colis, ENTETE
from camion import preparer_camion, BONUS_PRIORITE_PCT
import donnees

PAGE = 20


def lire_int(msg, defaut=None, minimum=None):
    while True:
        s = input(msg).strip()
        if not s and defaut is not None:
            return defaut
        try:
            v = int(s)
            if minimum is not None and v < minimum:
                print(f"  Valeur minimale : {minimum}"); continue
            return v
        except ValueError:
            print("  Entrez un entier.")


def afficher(liste, titre="", limite=PAGE):
    """Affiche 20 colis à la fois par défaut."""
    if titre:
        print(f"\n--- {titre} ({len(liste)} colis) ---")
    if not liste:
        print("  (aucun colis)"); return
    debut = 0
    while debut < len(liste):
        print(ENTETE)
        for c in liste[debut:debut + limite]:
            print(c.ligne())
        debut += limite
        if debut < len(liste):
            if input(f"  [{debut}/{len(liste)}] Entrée = suite, q = arrêter : ").strip().lower() == "q":
                break


def menu_afficher(col):
    afficher(col.tous(), "Colis (ordre d'insertion)")


def menu_ajouter(col):
    try:
        c = Colis(lire_int("ID : "), lire_int("Poids (entier) : "), lire_int("Valeur : "),
                  lire_int("Priorité (1-5, 5 = urgent) : "), input("Destination : "))
        col.ajouter(c)
        print("  Colis ajouté.")
    except ValueError as e:
        print(f"  Erreur : {e}")


def menu_rechercher(col):
    print("1. Par identifiant   2. Par destination   3. Par plage de poids")
    ch = input("Choix : ").strip()
    if ch == "1":
        c = col.trouver(lire_int("ID : "))
        print(ENTETE)
        if c:
            print(c.ligne())
        else:
            print("  Introuvable.")
    elif ch == "2":
        afficher(col.par_destination(input("Destination : ")), "Résultat")
    elif ch == "3":
        afficher(col.plage_poids(lire_int("Poids min : "), lire_int("Poids max : ")), "Résultat")


def menu_organiser(col):
    print("Trier par : 1. Poids  2. Valeur  3. Priorité")
    choix = input("Choix : ").strip()
    if choix == "1":
        crit = "poids"
    elif choix == "2":
        crit = "valeur"
    elif choix == "3":
        crit = "priorite"
    else:
        print("  Choix invalide.")
        return
    sens = input("Sens : 1. croissant  2. décroissant  (Entrée = défaut) : ").strip()
    dec = None
    if sens == "1":
        dec = False
    elif sens == "2":
        dec = True
    afficher(col.trier(crit, dec), f"Colis triés par {crit}")


class Etat:
    chargement = None


def menu_camion(col, etat):
    if len(col) == 0:
        print("  Aucun colis."); return
    cap = lire_int("Capacité maximale du camion : ", minimum=0)
    bonus = lire_int(f"Bonus de priorité en % par niveau [{BONUS_PRIORITE_PCT}] (0 = ignorer) : ",
                     BONUS_PRIORITE_PCT, 0)
    m = input("Méthode : 1. Optimale (programmation dynamique)  2. Gloutonne  [1] : ").strip()
    methode = "dp"
    if m == "2":
        methode = "glouton"
    etat.chargement = preparer_camion(col.tous(), cap, methode, bonus)
    print(f"  Camion préparé en {etat.chargement.temps*1000:.1f} ms.")
    menu_chargement(etat)


def menu_chargement(etat):
    ch = etat.chargement
    if ch is None:
        print("  Aucun chargement préparé."); return
    afficher(ch.colis, f"Chargement ({ch.methode}, capacité {ch.capacite}, bonus priorité {ch.bonus_pct}%)")
    print(f"  Poids : {ch.poids}/{ch.capacite}   Valeur réelle : {ch.valeur}   "
          f"Score pondéré : {ch.score/100:.2f}")


def menu_stats(col, etat):
    s = col.statistiques()
    if s["n"] == 0:
        print("  Aucun colis."); return
    print(f"\n  Colis : {s['n']}   Poids total : {s['poids_total']}   Valeur totale : {s['valeur_totale']}")
    print(f"  Poids moyen : {s['poids_moyen']:.2f} (min {s['poids_min']}, max {s['poids_max']})   "
          f"Valeur moyenne : {s['valeur_moyenne']:.2f}")
    print("  Par priorité :", ", ".join(f"{p}: {k}" for p, k in s["par_priorite"].items()))
    print("  Par destination :", ", ".join(f"{d}: {k}" for d, k in sorted(s["par_destination"].items())))
    if etat.chargement:
        ch = etat.chargement
        print(f"  Dernier chargement : {len(ch.colis)} colis, {ch.poids}/{ch.capacite} kg, valeur {ch.valeur}")


def menu_generer(col):
    n = lire_int("Nombre de colis à générer : ", minimum=1)
    debut = max((c.id for c in col), default=0) + 1
    donnees.generer(n, collection=col, debut_id=debut)
    print(f"  {n} colis ajoutés (total : {len(col)}).")


def menu_csv(col):
    chemin = input("Chemin du fichier CSV : ").strip()
    try:
        ok, ko = donnees.importer_csv(chemin, col)
        print(f"  {ok} colis importés, {ko} lignes rejetées.")
    except OSError as e:
        print(f"  Erreur : {e}")


def main():
    col = donnees.exemple_sujet()
    etat = Etat()
    while True:
        print("\n===== GESTION DES LIVRAISONS =====")
        print("1. Afficher les colis\n2. Ajouter un colis\n3. Rechercher un colis\n"
              "4. Organiser les colis\n5. Préparer un camion\n6. Afficher le chargement\n"
              "7. Afficher les statistiques\n8. Générer des colis aléatoires\n9. Importer un CSV\n0. Quitter")
        ch = input("Choix : ").strip()
        if ch == "0":
            break
        elif ch == "1":
            menu_afficher(col)
        elif ch == "2":
            menu_ajouter(col)
        elif ch == "3":
            menu_rechercher(col)
        elif ch == "4":
            menu_organiser(col)
        elif ch == "5":
            menu_camion(col, etat)
        elif ch == "6":
            menu_chargement(etat)
        elif ch == "7":
            menu_stats(col, etat)
        elif ch == "8":
            menu_generer(col)
        elif ch == "9":
            menu_csv(col)
        else:
            print("  Choix invalide.")


if __name__ == "__main__":
    main()
