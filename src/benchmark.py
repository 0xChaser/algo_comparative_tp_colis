import time
from pathlib import Path

import donnees
from camion import preparer_camion


def main():
    lignes = [
        '# Résultats des mesures',
        '',
        'Capacité : 50 kg. Bonus de priorité : 0. Temps en millisecondes.',
        '',
        '| Nombre de colis | Tri par poids (ms) | Chargement (ms) |',
        '|---|---|---|',
    ]

    for n in (100, 1000, 10000, 100000):
        col = donnees.generer(n)

        debut = time.perf_counter()
        col.trier('poids')
        temps_tri = (time.perf_counter() - debut) * 1000

        chargement = preparer_camion(col.tous(), 50, bonus_pct=0)
        temps_camion = chargement.temps * 1000

        lignes.append(f'| {n} | {temps_tri:.2f} | {temps_camion:.2f} |')

    texte = '\n'.join(lignes) + '\n'
    print(texte)
    chemin = Path(__file__).with_name('resultats_benchmark.md')
    chemin.write_text(texte, encoding='utf-8')


if __name__ == '__main__':
    main()
