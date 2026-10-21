from pathlib import Path

import duckdb

con = duckdb.connect("data/itsm.duckdb")

requete = Path("sql/kpis_equipe.sql").read_text(encoding="utf-8")
con.sql(requete).show()

requete = Path("sql/kpis_priorite.sql").read_text(encoding="utf-8")
con.sql(requete).show()

con.close()