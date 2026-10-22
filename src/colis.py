from dataclasses import dataclass

PRIORITE_MIN, PRIORITE_MAX = 1, 5  # 5 = priorité la plus importante


@dataclass(slots=True)
class Colis:
    """slots évite un dictionnaire par colis et réduit la mémoire utilisée."""
    id: int
    poids: int        # Poids entier en kg.
    valeur: int
    priorite: int     # 1 = faible, 5 = forte.
    destination: str

    def __post_init__(self):
        if not isinstance(self.poids, int) or self.poids <= 0:
            raise ValueError("Le poids doit être un entier strictement positif.")
        if not isinstance(self.valeur, int) or self.valeur < 0:
            raise ValueError("La valeur doit être un entier positif ou nul.")
        if not (PRIORITE_MIN <= self.priorite <= PRIORITE_MAX):
            raise ValueError(f"La priorité doit être entre {PRIORITE_MIN} et {PRIORITE_MAX}.")
        if not self.destination.strip():
            raise ValueError("La destination ne peut pas être vide.")

    def ligne(self) -> str:
        return f"{self.id:>8} {self.poids:>7} {self.valeur:>8} {self.priorite:>9}  {self.destination}"


ENTETE = f"{'ID':>8} {'Poids':>7} {'Valeur':>8} {'Priorité':>9}  Destination"
