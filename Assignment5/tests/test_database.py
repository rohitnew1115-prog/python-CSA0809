import tempfile, unittest
from pathlib import Path
from Task09_Final_Engineering_Decision.final_system import create_db, station_average

class DatabaseTests(unittest.TestCase):
    def test_parameterized_insert_and_injection(self):
        with tempfile.TemporaryDirectory() as d:
            con=create_db(Path(d)/"test.db")
            con.executemany("INSERT INTO stations(station_name,area) VALUES(?,?)",[("Adyar","South"),("Guindy","West")])
            ids=dict(con.execute("SELECT station_name,station_id FROM stations"))
            rows=[("Adyar","2026-10-01",48.0),("Guindy","2026-10-01",95.0),("Guindy","2026-10-03",121.0),("Adyar","2026-10-04",60.0)]
            con.executemany("INSERT INTO readings(station_id,observed_at,pm25) VALUES(?,?,?)",[(ids[s],t,v) for s,t,v in rows]); con.commit()
            self.assertEqual(station_average(con,"Adyar"),54.0); self.assertEqual(station_average(con,"Guindy"),108.0)
            self.assertIsNone(station_average(con,"Adyar' OR '1'='1")); con.close()

if __name__=="__main__": unittest.main()
