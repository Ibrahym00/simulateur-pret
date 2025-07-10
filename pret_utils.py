import pandas as pd

def calculer_mensualite(capital, taux_annuel, duree_annees):
    n = duree_annees * 12
    t = taux_annuel / 12 / 100

    if t == 0:
        mensualite = capital / n
    else:
        mensualite = (capital * t) / (1 - (1 + t) ** -n)

    total = mensualite * n
    interets = total - capital

    return round(mensualite, 2), round(total, 2), round(interets, 2)


def generer_tableau_amortissement(capital, taux_annuel, duree_annees):
    n = duree_annees * 12
    t = taux_annuel / 12 / 100
    mensualite, _, _ = calculer_mensualite(capital, taux_annuel, duree_annees)

    data = []
    capital_restant = capital

    for mois in range(1, n + 1):
        interet_mensuel = capital_restant * t
        capital_rembourse = mensualite - interet_mensuel
        capital_restant -= capital_rembourse
        capital_restant = max(0, capital_restant)

        data.append({
            "Mois": mois,
            "Mensualité (EUR)": round(mensualite, 2),
            "Intérêt payé (EUR)": round(interet_mensuel, 2),
            "Capital remboursé (EUR)": round(capital_rembourse, 2),
            "Capital restant dû (EUR)": round(capital_restant, 2)
        })

    df = pd.DataFrame(data)
    return df
