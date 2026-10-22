from colis import Colis, PRIORITE_MIN, PRIORITE_MAX
from tri import tri_fusion, tri_par_comptage, borne_inferieure, borne_superieure


class CollectionColis:
    """Les colis sont rangés par identifiant. On garde aussi un index par destination."""

    def __init__(self):
        self._par_id: dict[int, Colis] = {}
        self._par_dest: dict[str, list[Colis]] = {}
        self._cache: dict = {}

    def ajouter(self, colis: Colis) -> None:
        """Refuse les doublons et efface les anciens tris."""
        if colis.id in self._par_id:
            raise ValueError(f"Identifiant {colis.id} déjà utilisé.")
        self._par_id[colis.id] = colis
        destination = colis.destination.lower()
        if destination not in self._par_dest:
            self._par_dest[destination] = []
        self._par_dest[destination].append(colis)
        if self._cache:
            self._cache.clear()

    def trouver(self, id_colis: int):
        return self._par_id.get(id_colis)

    def trouver_lineaire(self, id_colis: int):
        for c in self._par_id.values():
            if c.id == id_colis:
                return c
        return None

    def par_destination(self, destination: str) -> list[Colis]:
        """Renvoie une copie des colis de cette destination."""
        return list(self._par_dest.get(destination.lower(), []))

    def __len__(self):
        return len(self._par_id)

    def __iter__(self):
        return iter(self._par_id.values())

    def tous(self) -> list[Colis]:
        return list(self._par_id.values())

    def trier(self, critere: str, decroissant: bool | None = None) -> list[Colis]:
        """Tri en O(n log n) au premier appel, puis résultat gardé en cache."""
        if critere not in ("poids", "valeur", "priorite"):
            raise ValueError("Critère inconnu (poids | valeur | priorite).")
        if decroissant is None:
            decroissant = critere != "poids"
        cle = (critere, decroissant)
        if cle in self._cache:
            return self._cache[cle]
        if critere == "poids":
            res = tri_fusion(self._par_id.values(), lambda c: c.poids, decroissant)
        elif critere == "valeur":
            res = tri_fusion(self._par_id.values(), lambda c: c.valeur, decroissant)
        else:
            base = self.trier("valeur", True)
            res = tri_par_comptage(base, lambda c: c.priorite,
                                   range(PRIORITE_MIN, PRIORITE_MAX + 1), decroissant)
        self._cache[cle] = res
        return res

    def plage_poids(self, pmin: int, pmax: int) -> list[Colis]:
        """Deux recherches dichotomiques dans la liste triée : O(log n + k)."""
        vue = self.trier("poids", False)
        if "poids_cles" not in self._cache:
            self._cache["poids_cles"] = [c.poids for c in vue]
        cles = self._cache["poids_cles"]
        return vue[borne_inferieure(cles, pmin):borne_superieure(cles, pmax)]

    def statistiques(self) -> dict:
        """Calcule les totaux en un parcours : O(n)."""
        n = len(self)
        if n == 0:
            return {"n": 0}
        tp = tv = 0
        pmin = pmax = None
        par_prio = {p: 0 for p in range(PRIORITE_MIN, PRIORITE_MAX + 1)}
        for c in self._par_id.values():
            tp += c.poids
            tv += c.valeur
            if pmin is None or c.poids < pmin:
                pmin = c.poids
            if pmax is None or c.poids > pmax:
                pmax = c.poids
            par_prio[c.priorite] += 1
        return {
            "n": n, "poids_total": tp, "valeur_totale": tv,
            "poids_moyen": tp / n, "valeur_moyenne": tv / n,
            "poids_min": pmin, "poids_max": pmax,
            "par_priorite": par_prio,
            "par_destination": {d: len(l) for d, l in self._par_dest.items()},
        }
