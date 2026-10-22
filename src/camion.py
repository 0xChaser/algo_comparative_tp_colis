import time
from dataclasses import dataclass, field
from colis import Colis
from tri import tri_fusion

BONUS_PRIORITE_PCT = 15  # Bonus par niveau au-dessus de la priorité 1.


def valeur_effective(c: Colis, bonus_pct: int = BONUS_PRIORITE_PCT) -> int:
    """Score multiplié par 100 pour garder des entiers. Bonus 0 : valeur seule."""
    return c.valeur * (100 + bonus_pct * (c.priorite - 1))


@dataclass
class Chargement:
    colis: list = field(default_factory=list)
    capacite: int = 0
    methode: str = ""
    bonus_pct: int = 0
    score: int = 0  # Total avec le bonus de priorité.
    temps: float = 0.0

    @property
    def poids(self):
        total = 0
        for c in self.colis:
            total += c.poids
        return total
    @property
    def valeur(self):
        total = 0
        for c in self.colis:
            total += c.valeur
        return total


LIMITE_CASES_DP = 300_000_000  # Limite la mémoire de la table de décisions.


def sac_a_dos_dp(colis, capacite, bonus_pct=BONUS_PRIORITE_PCT):
    """Sac à dos exact. Temps et mémoire O(n * W), avec W la capacité."""
    candidats = [c for c in colis if c.poids <= capacite]
    W = min(capacite, sum(c.poids for c in candidats))  # inutile de dépasser le poids total
    if len(candidats) * (W + 1) > LIMITE_CASES_DP:
        raise MemoryError("Table de programmation dynamique trop grande.")
    dp = [0] * (W + 1)
    decisions = []
    for c in candidats:
        p = c.poids
        v = valeur_effective(c, bonus_pct)
        ligne = bytearray(W + 1)
        # On descend pour ne pas utiliser le même colis plusieurs fois.
        for w in range(W, p - 1, -1):
            avec = dp[w - p] + v
            if avec > dp[w]:
                dp[w] = avec
                ligne[w] = 1
        decisions.append(ligne)
    # On remonte la table pour retrouver les colis retenus.
    choisis = []
    w = W
    for i in range(len(candidats) - 1, -1, -1):
        c = candidats[i]
        if decisions[i][w]:
            choisis.append(c)
            w -= c.poids
    choisis.reverse()
    return choisis, dp[W]


def sac_a_dos_glouton(colis, capacite, bonus_pct=BONUS_PRIORITE_PCT):
    """Prend les meilleurs ratios score/poids. Rapide, mais pas toujours optimal."""
    cand = [c for c in colis if c.poids <= capacite]
    tries = tri_fusion(cand, lambda c: valeur_effective(c, bonus_pct) / c.poids, True)
    choisis, reste = [], capacite
    for c in tries:
        if c.poids <= reste:
            choisis.append(c)
            reste -= c.poids
    score = sum(valeur_effective(c, bonus_pct) for c in choisis)
    if cand:
        meilleur = max(cand, key=lambda c: valeur_effective(c, bonus_pct))
        if valeur_effective(meilleur, bonus_pct) > score:
            return [meilleur], valeur_effective(meilleur, bonus_pct)
    return choisis, score


def preparer_camion(colis, capacite, methode="dp", bonus_pct=BONUS_PRIORITE_PCT) -> Chargement:
    if capacite < 0:
        raise ValueError("Capacité négative.")
    t0 = time.perf_counter()
    if methode == "dp":
        try:
            sel, score = sac_a_dos_dp(colis, capacite, bonus_pct)
        except MemoryError:
            methode = "glouton (repli : table DP trop grande)"
            sel, score = sac_a_dos_glouton(colis, capacite, bonus_pct)
    elif methode == "glouton":
        sel, score = sac_a_dos_glouton(colis, capacite, bonus_pct)
    else:
        raise ValueError("Méthode inconnue.")
    return Chargement(sel, capacite, methode, bonus_pct, score, time.perf_counter() - t0)
