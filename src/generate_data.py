import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 100_000
equipes = ["Support N1", "Support N2", "Infra", "Applicatif", "Sécurité"]
equipe = rng.choice(equipes, size=n)
priorites = ["P1", "P2", "P3", "P4"]
priorite = rng.choice(priorites, size=n, p=[0.03, 0.12, 0.55, 0.30])
canaux  = ["portail", "email", "téléphone", "chat"]
canal = rng.choice(canaux, size=n)
jours = pd.date_range("2025-01-01", "2025-12-31", freq="D")
ouverture = rng.choice(jours, size=n)

duree_h = rng.lognormal(mean=np.log(12), sigma=0.6, size=n)
df = pd.DataFrame({
    "equipe": equipe,
    "priorite": priorite,
    "canal": canal,
    "ouverture": ouverture,
    "duree_h": duree_h.round(1),
})

print(df.head(10))
print(df["duree_h"].describe())