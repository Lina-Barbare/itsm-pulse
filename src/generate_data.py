from pathlib import Path

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 100_000

equipes = ["Support N1", "Support N2", "Infra", "Applicatif", "Sécurité"]
equipe = rng.choice(equipes, size=n)
priorites = ["P1", "P2", "P3", "P4"]
priorite = rng.choice(priorites, size=n, p=[0.03, 0.12, 0.55, 0.30])
canaux = ["Portail", "Email", "Téléphone", "Chat"]
canal = rng.choice(canaux, size=n)
categories = ["Réseau", "Messagerie", "Poste de travail", "Applications", "Accès & droits", "Impression"]
categorie = rng.choice(categories, size=n)

# moins de tickets le week-end
jours = pd.date_range("2025-01-01", "2025-12-31", freq="D")
poids = np.where(jours.dayofweek < 5, 1.0, 0.35)

# j'ai cree une panne reseau du 10 au 12 juin pour tester la detection
panne = (jours >= "2025-06-10") & (jours <= "2025-06-12")
poids = poids * np.where(panne, 2.2, 1.0)
poids = poids / poids.sum()

jour = rng.choice(jours, size=n, p=poids)
minutes = rng.integers(7 * 60, 19 * 60, size=n)
ouverture = pd.to_datetime(jour) + pd.to_timedelta(minutes, unit="m")

pendant_panne = (ouverture >= "2025-06-10") & (ouverture < "2025-06-13")
categorie = np.where(pendant_panne & (rng.random(n) < 0.6), "Réseau", categorie)

vitesse_equipe = {
    "Support N1": 6,
    "Support N2": 14,
    "Infra": 20,
    "Applicatif": 18,
    "Sécurité": 10,
}
base = np.array([vitesse_equipe[e] for e in equipe])
facteur_priorite = np.select(
    [priorite == "P1", priorite == "P2"],
    [0.25, 0.5],
    default=1.0,
)
duree_h = rng.lognormal(mean=np.log(base * facteur_priorite), sigma=0.6)

# 2e incident : applicatif ralentit du 1er au 21 septembre
ralenti = (equipe == "Applicatif") & (ouverture >= "2025-09-01") & (ouverture < "2025-09-22")
duree_h = np.where(ralenti, duree_h * 2.5, duree_h)

resolution = (ouverture + pd.to_timedelta(duree_h, unit="h")).round("min")
reouvertures = rng.choice([0, 1, 2], size=n, p=[0.91, 0.08, 0.01])

df = pd.DataFrame({
    "ticket_id": [f"INC{100000 + i}" for i in range(n)],
    "equipe": equipe,
    "priorite": priorite,
    "canal": canal,
    "categorie": categorie,
    "ouverture": ouverture,
    "resolution": resolution,
    "reouvertures": reouvertures,
})

# j'ajoute des erreurs volontaires pour tester le nettoyage
doublons = df.sample(300, random_state=1)

idx = df.sample(150, random_state=2).index
df.loc[idx, "resolution"] = df.loc[idx, "ouverture"] - pd.Timedelta(hours=2)

idx = df.sample(200, random_state=3).index
df.loc[idx, "categorie"] = None

idx = df.sample(500, random_state=4).index
df.loc[idx, "resolution"] = pd.NaT

df = pd.concat([df, doublons], ignore_index=True)

Path("data").mkdir(exist_ok=True)
df.to_csv("data/tickets_raw.csv", index=False)
print(f"{len(df)} lignes enregistrees")