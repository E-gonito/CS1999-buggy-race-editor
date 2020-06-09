import sqlite3

DATABASE_FILE = "database.db"

con = sqlite3.connect(DATABASE_FILE)
print("- Opened database successfully in file \"{}\"".format(DATABASE_FILE))

# using Python's triple-quote for multi-line strings:

con.execute("""

  CREATE TABLE IF NOT EXISTS buggies (
    id                    INTEGER PRIMARY KEY,
    qty_wheels            INTEGER DEFAULT 4,
    flag_color            VARCHAR(20) DEFAULT 'white',
    flag_color_secondary  VARCHAR(20) DEFAULT 'black',
    flag_pattern          VARCHAR(20) DEFAULT 'plain',
    banging               BOOLEAN DEFAULT FALSE,
    power_type            VARCHAR(20) DEFAULT 'petrol',
    power_units           INTEGER DEFAULT 1,
    aux_power_type        VARCHAR(20) DEFAULT 'none',
    aux_power_units       INTEGER DEFAULT 0,
    hamster_booster       INTEGER DEFAULT 0,
    tyres                 VARCHAR(20) DEFAULT 'knobbly',
    qty_tyres             INTEGER DEFAULT 4,
    armour                VARCHAR(20) DEFAULT 'none',
    fireproof             BOOLEAN DEFAULT FALSE,
    insulated             BOOLEAN DEFAULT FALSE,
    antibiotic            BOOLEAN DEFAULT FALSE,
    attack                VARCHAR(20) DEFAULT 'none',
    qty_attacks           INTEGER DEFAULT 0,
    algo                  VARCHAR(20) DEFAULT 'steady',
    total_cost            INTERGER DEFAULT 64
    
    
  )

""")

print("- Table \"buggies\" exists OK")

cur = con.cursor()

cur.execute("SELECT * FROM buggies LIMIT 1")
rows = cur.fetchall()
if len(rows) == 0:
  cur.execute("INSERT INTO buggies (qty_wheels) VALUES (4)")
  con.commit()
  print("- Added one 4-wheeled buggy")
else:
  print("- Found a buggy in the database, nice")
print("- done")

con.close()
