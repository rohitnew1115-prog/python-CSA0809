import tempfile, unittest
from pathlib import Path
from Task05_AI_Applications.chatbot import answer
from Task05_AI_Applications.summariser import summarize
from Task09_Final_Engineering_Decision.final_system import create_db

class ApplicationTests(unittest.TestCase):
    def test_parameterized_chatbot_lookup(self):
        with tempfile.TemporaryDirectory() as d:
            con=create_db(Path(d)/"ai.db")
            con.execute("INSERT INTO stations(station_name,area) VALUES(?,?)",("Adyar","South"))
            sid=con.execute("SELECT station_id FROM stations WHERE station_name=?",("Adyar",)).fetchone()[0]
            con.execute("INSERT INTO readings(station_id,observed_at,pm25) VALUES(?,?,?)",(sid,"2026-10-01T08:00:00",48)); con.commit()
            self.assertIn("48.0",answer("What is PM2.5 in Adyar today?",con))
            self.assertIn("name a monitoring station",answer("What is PM2.5 today?",con))
            con.close()
    def test_extractive_summary_keeps_source_sentences(self):
        source="Smoke affects the road. The road needs repair. The monitor is online."
        summary=summarize(source,max_sentences=2)
        self.assertIn(".",summary); self.assertTrue(all(s in source for s in summary.split(". ") if s))

if __name__=="__main__": unittest.main()
