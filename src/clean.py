import pandas as pd

df = pd.read_csv("data/tickets_raw.csv", parse_dates=["ouverture", "resolution"])

print(df.shape)
print(df.dtypes)

print("doublons :", df["ticket_id"].duplicated().sum())
print("valeurs vides :")
print(df.isna().sum())
print("dates impossibles :", (df["resolution"] < df["ouverture"]).sum())
print("lignes brutes :", len(df))

# doublons : on garde la premiere occurrence
df = df.drop_duplicates(subset="ticket_id", keep="first")

# resolution avant l'ouverture = erreur de saisie, je ne garde pas cette date
impossible = df["resolution"] < df["ouverture"]
df.loc[impossible, "resolution"] = pd.NaT

df["categorie"] = df["categorie"].fillna("Non renseignée")

sla = {"P1": 4, "P2": 8, "P3": 24, "P4": 72}
df["sla_h"] = df["priorite"].map(sla)

df["duree_h"] = (df["resolution"] - df["ouverture"]).dt.total_seconds() / 3600
df["resolu"] = df["resolution"].notna()
df["sla_respecte"] = (df["duree_h"] <= df["sla_h"]).astype("boolean")
df.loc[~df["resolu"], "sla_respecte"] = pd.NA
df["jour"] = df["ouverture"].dt.normalize()

df.to_parquet("data/tickets_clean.parquet", index=False)
print("lignes propres :", len(df))
print(df.head())