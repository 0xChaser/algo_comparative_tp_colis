def tri_fusion(elements, cle, decroissant=False):
    """Fusionne des blocs de taille 1, 2, 4, etc. Temps O(n log n), mémoire O(n)."""
    n = len(elements)
    a = [(cle(x), x) for x in elements]
    if n < 2:
        return [x for _, x in a]
    b = [None] * n
    largeur = 1
    while largeur < n:
        for debut in range(0, n, 2 * largeur):
            milieu = min(debut + largeur, n)
            fin = min(debut + 2 * largeur, n)
            i, j, k = debut, milieu, debut
            while i < milieu and j < fin:
                # En cas d'égalité, on garde l'ordre de départ.
                if decroissant:
                    prendre_droite = a[j][0] > a[i][0]
                else:
                    prendre_droite = a[j][0] < a[i][0]
                if prendre_droite:
                    b[k] = a[j]
                    j += 1
                else:
                    b[k] = a[i]
                    i += 1
                k += 1
            while i < milieu:
                b[k] = a[i]
                i += 1
                k += 1
            while j < fin:
                b[k] = a[j]
                j += 1
                k += 1
        a, b = b, a
        largeur *= 2
    return [x for _, x in a]


def tri_par_comptage(elements, cle, valeurs_possibles, decroissant=False):
    """Un paquet par priorité. Avec 5 priorités, le tri prend O(n)."""
    paquets = {v: [] for v in valeurs_possibles}
    for x in elements:
        paquets[cle(x)].append(x)
    ordre = sorted(valeurs_possibles, reverse=decroissant)
    resultat = []
    for v in ordre:
        resultat.extend(paquets[v])
    return resultat


def borne_inferieure(valeurs_triees, cible):
    """Premier indice dont la valeur est supérieure ou égale à la cible."""
    lo, hi = 0, len(valeurs_triees)
    while lo < hi:
        mid = (lo + hi) // 2
        if valeurs_triees[mid] < cible:
            lo = mid + 1
        else:
            hi = mid
    return lo


def borne_superieure(valeurs_triees, cible):
    """Premier indice dont la valeur est strictement supérieure à la cible."""
    lo, hi = 0, len(valeurs_triees)
    while lo < hi:
        mid = (lo + hi) // 2
        if valeurs_triees[mid] <= cible:
            lo = mid + 1
        else:
            hi = mid
    return lo
